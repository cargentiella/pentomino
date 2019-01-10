# coding: utf-8
import sys
import os
import copy
import csv

# -------- init --------

args = sys.argv
if len(args) == 2:
	path = args[1]
	OUTPUT = True

if OUTPUT:
	file = open(path, 'w')
	writer = csv.writer(file, lineterminator=',')

BOX_WITH = 6
BOX_HEIGHT = 10

blocks = ['f', 'i', 'l', 'n', 'p', 't', 'u', 'v', 'w', 'x', 'y', 'z']

block_figure = {
	'f' : [	[0, 1, 1],
		[1, 1, 0],
		[0, 1, 0]	],
	'i' : [	[1, 1, 1, 1, 1], 
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	],
	'l' : [	[1, 1, 1, 1],
		[1, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0]	],
	'n' : [	[0, 1, 1, 1],
		[1, 1, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0]	],
	'p' : [	[1, 1, 1],
		[1, 1, 0],
		[0, 0, 0]	],
	't' : [	[1, 1, 1],
		[0, 1, 0],
		[0, 1, 0]	],
	'u' : [	[1, 1, 1],
		[1, 0, 1],
		[0, 0, 0]	],
	'v' : [	[1, 1, 1],
		[0, 0, 1],
		[0, 0, 1]	],
	'w' : [	[1, 1, 0],
		[0, 1, 1],
		[0, 0, 1]	],
	'x' : [	[0, 1, 0],
		[1, 1, 1],
		[0, 1, 0]	],
	'y' : [	[1, 1, 1, 1],
		[0, 1, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0]	],
	'z' : [	[1, 1, 0],
		[0, 1, 0],
		[0, 1, 1]	]
}

class Block:
	def __init__(self, type):
		self.figure = copy.deepcopy(block_figure[type])

	def turn(self, transform):
		if transform % 2 == 1:
			self.figure = copy.deepcopy(self.turn_mirror(self.figure))
		if transform // 2 % 2 == 1:
			self.figure = copy.deepcopy(self.turn_row(self.figure))
		if transform // 4 % 2 == 1:
			self.figure = copy.deepcopy(self.turn_col(self.figure))

		return self.figure

	def turn_mirror(self, block):
		_size = len(block)
		_block = [[0 for i in range(_size)] for j in range(_size)]
		for j in range(_size):
			for i in range(_size):
				_block[j][i] = block[i][j]
		return _block
	def turn_row(self, block):
		_size = len(block)
		_block = [[0 for i in range(_size)] for j in range(_size)]
		for j in range(_size):
			for i in range(_size):
				_block[j][i] = block[_size - 1 - j][i]
		return _block
	def turn_col(self, block):
		_size = len(block)
		_block = [[0 for i in range(_size)] for j in range(_size)]
		for j in range(_size):
			for i in range(_size):
				_block[j][i] = block[j][_size - 1 - i]
		return _block


turn_pattern = {
	'f' : [0, 1, 2, 3, 4, 5, 6, 7],
	'i' : [0, 1],
	'l' : [0, 1, 2, 3, 4, 5, 6, 7],
	'n' : [0, 1, 2, 3, 4, 5, 6, 7],
	'p' : [0, 1, 2, 3, 4, 5, 6, 7],
	't' : [0, 1, 2,       5],
	'u' : [0, 1, 2,       5],
	'v' : [0, 1, 2, 3],
	'w' : [0, 1, 2, 3],
	'x' : [0],
	'y' : [0, 1, 2, 3, 4, 5, 6, 7],
	'z' : [0, 1, 2, 3]
}

block_value = {
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
	'z' : 12,
}

pullet_end = '\033[0m'

pullet = [	'\033[30m', '\033[33m', '\033[31m', '\033[35m',
		'\033[32m', '\033[36m', '\033[35m', '\033[36m',
		'\033[31m', '\033[37m', '\033[37m', '\033[33m',
		'\033[32m'
]


# -------- func --------

def display_box(_box):
        for j in range(BOX_HEIGHT):
                for i in range(BOX_WITH):
                        sys.stdout.write(pullet[_box[j][i]] + "■" + pullet_end)
		sys.stdout.write("\n")

def put_block(_box, _ptr, _block, _value):
	for j in range(len(_block)):
		for i in range(len(_block[j])):
			if _block[j][i]:
				_box[_ptr[1] + j][_ptr[0] + i] = _value

def move_next(_box, _ptr):
# return next empty cell
	_next = [0, 0]

	for j in range(_ptr[1], BOX_HEIGHT):
		for i in range(BOX_WITH):
			if _box[j][i] == 0:
				_next[0] = i
				_next[1] = j
				return _next

def adjust_position(_box, _ptr, _block):
# return position that adjust _ptr and block head
	_adjust = [0, 0]
	for j in range(len(_block)):
		for i in range(len(_block[j])):
			if _block[j][i]:
				_adjust[0] = _ptr[0] - i
				_adjust[1] = _ptr[1] - j
				return _adjust

def can_put_block(_box, _ptr, _block):
	for j in range(len(_block)):
		for i in range(len(_block[j])):
			if _block[j][i]:
				# block is over box
				if _ptr[0] + i < 0 or BOX_WITH <= _ptr[0] + i:
					return False
				# block is over box
				if _ptr[1] + j < 0 or BOX_HEIGHT <= _ptr[1] + j:
					return False
				# block is over another block
				if _box[_ptr[1] + j][_ptr[0] + i] <> 0:
					return False
	return True

def island_area(_box, _verified, _x, _y):
	_area = 1
	_verified[_y][_x] = 1

	if 0 < _y and not _verified[_y - 1][_x] and _box[_y - 1][_x] == 0:
		_area += island_area(_box, _verified, _x, _y - 1)
	if _y < BOX_HEIGHT - 1 and not _verified[_y + 1][_x] and _box[_y + 1][_x] == 0:
		_area += island_area(_box, _verified, _x, _y + 1)		
	if 0 < _x and not _verified[_y][_x - 1] and _box[_y][_x - 1] == 0:
		_area += island_area(_box, _verified, _x - 1, _y)
	if _x < BOX_WITH - 1 and not _verified[_y][_x + 1] and _box[_y][_x + 1] == 0:
		_area += island_area(_box, _verified, _x + 1, _y)
	return _area

def not_have_island(_box, _ptr):
	_verified = [[0 for i in range(BOX_WITH)] for j in range(BOX_HEIGHT)]

	for j in range(_ptr[1], BOX_HEIGHT):
		for i in range(BOX_WITH):
			if _box[j][i] == 0 and _verified[j][i] == 0:
				if island_area(_box, _verified, i, j) < 5:
					return False
	return True

def no_more_block(_used):
	return len(_used) == 12

def write_solution(_box):
	writer.writerows(_box)
	file.write('\n')

def put_piece_recursive(box, ptr, used):
	adjust = [0, 0]

	for block in blocks:
		if block not in used:
			for turn in turn_pattern[block]:
				
				piece = Block(block)
				piece = copy.deepcopy(piece.turn(turn))

				adjust = adjust_position(box, ptr, piece)
				if can_put_block(box, adjust, piece):
					_box = copy.deepcopy(box)
					_used = copy.deepcopy(used)
					_ptr = [0, 0]

					put_block(_box, adjust, piece, block_value[block])
					_used.append(block)
					if no_more_block(_used):
						display_box(_box)
						print('------------')
						if OUTPUT:
							write_solution(_box)
					elif not_have_island(_box, ptr):
						_ptr = move_next(_box, ptr)
						put_piece_recursive(_box, _ptr, _used)


# -------- main --------

# init box
box = [[0 for i in range(BOX_WITH)] for j in range(BOX_HEIGHT)]
ptr = [0, 0]
used = []

put_piece_recursive(box, ptr, used)

if OUTPUT:
	file.close

