# coding: utf-8
import sys
import os
import copy
import csv


# -------- init --------

args = sys.argv
if len(args) != 2:
	print('ERROR : missing operand')
path = args[1]
if not os.path.exists(path):
	print('ERROR : file not exists')

CUBE_WITH = 5
CUBE_HEIGHT = 4
CUBE_DEPTH = 3

pullet_end = '\033[0m'

pullet = [	'\033[30m', '\033[33m', '\033[31m', '\033[35m',
		'\033[32m', '\033[36m', '\033[35m', '\033[36m',
		'\033[31m', '\033[37m', '\033[37m', '\033[33m',
		'\033[32m'
]


# -------- func --------

def display_cube(_line):
        for k in range(CUBE_DEPTH):
		for j in range(CUBE_HEIGHT):
			for i in range(CUBE_WITH):
				sys.stdout.write(pullet[int(_line[k * CUBE_HEIGHT * CUBE_WITH + j * CUBE_WITH + i])] + "■" + pullet_end)
			sys.stdout.write(" + ")
		sys.stdout.write("\n")


# -------- main --------

file = open(path, 'r')
reader = csv.reader(file)

for line in reader:
	display_cube(line)
	print('------------')
	
file.close


