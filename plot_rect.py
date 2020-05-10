# -*- coding: utf-8 -*-
#
# require:
#   pip install matplotlib
#
import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d, Axes3D


PALLET = ['#ffdc00', '#ea5550', '#7f1184', '#00a960', '#008db7', '#a50082', '#00afcc', '#d70035', '#ee7800', '#f39800', '#fff352', '#00885a']


class PLOT:
	def __init__(self, width, height):
		if width == 3:
			self.width = width
			self.height = height

			self.min_x = 3
			self.min_y = 0
			self.min_z = -7
			self.range = 11

		elif width == 4:
			self.width = width
			self.height = height

			self.min_x = 2
			self.min_y = 0
			self.min_z = -6
			self.range = 9

		elif width == 6:
			self.width = width
			self.height = height

			self.min_x = 2
			self.min_y = 0
			self.min_z = -3
			self.range = 7


	def plot(self, solution, file):
		colored = np.empty((60,), dtype=object)
		for i in range(60):
			colored[i] = PALLET[int(solution[i]) - 1]

		cube = colored.reshape(self.height, self.width, 1)
		fig = plt.figure(figsize=(2.0, 2.0), linewidth=0)
		ax = fig.gca(projection='3d')
		ax.voxels(cube, facecolors=cube, edgecolor='k')

		ax.set_xlim(self.min_x, self.min_x + self.range)
		ax.set_ylim(self.min_y, self.min_y + self.range)
		ax.set_zlim(self.min_z, self.min_z + self.range)
		plt.axis('off')

		fig.savefig(file, pad_inches=0.0)


def plot_rects(file, width, height):

	plot = PLOT(width, height)

	directory = str(width) + "x" + str(height)
	try:
		os.makedirs(directory)
	except FileExistsError:
		pass

	with open(file, 'r', encoding='utf-8') as f:
		reader = csv.reader(f)

		i = 1
		for line in reader:
			img = ("0000000" + str(i) + ".jpg")[-10:]
			plot.plot(line, os.path.join(directory, img))
			i += 1


# -------- main --------

if __name__ == '__main__':

	usage = 'Usage: python plot_rect [file] [width] [height]'

	args = sys.argv
	if len(args) == 4:
		file  = args[1]
		width  = int(args[2])
		height = int(args[3])

		plot_rects(file, width, height)

	else:
		print(usage)


