# coding: utf-8
import sys
import copy
import csv

# -------- init --------

args = sys.argv
if len(args) == 2:
	path = args[1]
	OUTPUT = True
else:
	OUTPUT = False

if OUTPUT:
	file = open(path, 'w')
	writer = csv.writer(file, lineterminator=',')

CUBE_WITH = 5
CUBE_HEIGHT = 4
CUBE_DEPTH = 3

blocks = ['f', 'i', 'l', 'n', 'p', 't', 'u', 'v', 'w', 'x', 'y', 'z']

block_figure = {
	'f' : [[	[0, 1, 1],
			[1, 1, 0],
			[0, 1, 0]	]],
	'i' : [[	[1, 1, 1, 1, 1], 
			[0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0]	]],
	'l' : [[	[1, 1, 1, 1],
			[1, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0]	]],
	'n' : [[	[0, 1, 1, 1],
			[1, 1, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0]	]],
	'p' : [[	[1, 1, 1],
			[1, 1, 0],
			[0, 0, 0]	]],
	't' : [[	[1, 1, 1],
			[0, 1, 0],
			[0, 1, 0]	]],
	'u' : [[	[1, 1, 1],
			[1, 0, 1],
			[0, 0, 0]	]],
	'v' : [[	[1, 1, 1],
			[0, 0, 1],
			[0, 0, 1]	]],
	'w' : [[	[1, 1, 0],
			[0, 1, 1],
			[0, 0, 1]	]],
	'x' : [[	[0, 1, 0],
			[1, 1, 1],
			[0, 1, 0]	]],
	'y' : [[	[1, 1, 1, 1],
			[0, 1, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0]	]],
	'z' : [[	[1, 1, 0],
			[0, 1, 0],
			[0, 1, 1]	]]
}

class Block:
	def __init__(self, type):
		self.figure = copy.deepcopy(block_figure[type])

	def turn(self, transform):
		_size = len(self.figure[0])

		if transform % 2 == 1:
			self.figure = copy.deepcopy(self.turn_mirror(self.figure, _size))
		if transform // 2 % 2 == 1:
			self.figure = copy.deepcopy(self.turn_row(self.figure, _size))
		if transform // 4 % 2 == 1:
			self.figure = copy.deepcopy(self.turn_col(self.figure, _size))
		if transform // 8 == 1:
			self.figure = copy.deepcopy(self.turn_horizontal(self.figure, _size))
		if transform // 8 == 2:
			self.figure = copy.deepcopy(self.turn_vertical(self.figure, _size))

		return self.figure

	def turn_mirror(self, block, _size):
		_block = [[[0 for i in range(_size)] for j in range(_size)]]
		for j in range(_size):
			for i in range(_size):
				_block[0][j][i] = block[0][i][j]
		return _block
	def turn_row(self, block, _size):
		_block = [[[0 for i in range(_size)] for j in range(_size)]]
		for j in range(_size):
			for i in range(_size):
				_block[0][j][i] = block[0][_size - 1 - j][i]
		return _block
	def turn_col(self, block, _size):
		_block = [[[0 for i in range(_size)] for j in range(_size)]]
		for j in range(_size):
			for i in range(_size):
				_block[0][j][i] = block[0][j][_size - 1 - i]
		return _block
	def turn_horizontal(self, block, _size):
		_block = [[[0 for i in range(_size)]] for k in range(_size)]
		for j in range(_size):
			for i in range(_size):
				_block[j][0][i] = block[0][j][i]
		return _block
	def turn_vertical(self, block, _size):
		_block = [[[0] for j in range(_size)] for k in range(_size)]
		for j in range(_size):
			for i in range(_size):
				_block[i][j][0] = block[0][j][i]
		return _block

turn_pattern = {
	'f' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
	'i' : [0],
	'l' : [0, 1, 2, 3, 4, 5, 6, 7, 8,    10,     12,     14,         17,     19,     21,     23],
	'n' : [0, 1, 2, 3, 4, 5, 6, 7, 8,    10,     12,     14,         17,     19,     21,     23],
	'p' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
	't' : [0, 1, 2,       5,       8, 9, 10,         13,         16, 17, 18,         21],
	'u' : [0, 1, 2,       5,       8, 9, 10,         13,         16, 17, 18,         21],
	'v' : [0, 1, 2, 3,             8, 9, 10, 11,                 16, 17, 18, 19],
	'w' : [0, 1, 2, 3,             8, 9, 10, 11,                 16, 17, 18, 19],
	'x' : [0,                      8,                            16],
	'y' : [0, 1, 2, 3, 4, 5, 6, 7, 8,    10,     12,     14,         17,     19,     21,     23],
	'z' : [0, 1, 2, 3,             8, 9, 10, 11,                 16, 17, 18, 19]
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

# make block all pattern before main

def offset_position(_block):
	_offset = [0, 0, 0]
	for k in range(len(_block)):
		for j in range(len(_block[k])):
			for i in range(len(_block[k][j])):
				if _block[k][j][i]:
					_offset[0] = -i
					_offset[1] = -j
					_offset[2] = -k
					return _offset

Blocks_turn_pattern = []

for block in blocks:
	Block_turn_pattern = []
	for turn in turn_pattern[block]:

		piece = Block(block)
		piece = copy.deepcopy(piece.turn(turn))

		offset = copy.deepcopy(offset_position(piece))
		Block_turn_pattern.append([piece, offset])
	Blocks_turn_pattern.append(Block_turn_pattern)


# -------- func --------

def display_cube(_cube):
	for k in range(CUBE_DEPTH):
		for j in range(CUBE_HEIGHT):
			for i in range(CUBE_WITH):
				sys.stdout.write(pullet[_cube[k][j][i]] + "■" + pullet_end)
			sys.stdout.write(" + ")
		sys.stdout.write("\n")

def put_block(_cube, _ptr, _block, _value):
	for k in range(len(_block)):
		for j in range(len(_block[k])):
			for i in range(len(_block[k][j])):
				if _block[k][j][i]:
					_cube[_ptr[2] + k][_ptr[1] + j][_ptr[0] + i] = _value

def move_next(_cube, _ptr):
# return next empty cell
	_next = [0, 0, 0]

	for k in range(_ptr[2], CUBE_DEPTH):
		for j in range(CUBE_HEIGHT):
			for i in range(CUBE_WITH):
				if _cube[k][j][i] == 0:
					_next[0] = i
					_next[1] = j
					_next[2] = k
					return _next

def adjust_position(_ptr, _offset):
# return position that adjust _ptr and block head
	_adjust = [0, 0, 0]
	_adjust[0] = _ptr[0] + _offset[0]
	_adjust[1] = _ptr[1] + _offset[1]
	_adjust[2] = _ptr[2] + _offset[2]
	return _adjust

def can_put_block(_cube, _ptr, _block):
	for k in range(len(_block)):
		for j in range(len(_block[k])):
			for i in range(len(_block[k][j])):
				if _block[k][j][i]:
					# block is over cube
					if _ptr[0] + i < 0 or CUBE_WITH <= _ptr[0] + i:
						return False
					# block is over cube
					if _ptr[1] + j < 0 or CUBE_HEIGHT <= _ptr[1] + j:
						return False
					# block is over cube
					if _ptr[2] + k < 0 or CUBE_DEPTH <= _ptr[2] + k:
						return False
					# block is over another block
					if _cube[_ptr[2] + k][_ptr[1] + j][_ptr[0] + i] <> 0:
						return False
	return True

def island_volume(_cube, _verified, _x, _y, _z):
	_volume = 1
	_verified[_z][_y][_x] = 1

	if 0 < _z and not _verified[_z - 1][_y][_x] and _cube[_z - 1][_y][_x] == 0:
		_volume += island_volume(_cube, _verified, _x, _y, _z - 1)
	if _z < CUBE_DEPTH - 1 and not _verified[_z + 1][_y][_x] and _cube[_z + 1][_y][_x] == 0:
		_volume += island_volume(_cube, _verified, _x, _y, _z + 1)
	if 0 < _y and not _verified[_z][_y - 1][_x] and _cube[_z][_y - 1][_x] == 0:
		_volume += island_volume(_cube, _verified, _x, _y - 1, _z)
	if _y < CUBE_HEIGHT - 1 and not _verified[_z][_y + 1][_x] and _cube[_z][_y + 1][_x] == 0:
		_volume += island_volume(_cube, _verified, _x, _y + 1, _z)
	if 0 < _x and not _verified[_z][_y][_x - 1] and _cube[_z][_y][_x - 1] == 0:
		_volume += island_volume(_cube, _verified, _x - 1, _y, _z)
	if _x < CUBE_WITH - 1 and not _verified[_z][_y][_x + 1] and _cube[_z][_y][_x + 1] == 0:
		_volume += island_volume(_cube, _verified, _x + 1, _y, _z)
	return _volume

def not_have_island(_cube, _ptr):
	_verified = [[[0 for i in range(CUBE_WITH)] for j in range(CUBE_HEIGHT)] for k in range(CUBE_DEPTH)]

	for k in range(_ptr[2], CUBE_DEPTH):
		for j in range(CUBE_HEIGHT):
			for i in range(CUBE_WITH):
				if _cube[k][j][i] == 0 and _verified[k][j][i] == 0:
					if island_volume(_cube, _verified, i, j, k) < 5:
						return False
	return True

def no_more_block(_used):
	return len(_used) == 12

def write_solution(_cube):
	for _layer in _cube:
		writer.writerows(_layer)
	file.write('\n')

def put_piece_recursive(cube, ptr, used):

	for value in range(12):
		if value not in used:
			for turn in Blocks_turn_pattern[value]:
				piece = turn[0]
				offset = turn[1]

				adjust = adjust_position(ptr, offset)
				if can_put_block(cube, adjust, piece):
					_cube = copy.deepcopy(cube)
					_used = copy.deepcopy(used)
					_ptr = [0, 0, 0]

					put_block(_cube, adjust, piece, value + 1)
					_used.append(value)
					if no_more_block(_used):
						display_cube(_cube)
						print('----------------')
						if OUTPUT:
							write_solution(_cube)
					elif not_have_island(_cube, ptr):
						_ptr = move_next(_cube, ptr)
						put_piece_recursive(_cube, _ptr, _used)


# -------- main --------

# init cube

cube = [[[0 for i in range(CUBE_WITH)] for j in range(CUBE_HEIGHT)] for k in range(CUBE_DEPTH)]
ptr = [0, 0, 0]
used = []

put_piece_recursive(cube, ptr, used)

if OUTPUT:
	file.close



