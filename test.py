# coding: utf-8
import sys

# -------- init --------

class cell:
	EMPTY = '\033[30m'
	FRAME = '\033[37m'
	END = '\033[0m'


case_with = 6
case_height = 10



# -------- func --------

def display_case(case):
        for j in range(case_height + 2):
                for i in range(case_with + 2):
                        sys.stdout.write(case[j][i] + "■" + cell.END)
		sys.stdout.write("\n")

# -------- main --------


case = [[cell.EMPTY for i in range(case_with + 2)] for j in range(case_height + 2)]

for i in range(case_with + 2):
	case[0][i] = cell.FRAME
	case[case_height + 1][i] = cell.FRAME

for j in range(case_height):
	case[j + 1][0] = cell.FRAME
	case[j + 1][case_with + 1] = cell.FRAME




#print(case)
display_case(case)


