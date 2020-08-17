# YouTube Play Together

This is a continuation of what I began in [zoom-plays](https://github.com/tsangryan/zoom-plays) in which I continue to try to create a "Twitch Plays"-like game using a different platform. As Zoom has failed for now due to its API's lack of ability to access In-Meeting chat messages, I will instead try to make this work as unlisted livestreams on YouTube.

At some point I'll give this a better UI, but for now it's real ugly and barely works.

## Running the "App"
In the main folder of the repo, first make sure you have all the necessary dependencies in your environment (see below)
Currently only `playgba.py` is working with YouTube Live. 

```
python3 playgba.py 	# starts the script
```
Notes: You will need to have a valid `client_secrets.json` file saved in a folder named `private/` for this script to work. `playgba.py` simply gets gba commands from the YouTube LiveChat and simulates a corrosponding keystroke.

## Dependencies

- `pyobjc-framework-quartz`
- `google-api-python-client`
- `google-auth-oauthlib`
- `pygame`

I used virtualenv for this.
Check `req.txt` for a full list of dependencies.

### Setting Up a Virtual Environment

**Creating a Virtual Env**
```
pip install virtualenv
virtualenv ytptenv 									# Creates a new virtual environment named ytptenv
source ytptenv/bin/activate							# activates the virtual environment
ytpyenv/bin/pip install pyobjc-framework-quartz 	# install quartz
ytpyenv/bin/pip install google-api-python-client	# install google api for python
```

**Common Commands**
- `source <env>/bin/activate` - activates virtual environment
- `pip list` or `pip freeze` - lists installed packages in envirtual env.
- `pip freeze > req.txt` - saves list of installed packages to a txt file named "req.txt"
- `pip install -r req.txt` - pip installs all the packages listed in req.txt
- `deactivate` - deactivates environment (only use after activating env.)
- `rm -r <env>` - deletes a created virtual environment (make sure to deactivate it first)

Note: using `pip` while the environment is equivalent to `<env>/bin/pip`

## YouTube Interface

I'll be attempting to use the python wrapper for the YouTube livestream API to access the live chat. 

A ton of stuff is going on here so I'll try to explain what's happening in comments rather than here. But here's a basic overview of what's happening:

First, I created a project on [Google Developer Console](https://console.developers.google.com/). Since I want to access live broadcasts with my app, I need to use Oauth 2.0 for API access. I created an Oauth2 consent form in the tab on the console, then in the Credentials tab of the console, I created an Oauth2 user and downloaded the corrosponding `client_secrets.json` file, so that my app knows where to go to get authorization.

Using the YouTube Live Streaming API, which is partially included in the YouTube Data API, I can access the liveBroadcast API to search my accout's channel (choose your account during runtime on the Oauth2 consent screen) for any ready or active live broadcasts. I can select the one I want by title, then access the associated liveChatId.

Using the liveChatMessages API, I can use my obtained liveChatId to access the text messages on the live chat, which I can then process to find game commands.

I have yet to figure out how to save OAuth2 Refresh Tokens so i don't have to constantly be allowing account access for my app, but I'll get to that eventually. Maybe.

In other news, this more or less works, though the latency leads to about a 10s lag time between commenting on youtube and broadcasting a video response. The way I set it up, the lag time will increase if fewer people are playing in order to avoid burning through my api quota (ends up being a lot if I'm sending a request every 42 ms)

## GBA Game Interface

It's a dumbinterface. since most emulators for mac lack lua scripting capacity (waiting on mGBA release), this interface is literally just generated keyboard events while the emulator is in the foreground. Too lazy to compile the emulator's source files on my own so this is what it is for now.

For now I'm using [mGBA](https://github.com/mgba-emu/mgba) which says it'll support lua scripting eventually

## Building Simple Python Games

For the event that I want to use this for, Pokemon is no good. I need some games that are fast, high energy, and chaotic to engage a large online crowd. I have two games in mind: Tug o' War and a Maze Game.

I'll be developing these with pygame

### Tug O War

*not started*

### Maze Game

I'll be using [Wilson's Algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Wilson's_algorithm) to generate mazes, code modified so that the maze will be generated on a binary grid. The example I used was found on this [stackexchange post](https://codereview.stackexchange.com/questions/227660/maze-generator-animator-in-python)

The code itself was mostly copied from another [pygame maze tutorial](https://pythonspot.com/maze-in-pygame/)
The game is endless. You start on the yellow square and try to get to the green one. 

## Useful Links

**For YouTube Interface**
- [pytchat package (didn't use)](https://pypi.org/project/pytchat/)
- [Google Developer Console](https://console.developers.google.com/)
- [YouTube Live API (2013)](https://youtube-eng.googleblog.com/2013/05/streaming-to-youtube-live-put-api-on-it_2.html)
- [YouTube Live Streaming API Overview](https://developers.google.com/youtube/v3/live/getting-started?hl=en_US)
- [YouTube Data API Instance Methods](https://google-api-client-libraries.appspot.com/documentation/youtube/v3/python/latest/)
- [Live Streaming API Use Cases and Code Snippets](https://developers.google.com/youtube/v3/live/code_samples)
- [API LiveBroadcasts](https://developers.google.com/youtube/v3/live/docs/liveBroadcasts#status.lifeCycleStatus)
- [API LiveChatMessages](https://developers.google.com/youtube/v3/live/docs/liveChatMessages#resource)
- [YouTube Python API Samples on Github](https://github.com/youtube/api-samples/tree/master/python)
- [YouTube Data API Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost)

*Google's Oauth 2 Stuff*
- [Oauth2.0 for Installed Apps](https://developers.google.com/youtube/v3/guides/auth/installed-apps#custom-uri-scheme)
- [google-auth-oauthlib](https://google-auth-oauthlib.readthedocs.io/en/latest/)
- [google-auth-oauthlib.flow](https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html)
- [google-auth-oauthlib.credentials](https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html#google.oauth2.credentials.Credentials)

**For Game Interface**

*Pygame*
- [pygame: getting started](https://www.pygame.org/wiki/GettingStarted)
- [pygame intro](https://www.pygame.org/docs/tut/PygameIntro.html)
- [pygame docs](https://www.pygame.org/docs/)
- [pygame tutorials](https://www.pygame.org/wiki/tutorials)

*Generating Key Events*
- [Mac Virtual Keycodes](https://gist.github.com/eegrok/949034)
- [Generating Keyboard Events in Python (stackoverflow)](https://stackoverflow.com/questions/13564851/how-to-generate-keyboard-events-in-python)
- [apple developer quartz event services](https://developer.apple.com/documentation/coregraphics/quartz_event_services#//apple_ref/c/func/CGEventCreateKeyboardEvent)
- [quartz to generate key events](https://stackoverflow.com/questions/6868167/how-to-generate-keyboard-keypress-events-through-python-to-control-pp-presentati)
- [CGEventCreateKeyboardEvent](https://developer.apple.com/documentation/coregraphics/1456564-cgeventcreatekeyboardevent?language=objc)
- [PyPI Quartz page](https://pypi.org/project/pyobjc-framework-Quartz/)

*Virtual HID to trick OpenEmu (Unattempted)*
- [hidapi github](https://github.com/libusb/hidapi)
- [cython homepage](https://cython.org/#about)

*Lua Scripting (Not Possible on Mac)*
- [TASVideos Emulator Resources](http://tasvideos.org/EmulatorResources/VBA/LuaScriptingFunctions.html)
- [Github TASVideos/vba-rerecording](https://github.com/TASVideos/vba-rerecording)
- [SDL used by vbe-rr](http://www.libsdl.org/)
- [Lua Scripting Example with an SNES emulator on Windows](https://www.twilio.com/blog/2015/08/romram-hacking-building-an-sms-powered-game-genie-with-lua-and-python.html)
- [Lua Homepage](https://www.lua.org/)
- [Lua Manual](https://www.lua.org/manual/5.4/manual.html#2)
- [Python Wrapper Package for Lua](https://pypi.org/project/lupa/)