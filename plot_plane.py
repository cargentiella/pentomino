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


class PLANE:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def plot(self, solution, file):
        colors = np.empty((self.height * self.width), dtype=object)
        for h in range(self.height):
            for w in range(self.width):
                if solution[h * self.width + w] != BLANK:
                    colors[h * self.width + w] = PALLET[int(solution[h * self.width + w]) - 1]

        voxelarray = colors.reshape(self.height, self.width, 1)

        ax = plt.figure(figsize=(2.0, 2.0), linewidth=0).add_subplot(projection='3d')
        ax.voxels(voxelarray, facecolors=voxelarray, edgecolor='k')
        ax.set_xlim(0, self.height)
        ax.set_ylim(0, self.width)
        ax.set_aspect('equal')
        plt.axis('off')
        plt.savefig(file, pad_inches=0)
        plt.close()


def plot_plane(file, width, height):
    plane = PLANE(width, height)

    directory = os.path.splitext(file)[0]
    try:
        os.makedirs(directory)
    except FileExistsError:
        pass

    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        for count, solution in enumerate(reader):
            image = ("0000000" + str(count) + ".jpg")[-10:]
            plane.plot(solution, os.path.join(directory, image))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Plot a pentomino 2D puzzle',
    )
    parser.add_argument('file')
    parser.add_argument('width', type=int)
    parser.add_argument('height', type=int)
    args = parser.parse_args()

    plot_plane(args.file, args.width, args.height)
