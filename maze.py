import random as rand
from pygame.locals import *
import pygame

class Maze:

	def getNeighbors(self, i, j):
		neighbors = []
		if i-2 > 0:
			neighbors += [(i-2, j)]
		if i+2 < 2*self.dx+1:
			neighbors += [(i+2, j)]
		if j-2 > 0:
			neighbors += [(i, j-2)]
		if j+2 < 2*self.dy+1:
			neighbors += [(i, j+2)]
		return neighbors

	def connectCells(self, c1, c2): # assumes given the odd integered indices
		# print(c1, c2)
		self.maze[(c1[0]+c2[0])//2][(c1[1]+c2[1])//2] = 0


	def __init__(self, dx=10, dy=10, wall_img=None, start_img=None, end_img=None):
		self.dx = dx
		self.dy = dy
		self.wall_img = wall_img
		self.start_img = start_img
		self.end_img = end_img
		self.maze = [[(i%2 & j%2)^1 for j in range(2*dy+1)] for i in range(2*dx+1)]
		self.big_maze = None

		# using Wilson's Algorithm to generate the maze
		# code based on stackexchange post here: https://codereview.stackexchange.com/questions/227660/maze-generator-animator-in-python
		visited = set()
		unvisited = set([(2*i+1, 2*j+1) for j in range(dy) for i in range(dx)])
		start = rand.choice(list(unvisited))
		visited.add(start)
		self.start = start
		path = [start]
		while unvisited:
			cur_cell = path[-1]
			new_cell = rand.choice(self.getNeighbors(cur_cell[0], cur_cell[1]))
			if new_cell in path and new_cell not in visited:
				erase = path.index(new_cell)
				del path[erase+1:]
			if new_cell in visited:
				for cell in path:
					visited.add(cell)
					if cell in unvisited:
						unvisited.remove(cell)
				path.append(new_cell)
				for i in range(len(path)-1):
					self.connectCells(path[i], path[i+1])
				path.clear()
				if unvisited:
					path.append(rand.choice(list(unvisited)))
			if new_cell not in path and new_cell not in visited:
				path.append(new_cell)
			# print(visited)

			# print(self.__repr__())

		self.end = rand.choice(self.getDeadEnds())
		self.maze[self.start[0]][self.start[1]] = 's'
		self.maze[self.end[0]][self.end[1]] = 'e'

		# print(self.__repr__())


	def __repr__(self):
		val = ""
		for j in range(2*self.dy+1):
			for i in range(2*self.dx+1):
				val += str(self.maze[i][j])
			val += '\n'
		return val

	def draw(self,display_surf):
		for i in range(2*self.dx+1):
			for j in range(2*self.dy+1):
				if self.maze[i][j] == 1:
					display_surf.blit(self.wall_img,(i*20 ,j*20))
				if self.maze[i][j] == 's':
					display_surf.blit(self.start_img,(i*20 ,j*20))
				if self.maze[i][j] == 'e':
					display_surf.blit(self.end_img,(i*20 ,j*20))

	def makeFullSize(self):
		full = []
		for i in range(2*self.dx+1):
			for a in range(20):
				col = []
				for j in range(2*self.dy+1):
					for b in range(20):
						# print(self.maze[i][j], end="")
						col += [self.maze[i][j]]
				full += [col]
				# print("\n")
		self.big_maze = full
		return full

	def isDeadEnd(self, i, j):
		walls = (self.maze[i+1][j]
				+ self.maze[i-1][j]
				+ self.maze[i][j+1]
				+ self.maze[i][j-1])
		return walls == 3

	def getDeadEnds(self):
		dead_ends = []
		for i in range(self.dx):
			for j in range(self.dy):
				if self.isDeadEnd(2*i+1, 2*j+1):
					dead_ends += [(2*i+1, 2*j+1)]
		return dead_ends


### Class Testing ###
if __name__ == "__main__":
	maze = Maze()
	# print(maze)