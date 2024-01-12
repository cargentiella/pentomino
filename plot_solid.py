# -*- coding: utf-8 -*-
import argparse
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
from mpl_toolkits.mplot3d import axes3d, Axes3D


BLANK = '13'

PALLET = [
    '#ffdc00', # f: yellow
    '#e95464', # i: rose
    '#7f1184', # l: royal purple
    '#00885a', # n: viridian
    '#00a1e9', # p: cyan
    '#9a0d7c', # t: framboise
    '#00afcc', # u: turquoise blue
    '#d70035', # v: carmine
    '#ee7800', # w: orange
    '#f39800', # x: marigold
    '#fcc800', # y: chrome yellow
    '#9cbb1c', # z: spring green
]


class SOLID:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth

        self.span  = 3
#        if width == 3:
#            self.span  = 3

    def plot(self, solution, file):
        colors = np.empty(self.depth * self.height * ((self.width - 1) * self.span + 1), dtype=object)
        for d in range(self.depth):
            for h in range(self.height):
                for w in range(self.width):
                    if solution[d * self.height * self.width + h * self.width + w] != BLANK:
                        colors[d * self.height * ((self.width -1) * self.span + 1) + h * ((self.width - 1) * self.span + 1) + w * self.span] = PALLET[int(solution[d * self.height * self.width + h * self.width + w]) - 1]

        voxelarray = colors.reshape(self.depth, self.height, ((self.width - 1) * self.span + 1))

        ax = plt.figure(figsize=(2.0, 2.0), linewidth=0).add_subplot(projection='3d')
        ax.voxels(voxelarray, facecolors=voxelarray, edgecolor='k')
        ax.set_xlim(0, self.depth)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')
        plt.axis('off')
        plt.savefig(file, pad_inches=0)
        plt.close()


def plot_solid(file, width, height, depth):
    solid = SOLID(width, height, depth)

    directory = os.path.splitext(file)[0]
    try:
        os.makedirs(directory)
    except FileExistsError:
        pass

    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        for count, solution in enumerate(reader):
            image = ("0000000" + str(count) + ".jpg")[-10:]
            solid.plot(solution, os.path.join(directory, image))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Plot a pentomino 3D puzzle',
    )
    parser.add_argument('file')
    parser.add_argument('width', type=int)
    parser.add_argument('height', type=int)
    parser.add_argument('depth', type=int)
    args = parser.parse_args()

    plot_solid(args.file, args.width, args.height, args.depth)
