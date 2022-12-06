import pygame
pygame.font.init()
import math
from queue import PriorityQueue
from time import time

WIDTH = 200
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Forward A*")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY_1 = (117, 117, 117)
GREY_2 = (158, 158, 158)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.adjacent = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == GREY_2

	def is_open(self):
		return self.color == GREY_1

	def is_wall(self):
		return self.color == BLACK

	def is_source(self):
		return self.color == PURPLE

	def is_target(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_source(self):
		self.color = PURPLE

	def make_closed(self):
		self.color = GREY_2

	def make_open(self):
		self.color = GREY_1

	def make_wall(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def shortest_path(self):
		self.color = ORANGE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_adjacent_nodes(self, grid):
		self.adjacent = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall(): # DOWN
			self.adjacent.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_wall(): # UP
			self.adjacent.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall(): # RIGHT
			self.adjacent.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): # LEFT
			self.adjacent.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def construct_shortest_path(came_from, current, draw):
        res = []
        count = 0
        while current in came_from:
                current = came_from[current]
                current.shortest_path()
                row, col = current.get_pos()
                res.append((row, col))
                count = count+1
                draw()
        if count != 0:
                print ("\nShortest Path from Agent to Target:", count,  "steps\n")
                for row, col in reversed(res):
                        print ("[", row, col, "]", end=' : ', flush=True)

def astar_forward(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	g_value = {spot: float("inf") for row in grid for spot in row}
	g_value[start] = 0
	f_value = {spot: float("inf") for row in grid for spot in row}
	f_value[start] = h(start.get_pos(), end.get_pos())
	open_set.put((0, g_value[start], start)) #tie breaker situation if f_value is same then node is chosen based on g_value
	came_from = {}
	

	open_set_hash = {start}
	print("\n\nOpen list for traversal in order:\n")
	print("Position\tg_value\th_value\tf_value\n")
	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
  
		current = open_set.get()[2]
		open_set_hash.remove(current)
		if current == end:
			construct_shortest_path(came_from, end, draw)
			print ("[", end.row, end.col, "]")
			end.make_end()
			start.make_source()
			return True

		print("(", current.row, current.col, ")", "\t", g_value[current], "\t",h(current.get_pos(), end.get_pos()), "\t",f_value[current])

		for adjacent in current.adjacent:
			temp_g_value = g_value[current] + 1

			if temp_g_value < g_value[adjacent]:
				came_from[adjacent] = current
				g_value[adjacent] = temp_g_value
				f_value[adjacent] = temp_g_value + h(adjacent.get_pos(), end.get_pos())
				if adjacent not in open_set_hash:
					count += 1
					open_set.put((f_value[adjacent], g_value[adjacent], adjacent))
					open_set_hash.add(adjacent)
					adjacent.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Node(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 5
	grid = make_grid(ROWS, width)
	gap = width // ROWS
	start = None
	end = None
	val = 0
	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					print("\n\nAgent Position\t: [", row, col, "]")
					start.make_source()

				elif not end and spot != start:
					end = spot
					print("Target Position\t: [", row, col, "]")
					end.make_end()


				elif spot != end and spot != start:
					spot.make_wall()

			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_adjacent_nodes(grid)
					t0 = time()
					val = astar_forward(lambda: draw(win, grid, ROWS, width), grid, start, end)
					t1 = time()

					if val==0:
                                                print ("\nNo path from Agent to Target\n")

					print ("\n\nExecution time for A* = %f" %(t1-t0) + " seconds\n")
					

	pygame.quit()

main(WIN, WIDTH)
