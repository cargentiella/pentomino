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

BOX_WITH = 6
BOX_HEIGHT = 10

pullet_end = '\033[0m'

pullet = [	'\033[30m', '\033[33m', '\033[31m', '\033[35m',
		'\033[32m', '\033[36m', '\033[35m', '\033[36m',
		'\033[31m', '\033[37m', '\033[37m', '\033[33m',
		'\033[32m'
]


# -------- func --------

def display_box(_line):
        for j in range(BOX_HEIGHT):
                for i in range(BOX_WITH):
			sys.stdout.write(pullet[int(_line[j * BOX_WITH + i])] + "■" + pullet_end)
		sys.stdout.write("\n")


# -------- main --------

file = open(path, 'r')
reader = csv.reader(file)

for line in reader:
	display_box(line)
	print('------------')
	
file.close


