from tkinter import *
from GameOfLife import GameOfLife

class GOLAnimation(object):
	"""Animates game of life using GameOfLife.py
		Takes a GameOfLife object as an argument and displays generations using tkinter
	"""
	def __init__(self, gol, num_iterations):

		self.gol = gol
		self.simulation = self.gol.run_simulation(num_iterations)

		# initialize gui window:
		self.root = Tk()
		self.root.title('Game of Life')
		# create all of the main containers
		center = Frame(self.root, bg='white', width=450, height=450, padx=3, pady=3)

		# layout all of the main containers
		self.root.grid_rowconfigure(self.gol.dimensions[0], weight=1)
		self.root.grid_columnconfigure(self.gol.dimensions[0], weight=1)
		center.grid(row=1, sticky="nsew")

		# create the center widgets
		center.grid_rowconfigure(0, weight=1)
		center.grid_columnconfigure(1, weight=1)

		self.cells = {}
		for row in range(self.gol.dimensions[0]):
			for column in range(self.gol.dimensions[1]):
				cell = Frame(center, bg='blue', highlightbackground="black",
							 highlightcolor="black", highlightthickness=1,
							 width=10, height=10, padx=3, pady=3)
				cell.grid(row=row, column=column)
				self.cells[(row, column)] = cell


	def call_next_gen(self):
		# get the next generation from GameOfLifeObject

		next(self.simulation)
		# color the grid cells either alive or dead:
		for row in range(len(self.gol.grid)):
			for col in range(len(self.gol.grid[0])):

				if self.gol.grid[row][col] == GameOfLife.ALIVE:
					self.cells[(row, col)].configure(background='DarkSeaGreen4')
				else:
					self.cells[(row, col)].configure(background='cornsilk3')
		# callback
		self.root.after(500, self.call_next_gen)

if __name__ == '__main__':

	gol = GameOfLife((20,50), 'glider', torodial=True)

	gola = GOLAnimation(gol, 50000000)

	gola.root.after(0, gola.call_next_gen)

	gola.root.mainloop()


