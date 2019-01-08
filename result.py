# coding: utf-8
import sys
import copy

# -------- init --------

CASE_WITH = 6
CASE_HEIGHT = 10

class Position:
	x = 0
	y = 0

blocks = ['f', 'i', 'l', 'n', 'p', 't', 'u', 'v', 'w', 'x', 'y', 'z']

block_figure = {
	'f' : [	[0, 1, 1, 0, 0],
		[1, 1, 0, 0, 0],
		[0, 1, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	],
	'i' : [	[1, 1, 1, 1, 1], 
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	],
	'l' : [	[1, 1, 1, 1, 0],
		[1, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	],
	'n' : [	[0, 1, 1, 1, 0],
		[1, 1, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	],
	'p' : [	[1, 1, 1, 0, 0],
		[1, 1, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	],
	't' : [	[1, 1, 1, 0, 0],
		[0, 1, 0, 0, 0],
		[0, 1, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	],
	'u' : [	[1, 1, 1, 0, 0],
		[1, 0, 1, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	],
	'v' : [	[1, 1, 1, 0, 0],
		[0, 0, 1, 0, 0],
		[0, 0, 1, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	],
	'w' : [	[1, 1, 0, 0, 0],
		[0, 1, 1, 0, 0],
		[0, 0, 1, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	],
	'x' : [	[0, 1, 0, 0, 0],
		[1, 1, 1, 0, 0],
		[0, 1, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	],
	'y' : [	[1, 1, 1, 1, 0],
		[0, 1, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	],
	'z' : [	[1, 1, 0, 0, 0],
		[0, 1, 0, 0, 0],
		[0, 1, 1, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	]
}

class Block:
	def __init__(self, type):
		self.figure = [[0 for i in range(5)] for j in range(5)]
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
		_block = [[0 for i in range(5)] for j in range(5)]
		for j in range(5):
			for i in range(5):
				_block[j][i] = block[i][j]
		return _block
	def turn_row(self, block):
		_block = [[0 for i in range(5)] for j in range(5)]
		for j in range(5):
			for i in range(5):
				_block[j][i] = block[4 - j][i]
		return _block
	def turn_col(self, block):
		_block = [[0 for i in range(5)] for j in range(5)]
		for j in range(5):
			for i in range(5):
				_block[j][i] = block[j][4 - i]
		return _block


pattern = {
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

cell_value = {
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
	'TMP' : 13,
}

pullet_end = '\033[0m'

pullet = [	'\033[30m', '\033[33m', '\033[31m', '\033[35m',
		'\033[32m', '\033[36m', '\033[35m', '\033[36m',
		'\033[31m', '\033[37m', '\033[37m', '\033[33m',
		'\033[32m', '\033[34m'
]


# -------- func --------

def display_case(_case):
        for j in range(CASE_HEIGHT):
                for i in range(CASE_WITH):
                        sys.stdout.write(pullet[case[j][i]] + "■" + pullet_end)
		sys.stdout.write("\n")

def put_block(_case, _ptr, _block, _value):
	for j in range(len(_block)):
		for i in range(len(_block[j])):
			if _block[j][i]:
				_case[_ptr.y + j][_ptr.x + i] = _value

def move_next(_case, _ptr):
# return next empty cell
	_next = Position

	for j in range(_ptr.y, CASE_HEIGHT):
		for i in range(CASE_WITH):
			if _case[j][i] <> 0:
				_next.x = i
				_next.y = j
				return _next

def adjust_positioning(_case, _ptr, _block):
# return position that adjust _ptr and block head
	_adjust = Position

	for j in range(len(_block)):
		for i in range(len(_block[j])):
			if _block[j][i]:
				_adjust.x = _ptr.x - i
				_adjust.y = _ptr.y - j
				return _adjust

def can_put_block(_case, _ptr, _block):
	for j in range(len(_block)):
		for i in range(len(_block[j])):
			if _block[j][i]:
				# block is over case
				if _ptr.x + i < 0 or CASE_WITH <= _ptr.x:
					return False
				# block is over case
				if _ptr.y + j < 0 or CASE_HEIGHT < _ptr.y:
					return False
				# block is over another block
				if _case[_ptr.y + j][_ptr.x + i] <> 0:
					return False
	return True

def island_area(_case, _verified, _x, _y):
	_area = 1
	_verified[_y][_x] = 1

	if 0 < _y and not _verified[_y - 1][_x] and _case[_y - 1][_x] == 0:
		_area += island_area(_case, _verified, _x, _y - 1)
	if _y < CASE_HEIGHT - 1 and not _verified[_y + 1][_x] and _case[_y + 1][_x] == 0:
		_area += island_area(_case, _verified, _x, _y + 1)		
	if 0 < _x and not _verified[_y][_x - 1] and _case[_y][_x - 1] == 0:
		_area += island_area(_case, _verified, _x - 1, _y)
	if _x < CASE_WITH - 1 and not _verified[_y][_x + 1] and _case[_y][_x + 1] == 0:
		_area += island_area(_case, _verified, _x + 1, _y)
	return _area

def not_have_island(_case, _ptr):
	_verified = [[0 for i in range(CASE_WITH)] for j in range(CASE_HEIGHT)]

	for j in range(_ptr.y, CASE_HEIGHT):
		for i in range(CASE_WITH):
			if _case[j][i] == 0 and _verified[j][i] == 0:
				if island_area(_case, _verified, i, j) < 5:
					return False
	return True



#def trun_block(block, type):
	



# -------- main --------

current = Position
adjust = Position
blk = [[0 for i in range(5)] for j in range(5)]

# init case
case = [[0 for i in range(CASE_WITH)] for j in range(CASE_HEIGHT)]


# test put
blk = copy.deepcopy(Block('i'))

#print(blk.turn(0))

character = 'n'

for c in range(len(pattern[character])):
	current.x = 0
	current.y = 0
	case = [[0 for i in range(CASE_WITH)] for j in range(CASE_HEIGHT)]
	blk = copy.deepcopy(Block(character))
	blk = copy.deepcopy(blk.turn(pattern[character][c]))
	put_block(case, current, blk, cell_value[character])
	display_case(case)

	print(not_have_island(case, current))

#put_block(case, current, blk, pullet['w'])

# search next position
#current = move_next(case, current)
#adjust = adjust_positioning(case, current, block['u'])

#if can_put_block(case, adjust, block['u']):
#	put_block(case, adjust, block['u'], pullet['u'])

#put_block(case, block['f'], pullet['f'])

#display_case(case)
#print(ptr)


