import os
import json
import time
from keys import Keyboard
from GBACommander import *

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
invalid_broadcast_status = {"complete", "revoked"}

def countdown(t):
    for i in range(t):
        print("\r*** %d ***" %(t-i), end="")
        time.sleep(1)
    print("*** 0 ***")

def executeCommandsIn(response, finder):
    # iterate through all the returned messages and execute any commands
    for msg in response["items"]:
        # Make sure that the message is the right type and the "messageText" key is actually present
        if msg["snippet"]["type"] == "textMessageEvent":
            # print(msg["snippet"]["textMessageDetails"]["messageText"])

            # using CommandFinder from GBACommand.py, return a list of GBACommand objects for each command  
            #   present in the message string. commands with incorrect syntax and other stuff will be ignored
            cmds = finder.find(msg["snippet"]["textMessageDetails"]["messageText"])

            # execute each valid found command
            for cmd in cmds:
                if cmd.execute():
                    exit()

def main():
    # initialize the keyboard object that generates key events
    kb = Keyboard()

    # initialize the CommandFinder that searches for commands in a string
    finder = CommandFinder(GBACommand.cmdMap.keys())

    ###############################
    ### BEGIN YOUTUBE API CALLS ###
    ###############################

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "private/client_secret.json"

    # Get credentials and create an API client
    # This will ask you to go to a website and authorize my registered application 
    #   to allow access to your YouTube Account. It looks shady, but go to 
    #   "Advanced" -> "Proceed Anyways"
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # add a countdown for you to get ready on the right screen.
    stream_title = input("Input Stream Title Here: ")
    countdown(5)

    # Calls a list of current broadcasts on my account
    # Returns a json object documented here: 
    #   https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/list
    # Relevant Keys: (not a complete list)
    #   "etag": etag,
    #   "nextPageToken": string,
    #   "prevPageToken": string,
    #   "pageInfo": {
    #     "totalResults": integer,
    #     "resultsPerPage": integer
    #   },
    #   "items": [
    #     liveBroadcast Resource
    #   ]
    request = youtube.liveBroadcasts().list(
        part="snippet,contentDetails,status",
        # id="BROADCAST_ID"
        broadcastType="all",
        mine=True
    )
    broadcast_response = request.execute()

    # error checking
    # if the api errors, it'll return a json object with a single key: "error"
    if "error" in broadcast_response.keys():
    	print(broadcast_response)
    	return
    # print(broadcast_response["items"])

    # the "items" key is a list of all the Broadcast Objects found by the search
    if not broadcast_response["items"]:
    	print("Error: No Broadcasts Found!\n")
    	return

    # for dict (json) structure of a broadcast obj: 
    # https://developers.google.com/youtube/v3/live/docs/liveBroadcasts
    # Relevant Keys: (not a complete list)
    # "snippet": {
    #     "channelId": string,
    #     "title": string,
    #     "liveChatId": string
    # }

    # scan available broadcasts for correct title
    ytpt_broadcast = None
    for i in range(len(broadcast_response["items"])):
    	if (broadcast_response["items"][i]["snippet"]["title"] == stream_title
            and broadcast_response["items"][i]["status"]["liveCycleStatus"] not in invalid_broadcast_status):
    		ytpt_broadcast = broadcast_response["items"][i]
    
    # if right broadcast unavailable, abort
    if not ytpt_broadcast: return

    # get associated live chat id
    liveChatId = ytpt_broadcast["snippet"]["liveChatId"]

    # Calls a list of live chat messages from the broadcast's liveChat
    # The first time we do this, we do it without using the PageToken parameter,
    # but for all subsequent calls, we want to use it so that we don't end up with repeat messages.
    request = youtube.liveChatMessages().list(
        liveChatId=liveChatId,
        part="snippet"
    )
    response = request.execute()

    nextPageToken = response["nextPageToken"]
    pollIntervalSec = float(response["pollingIntervalMillis"]) / 1000

    # searches for commands in the API response and executes them
    executeCommandsIn(response, finder)

    # We need to wait before calling the api again by the indicated polling interval
    time.sleep(pollIntervalSec)
    
    alive = True
    strikes = 0
    while(alive):
        # This time, we'll call the list function with the PageToken parameter so we don't end up with repeats
        # This loop will repeatedly call the list function until list() returns an error, or the process is killed
        request = youtube.liveChatMessages().list(
            liveChatId=liveChatId,
            part="snippet",
            pageToken=nextPageToken
        )
        response = request.execute()

        nextPageToken = response["nextPageToken"]
        pollIntervalSec = float(response["pollingIntervalMillis"]) / 1000 + 0.1

        if not response["items"]:
            if strikes < 3:
                strikes += 1
            pollIntervalSec += 3 * strikes
        else:
            strikes = 0
            executeCommandsIn(response, finder)

        time.sleep(pollIntervalSec)


if __name__ == "__main__":
    main()

