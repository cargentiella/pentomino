# coding: utf-8
import sys
import copy

# -------- init --------

case_with = 6
case_height = 10

class Position:
	x = 0
	y = 0

blocks = ['i', 'l', 'n', 'y', 'f', 'p', 't', 'u', 'v', 'w', 'x', 'z']

origin = {
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
	'y' : [	[1, 1, 1, 1, 0],
		[0, 1, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	],
	'f' : [	[0, 1, 1, 0, 0],
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
	'z' : [	[1, 1, 0, 0, 0],
		[0, 1, 0, 0, 0],
		[0, 1, 1, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]	]
}

class Block:
	def __init__(self, type):
		self.figure = [[0 for i in range(5)] for j in range(5)]
		self.figure = copy.deepcopy(origin[type])

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
	'i' : [0, 1],
	'l' : [0, 1],
	'n' : ,
	'y' : ,
	'f' : ,
	'p' : ,
	't' : ,
	'u' : ,
	'v' : ,
	'w' : ,
	'x' : ,
	'z' : 
}

pullet = {
	'EMPTY' : '\033[30m',
	'i' : '\033[31m',
	'l' : '\033[35m',
	'n' : '\033[32m',
	'y' : '\033[37m',
	'f' : '\033[37m',
	'p' : '\033[36m',
	't' : '\033[35m',
	'u' : '\033[36m',
	'v' : '\033[31m',
	'w' : '\033[33m',
	'x' : '\033[33m',
	'z' : '\033[32m',
	'END' : '\033[0m'
}


# -------- func --------

def display_case(case):
        for j in range(case_height):
                for i in range(case_with):
                        sys.stdout.write(case[j][i] + "■" + pullet['END'])
		sys.stdout.write("\n")

def put_block(case, ptr, block, color):
	for j in range(len(block)):
		for i in range(len(block[j])):
			if block[j][i]:
				case[ptr.y + j][ptr.x + i] = color
	return case

def move_next(case, ptr):
	next = Position

	for j in range(ptr.y, len(case)):
		for i in range(len(case[j])):
			if case[j][i] == pullet['EMPTY']:
				next.x = i
				next.y = j
				return next

def tryon_positioning(case, ptr, block):
	temp = Position

	for j in range(len(block)):
		for i in range(len(block[j])):
			if block[j][i]:
				tryon.x = ptr.x - i
				tryon.y = ptr.y - j
				return temp

def can_put_block(case, ptr, block):
	for j in range(len(block)):
		for i in range(len(block[j])):
			if block[j][i]:
				# block is over case
				if ptr.x + i < 0 or case_with <= ptr.x:
					return False
				if ptr.y + j < 0 or case_height < ptr.y:
					return False
				if case[ptr.y + j][ptr.x + i] <> pullet['EMPTY']:
					return False
	return True

#def trun_block(block, type):
	



# -------- main --------

current = Position
tryon = Position
blk = [[0 for i in range(5)] for j in range(5)]

# init case
case = [[pullet['EMPTY'] for i in range(case_with)] for j in range(case_height)]


# test put
blk = copy.deepcopy(Block('i'))

print(blk.turn(0))

#put_block(case, current, blk, pullet['i'])

# search next position
#current = move_next(case, current)
#tryon = tryon_positioning(case, current, block['u'])

#if can_put_block(case, tryon, block['u']):
#	put_block(case, tryon, block['u'], pullet['u'])

#put_block(case, block['f'], pullet['f'])

#display_case(case)
#print(ptr)


