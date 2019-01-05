# coding: utf-8
import sys

# -------- init --------

case_with = 6
case_height = 10

blocks = ['i', 'l', 'n', 'y', 'f', 'p', 't', 'u', 'v', 'w', 'x', 'z']
	
block = {
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
	'y' : [	[1, 1, 1, 1],
		[0, 1, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0]	],
	'f' : [	[0, 1, 1],
		[1, 1, 0],
		[0, 1, 0]	],
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
		[1, 0, 0],
		[1, 0, 0]	],
	'w' : [	[1, 1, 0],
		[0, 1, 1],
		[0, 0, 1]	],
	'x' : [	[0, 1, 0],
		[1, 1, 1],
		[0, 1, 0]	],
	'z' : [	[1, 1, 0],
		[0, 1, 0],
		[0, 1, 1]	]
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

def put_block(case, locate, block, color):
	for j in range(len(block)):
		for i in range(len(block[j])):
			if block[j][i]:
				case[locate['y'] + j][locate['x'] + i] = color
	return case


# -------- main --------

locate = {
	'x' : 0,
	'y' : 0
}

case = [[pullet['EMPTY'] for i in range(case_with)] for j in range(case_height)]

caset = put_block(case, locate, block['v'], pullet['v'])



display_case(case)


