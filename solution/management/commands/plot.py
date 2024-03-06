import base64
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
from ._Logger import set_logger
from django.core.management.base import BaseCommand
from io import BytesIO
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

SHAPE = {
    'plane': {
        'rectangle': ['3x20', '4x15', '5x12', '6x10'],
        'square': ['8x8'],
    },
    'solid': {
        'rectangular': ['2x3x10', '2x5x6', '3x4x5'],
        'hollow': ['3x3x9', '3x5x7', '5x3x5'],
        'stairs': ['6x4x4'],
    },
}

_logger = set_logger(__name__)


class SOLID:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth

        self.span  = 3
#        if width == 3:
#            self.span  = 3

    def _create_graph(self, solution, figsize):
        colors = np.empty(self.depth * self.height * ((self.width - 1) * self.span + 1), dtype=object)
        for d in range(self.depth):
            for h in range(self.height):
                for w in range(self.width):
                    if solution[d * self.height * self.width + h * self.width + w] != BLANK:
                        colors[d * self.height * ((self.width -1) * self.span + 1) + h * ((self.width - 1) * self.span + 1) + w * self.span] = PALLET[int(solution[d * self.height * self.width + h * self.width + w]) - 1]

        voxelarray = colors.reshape(self.depth, self.height, ((self.width - 1) * self.span + 1))
        plt.cla()
        ax = plt.figure(figsize=figsize, linewidth=0).add_subplot(projection='3d')
        ax.voxels(voxelarray, facecolors=voxelarray, edgecolor='k')
        ax.set_xlim(0, self.depth)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')
        plt.axis('off')

    def save(self, solution, file):
        figsize = (2.0, 2.0)
        self._create_graph(solution, figsize)

        plt.savefig(file, pad_inches=0)
        plt.close()

    def image(self, solution):
        figsize = (4.0, 4.0)
        self._create_graph(solution, figsize)

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image = buffer.getvalue()
        graph = base64.b64encode(image)
        graph = graph.decode("utf-8")
        buffer.close()

        return graph


class SOLUTION:
    def __init__(self, dimension, type, width, height, depth=None):
        if depth:
            size = width + 'x' + height + 'x' + depth
        else:
            size = width + 'x' + height

        if size not in SHAPE[dimension][type]:
            _logger.error('size not in shape')
            self.file = None

        self.file = dimension + '_' + type + '_' + size + '.txt'

    def get(self, line):
        try:
            with open(self.file, 'r') as f:
                if line > 0:
                    for _ in range(line - 1):
                        next(f)

                return f.readline().strip().split(',')

        except Exception as e:
            _logger.error(e)
            return [1] * 60


class Command(BaseCommand):
    help = 'Plot a pentomino 2D or 3D puzzle'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
        parser.add_argument('width', type=int)
        parser.add_argument('height', type=int)
        parser.add_argument('depth', type=int, default=1)

    def handle(self, *args, **options):
        pass
#        download(options['url'], null, options['author'])


#
#if __name__ == '__main__':
#    parser = argparse.ArgumentParser(
#        description='Plot a pentomino 3D puzzle',
#    )
#    parser.add_argument('file')
#    parser.add_argument('width', type=int)
#    parser.add_argument('height', type=int)
#    parser.add_argument('depth', type=int)
#    args = parser.parse_args()
#
#    plot_solid(args.file, args.width, args.height, args.depth)
#
#
