import os
from time import sleep
from pickle import load

class GameOfLife(object):
	""" Implementation of John Conway's Game of Life

		RULES:
			1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
	    	2. Any live cell with two or three live neighbours lives on to the next generation.
	    	3. Any live cell with more than three live neighbours dies, as if by overpopulation.
	    	4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

	    These rules are implemented in calculate_next_generation. The run_simulation method returns a generator
	    that will iterate through the generations. self.grid can be accessed by external applications to display each
	    generation returned by run_simulation.
	"""

	ALIVE = '0'
	DEAD = '-'
	STARTING_PATTERNS = {'10-row': (tuple((10, i) for i in range(5, 15))),
						 'boat': ((6,6), (5,7), (7,7), (7,8), (6,8)),
						 'glider': ((6,6), (6,7), (6,8), (5,8), (4,7)),
						 'gosper_glider': load(open('gosper_glider_gun.pkl', 'rb')),
						 'R-pentomino': ((10,10), (10,9), (9,10),(11,10), (9,11))}


	def __init__(self, dimensions, starting_pattern, torodial=True):

		self.dimensions = dimensions
		self.tororidal = torodial
		# self.torodial is a flag do decide whether patterns can extend themselves over the border of the grid.
		# if set to True, any patterns crossing the bottom of the pane will be sent to the top (and vice versa), and any patterns
		# crossing the sides will wrap to the opposite side.
		self.grid = self.make_grid()
		self.print_grid(self.grid)
		self.starting_pattern = GameOfLife.STARTING_PATTERNS[starting_pattern]
		self.initialize_grid()
		self.print_grid(self.grid)


	def run_simulation(self, iterations):
		for _ in range(iterations):

			yield self.calculate_next_generation()


	def calculate_next_generation(self):

		next_generation = self.make_grid()

		for i in range(len(self.grid)):

			for j in range(len(self.grid[0])):

				n_neighbors = self.count_neighbors((i, j))
				if self.tororidal:
					i, j = i % self.dimensions[0], j % self.dimensions[1]



				if self.grid[i][j] == GameOfLife.ALIVE:

					if n_neighbors < 2:
						# 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
						next_generation[i][j] = GameOfLife.DEAD

					elif n_neighbors in (2,3):
						# 2. Any live cell with two or three live neighbours lives on to the next generation.
						next_generation[i][j] = GameOfLife.ALIVE
					else:
						# 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
						next_generation[i][j] = GameOfLife.DEAD

				else:

					if n_neighbors == 3:
						# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
						next_generation[i][j] = GameOfLife.ALIVE

		self.grid = next_generation
		return next_generation

	def print_grid(self, grid):

		for row in grid:

			for item in row:

					print(item, end='  ')

			print()


	def initialize_grid(self):

		for individual in self.starting_pattern:

			self.grid[individual[0]][individual[1]] = GameOfLife.ALIVE

	def make_grid(self):

		return [[GameOfLife.DEAD for _ in range(self.dimensions[1])] for _ in range(self.dimensions[0])]

	def count_neighbors(self, position):
		neighbors = [(1, 1), (0, 1), (1, 0),
					 (-1,-1), (0,-1), (-1, 0),
					 (-1, 1), (1,-1)]
		n_alive = 0
		if self.tororidal:
			position = (position[0] % self.dimensions[0], position[1] % self.dimensions[1])
		for neighbor in neighbors:
			neighbor = (position[0] + neighbor[0], position[1] + neighbor[1])

			try:
				if self.grid[neighbor[0]][neighbor[1]] == GameOfLife.ALIVE:
					n_alive += 1
			except IndexError:
				pass # do nothing

		return n_alive

if __name__ == '__main__':
	gol = GameOfLife((20,20), 'glider')
	clear = lambda: os.system('clear')
	for i in gol.run_simulation(100):

		gol.print_grid(i)
		sleep(1)
		clear()