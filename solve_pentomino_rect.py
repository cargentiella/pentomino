# -*- coding: utf-8 -*-
import sys
import os
import copy
import csv
import numpy as np


# -------- init --------


class BLOCK:

	types = ['f', 'i', 'l', 'n', 'p', 't', 'u', 'v', 'w', 'x', 'y', 'z']

	shape = {
		'f' : np.array([[0, 1, 1],
						[1, 1, 0],
						[0, 1, 0]]),
		'i' : np.array([[1],
						[1],
						[1],
						[1],
						[1]]),
		'l' : np.array([[1, 0],
						[1, 0],
						[1, 0],
						[1, 1]]),
		'n' : np.array([[0, 1],
						[0, 1],
						[1, 1],
						[1, 0]]),
		'p' : np.array([[1, 1],
						[1, 1],
						[1, 0]]),
		't' : np.array([[1, 1, 1],
						[0, 1, 0],
						[0, 1, 0]]),
		'u' : np.array([[1, 0, 1],
						[1, 1, 1]]),
		'v' : np.array([[1, 0, 0],
						[1, 0, 0],
						[1, 1, 1]]),
		'w' : np.array([[1, 0, 0],
						[1, 1, 0],
						[0, 1, 1]]),
		'x' : np.array([[0, 1, 0],
						[1, 1, 1],
						[0, 1, 0]]),
		'y' : np.array([[0, 1],
						[1, 1],
						[0, 1],
						[0, 1]]),
		'z' : np.array([[1, 1, 0],
						[0, 1, 0],
						[0, 1, 1]])
	}

	value = {
		'f' : 1,
		'i' : 2,
		'l' : 3,
		'n' : 4,
		'p' : 5,
		't' : 6,
		'u' : 7,
		'v' : 8,
		'w' : 9,
		'x' : 10,
		'y' : 11,
		'z' : 12
	}

	directions = {
		'f' : [0, 1, 2, 3, 4, 5, 6, 7],
		'i' : [0,          4         ],
		'l' : [0, 1, 2, 3, 4, 5, 6, 7],
		'n' : [0, 1, 2, 3, 4, 5, 6, 7],
		'p' : [0, 1, 2, 3, 4, 5, 6, 7],
		't' : [0, 1, 2, 3            ],
		'u' : [0, 1, 2, 3            ],
		'v' : [0, 1, 2, 3            ],
		'w' : [0, 1, 2, 3            ],
		'x' : [0                     ],
		'y' : [0, 1, 2, 3, 4, 5, 6, 7],
		'z' : [0, 1,       4, 5      ]
	}

	def __init__(self):
		self.figures = {}
		self.tops = {}

		for type in BLOCK.types:
			figures = []
			tops = []
			for d in BLOCK.directions[type]:
				_figure = BLOCK.shape[type]
				if d // 4 == 1:
					_figure = _figure.T

				if d % 4 == 1:
					_figure = np.rot90(_figure)
				elif d % 4 == 2:
					_figure = np.rot90(_figure, 2)
				elif d % 4 == 3:
					_figure = np.rot90(_figure, 3)

				h, w = _figure.shape
				if w <= width and h <= height:
					figures.append(_figure * BLOCK.value[type])
					tops.append(self._top(_figure))

			self.figures[type] = figures
			self.tops[type] = tops


	def _top(self, _figure):
		y, x = np.where(_figure > 0)
		return np.array([y[0], x[0]])



# -------- func --------


def next_blank(_box):
	y, x = np.where(_box < 1)
	return np.array([y[0], x[0]])


def can_put_figure(box, position, figure):
	h, w = figure.shape

	if position[1] < 0 or width < position[1] + w:
		return False
	if position[0] < 0 or height < position[0] + h:
		return False

	y, x = np.where(figure > 0)
	for i in range(len(y)):
		if box[position[0] + y[i], position[1] + x[i]] != 0:
			return False

	return True


def put_figure(_box, position, _figure):
	h, w = _figure.shape

	for y in range(h):
		for x in range(w):
			_box[position[0] + y][position[1] + x] += _figure[y, x]

	return _box


def save_solution(_box):
#	print(_box.flatten())
	writer.writerow(_box.flatten())


def put_block_recursive(box, ptr, unused):

	for type in unused:
		_unused = copy.deepcopy(unused)
		_unused.remove(type)

		for f in range(len(block.figures[type])):

			position = ptr - block.tops[type][f]

			if can_put_figure(box, position, block.figures[type][f]):
				_box = put_figure(copy.deepcopy(box), position, block.figures[type][f])

				if len(_unused) == 0:
					save_solution(_box)
				else:
					_ptr = next_blank(_box)
					put_block_recursive(_box, _ptr, _unused)


def solve_pentomino_rect(width, height):

	if width * height != 60:
		print("[ERROR] width * height not equal 60.")

	box = np.zeros((height, width), dtype=int)
	ptr = np.array([0, 0])
	unused = copy.deepcopy(block.types)

	put_block_recursive(box, ptr, unused)



# -------- main --------

if __name__ == '__main__':
	global block
	global width
	global height
	global writer

	usage = 'Usage: python solve_pentomino_rect [width] [height]'

	args = sys.argv
	if len(args) == 3:
		width  = int(args[1])
		height = int(args[2])

		block = BLOCK()
		file = "solution_rect_" + str(width) + "x" + str(height) + ".txt"

		f = open(file, 'w', encoding='utf-8')
		writer = csv.writer(f, delimiter=',', lineterminator='\n')

		solve_pentomino_rect(width, height)

		f.close

	else:
		print(usage)



