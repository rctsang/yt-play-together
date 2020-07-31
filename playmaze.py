import pygame
from pygame.locals import *
from maze import Maze

# Much of this code comes from a tutorial found here: https://pythonspot.com/maze-in-pygame/

class Player:
    speed = 3
    scalar = 20

    def __init__(self, maze, w=15, h=15):
    	self.loc = (maze.start[0]*self.scalar+2, maze.start[1]*self.scalar+2)
    	self.w = w
    	self.h = h
    	self.maze = maze.maze
    	self.big_maze = maze.big_maze

    def solved(self):
	    if (self.big_maze[self.loc[0]][self.loc[1]] == 'e'
	    	or self.big_maze[self.loc[0]][self.loc[1]+self.h] == 'e'
	    	or self.big_maze[self.loc[0]+self.w+1][self.loc[1]] == 'e'
	    	or self.big_maze[self.loc[0]+self.w+1][self.loc[1]+self.h] == 'e'):
	    	return True
	    return False

 
    def moveRight(self, maze_full):
    	if (maze_full[self.loc[0]+self.w+(self.speed)][self.loc[1]] != 1
    		and maze_full[self.loc[0]+self.w+(self.speed)][self.loc[1]+self.h] != 1):
        	self.loc = (self.loc[0]+self.speed, self.loc[1])
 
    def moveLeft(self, maze_full):
    	if (maze_full[self.loc[0]-(self.speed)][self.loc[1] != 1]
    		and maze_full[self.loc[0]-(self.speed)][self.loc[1]+self.h] != 1):
    		self.loc = (self.loc[0]-self.speed, self.loc[1])
 
    def moveUp(self, maze_full):
    	if (maze_full[self.loc[0]][self.loc[1]-(self.speed)] != 1
    		and maze_full[self.loc[0]+self.w][self.loc[1]-(self.speed)] != 1):
    		self.loc = (self.loc[0], self.loc[1]-self.speed)
 
    def moveDown(self, maze_full):
    	if (maze_full[self.loc[0]][self.loc[1]+self.h+(self.speed)] != 1
    		and maze_full[self.loc[0]+self.w][self.loc[1]+self.h+(self.speed)] != 1):
    		self.loc = (self.loc[0], self.loc[1]+self.speed)

    def draw(self, display_surf, image_surf):
    	display_surf.blit(image_surf, (self.loc[0], self.loc[1]))

class App:
 
    windowWidth = 420
    windowHeight = 420
    player = 0
 
    def __init__(self):
        self.start_size = 10
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self.maze = Maze(dx=self.start_size, dy=self.start_size)
        self.maze_full = self.maze.makeFullSize()
        # print(len(self.maze_full))
        self.player = Player(self.maze)
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.image.load("imgs/blue_tile15x15.jpg").convert()
        self._block_surf = pygame.image.load("imgs/black_tile20x20.jpg").convert()
        self.maze.wall_img = pygame.image.load("imgs/black_tile20x20.jpg").convert()
        self.maze.start_img = pygame.image.load("imgs/yellow_tile20x20.jpg").convert()
        self.maze.end_img = pygame.image.load("imgs/green_tile20x20.jpg").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        if self.player.solved():
        	# self.start_size += 5
        	self.maze = Maze(dx=self.start_size, 
        					dy=self.start_size,
        					wall_img=self.maze.wall_img,
        					start_img=self.maze.start_img,
        					end_img=self.maze.end_img)
        	self.maze_full = self.maze.makeFullSize()
        	# print(len(self.maze_full))
        	self.player = Player(self.maze)
        pass
    
    def on_render(self):
        self._display_surf.fill((255,255,255))
        self.maze.draw(self._display_surf)
        self.player.draw(self._display_surf, self._image_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            
            if (keys[K_RIGHT]):
                self.player.moveRight(self.maze_full)
 
            if (keys[K_LEFT]):
                self.player.moveLeft(self.maze_full)
 
            if (keys[K_UP]):
                self.player.moveUp(self.maze_full)
 
            if (keys[K_DOWN]):
                self.player.moveDown(self.maze_full)
 
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()