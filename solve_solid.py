# -*- coding: utf-8 -*-
import argparse
import csv
import logging
import numpy as np


logger = logging.getLogger(__name__)


BLANK = 13

class PENTOMINO:
    # blockの種類
    blocks = np.array(['f', 'i', 'l', 'n', 'p', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

    # blockの形
    shape = {
        'f' : np.array([[[0, 1, 1],
                        [1, 1, 0],
                        [0, 1, 0]]]),
        'i' : np.array([[[1],
                        [1],
                        [1],
                        [1],
                        [1]]]),
        'l' : np.array([[[1, 0],
                        [1, 0],
                        [1, 0],
                        [1, 1]]]),
        'n' : np.array([[[0, 1],
                        [0, 1],
                        [1, 1],
                        [1, 0]]]),
        'p' : np.array([[[1, 1],
                        [1, 1],
                        [1, 0]]]),
        't' : np.array([[[1, 1, 1],
                        [0, 1, 0],
                        [0, 1, 0]]]),
        'u' : np.array([[[1, 0, 1],
                        [1, 1, 1]]]),
        'v' : np.array([[[1, 0, 0],
                        [1, 0, 0],
                        [1, 1, 1]]]),
        'w' : np.array([[[1, 0, 0],
                        [1, 1, 0],
                        [0, 1, 1]]]),
        'x' : np.array([[[0, 1, 0],
                        [1, 1, 1],
                        [0, 1, 0]]]),
        'y' : np.array([[[0, 1],
                        [1, 1],
                        [0, 1],
                        [0, 1]]]),
        'z' : np.array([[[1, 1, 0],
                        [0, 1, 0],
                        [0, 1, 1]]])
    }

    # blockの回転・反転パターン
    #   反転: 4で割った商で判定
    #     0 : 反転なし
    #     1 : 反転あり
    #   回転: 4で割った余で判定
    #     0 : 回転なし
    #     1 : 回転 90度
    #     2 : 回転180度
    #     3 : 回転270度
    transformation = {
        'f' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        'i' : [0,          4,          8                                                           ],
        'l' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        'n' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        'p' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        't' : [0, 1, 2, 3,             8, 9, 10, 11,                 16, 17, 18, 19                ],
        'u' : [0, 1, 2, 3,             8, 9, 10, 11,                 16, 17, 18, 19                ],
        'v' : [0, 1, 2, 3,             8, 9, 10, 11,                 16, 17, 18, 19                ],
        'w' : [0, 1, 2, 3,             8, 9, 10, 11,                 16, 17, 18, 19                ],
        'x' : [0,                      8,                            16                            ],
        'y' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        'z' : [0, 1,       4, 5,       8, 9,         12, 13,         16, 17,         20, 21        ]
    }

    # blockの番号割り当て
    def _encode(self, block):
        return np.where(PENTOMINO.blocks == block)[0][0] + 1

    def _head(self, shape):
        z, y, x = np.where(shape > 0)
        return np.array([z[0], y[0], x[0]])

    def _transform(self, shape, t):
        # 反転
        if t // 4 % 2 == 1:
            shape = shape.transpose(0, 2, 1)

        # 回転
        shape = np.rot90(shape, t % 4, axes=(1, 2))

        # 平面変換(デフォルトはXY平面)
        if t // 8 == 1: # YZ平面
            shape = np.rot90(shape, axes=(0, 1))
        elif t // 8 == 2: # ZX平面
            shape = np.rot90(shape, axes=(2, 0))

        return shape

    # blockの変換パターン作成
    def _create_images(self, width, height, depth):
        self.images = {}

        for block in PENTOMINO.blocks:
            images = []

            for t in PENTOMINO.transformation[block]:
                shape = self._transform(PENTOMINO.shape[block], t)
                d, h, w = shape.shape

                if w <= width and h <= height and d <= depth:
                    images.append({
                        'shape' : shape * self._encode(block),
                        'head'   : self._head(shape)
                    })

            self.images[block] = images

    def __init__(self, width=60, height=60, depth=60):
        self._create_images(width, height, depth)


class SOLID:
    def _box_put_a_shape(self, box, ptr, shape):
        d, h, w = shape.shape

        for z in range(d):
            for y in range(h):
                for x in range(w):
                    box[ptr[0] + z][ptr[1] + y][ptr[2] + x] += shape[z, y, x]

        return box

    def _put_a_block(self, box, blocks):
        z, y, x = np.where(box < 1)
        ptr = np.array([z[0], y[0], x[0]])

        for block in blocks:
            unused = blocks[blocks != block]

            for image in self.pentomino.images[block]:
                d, h, w = image['shape'].shape
                head = ptr - image['head']

                # imageがboxに収まるかの確認
                if head[2] < 0 or self.width < head[2] + w:
                    continue
                if head[1] < 0 or self.height < head[1] + h:
                    continue
                if head[0] < 0 or self.depth < head[0] + d:
                    continue

                # imageが既存のblockと重ならないかの確認
                z, y, x = np.where(image['shape'] > 0)
                for i in range(5):
                    if box[head[0] + z[i], head[1] + y[i], head[2] + x[i]] != 0:
                        break
                else:
                    if len(unused) == 0:
                        self.writer.writerow(self._box_put_a_shape(np.copy(box), ptr - image['head'], image['shape']).flatten())
                    else:
                        self._put_a_block(self._box_put_a_shape(np.copy(box), ptr - image['head'], image['shape']), unused)

    # 器の作成（直方体）
    def create_box_rectangular(self, width, height, depth):
        self.box = np.zeros((depth, height, width), dtype=int)

    # 器の作成（中空）
    def create_box_hollow(self, width, height, depth):
        self.box = np.zeros((depth, height, width), dtype=int)
        for d in range(1, depth - 1):
            for h in range(1, height - 1):
                for w in range(width):
                    self.box[d][h][w] = BLANK

    def create_box_farfalle(self):
        self.box = np.zeros((3, 3, 7), dtype=int)
        for w in range(width):
            self.box[3][1][w] = BLANK

    # 器の作成（階段）
    def create_box_stairs(self, width, height, depth):
        self.box = np.zeros((depth, height, width), dtype=int)
        for d in range(depth):
            for h in range(height):
                if d + h >= depth:
                    for w in range(width):
                        self.box[d][h][w] = BLANK

    def _is_box_size_60(self):
        return len(np.where(self.box < 1)[0]) == 60

    def _measure_box_size(self):
        self.depth, self.height, self.width = self.box.shape

    def solve(self, file):
        if not self._is_box_size_60():
            logger.error("BOXのサイズが60に合致しません。")
            return False

        self._measure_box_size()
        self.pentomino = PENTOMINO(self.width, self.height, self.depth)

        with open(file, 'w', encoding='utf-8') as f:
            self.writer = csv.writer(f, delimiter=',', lineterminator='\n')
            self._put_a_block(self.box, self.pentomino.blocks)
            return True

    def __enter__(self):
        return self

    def __init__(self):
        self.file = ""
        self.box = np.empty([0, 0, 0])

    def __exit__(self, ex_type, ex_value, trace):
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Solve a pentomino 3D puzzle',
    )
    subparsers = parser.add_subparsers(help='sub-command help', required=True)
    parser_rectangular = subparsers.add_parser('rectangular', help='rectangular help')
    parser_rectangular.set_defaults(shape='rectangular')
    parser_rectangular.add_argument('width', type=int)
    parser_rectangular.add_argument('height', type=int)
    parser_rectangular.add_argument('depth', type=int)
    parser_hollow = subparsers.add_parser('hollow', help='hollow help')
    parser_hollow.set_defaults(shape='hollow')
    parser_hollow.add_argument('width', type=int)
    parser_hollow.add_argument('height', type=int)
    parser_hollow.add_argument('depth', type=int)
    parser_farfalle = subparsers.add_parser('farfalle', help='farfalle help')
    parser_farfalle.set_defaults(shape='farfalle')
    parser_stairs = subparsers.add_parser('stairs', help='stairs help')
    parser_stairs.set_defaults(shape='stairs')
    parser_stairs.add_argument('width', type=int)
    parser_stairs.add_argument('height', type=int)
    parser_stairs.add_argument('depth', type=int)
    args = parser.parse_args()


    with SOLID() as solid:
        if args.shape == 'rectangular':
            file = "solid_rectangular_" + str(args.width) + "x" + str(args.height) + "x" + str(args.depth) + ".txt"
            solid.create_box_rectangular(args.width, args.height, args.depth)
        elif args.shape == 'hollow':
            file = "solid_hollow_" + str(args.width) + "x" + str(args.height) + "x" + str(args.depth) + ".txt"
            solid.create_box_hollow(args.width, args.height, args.depth)
        elif args.shape == 'farfalle':
            file = "solid_farfalle_3x3x7.txt"
            solid.create_box_farfalle()
        elif args.shape == 'stairs':
            file = "solid_stairs_" + str(args.width) + "x" + str(args.height) + "x" + str(args.depth) + ".txt"
            solid.create_box_stairs(args.width, args.height, args.depth)

        solid.solve(file)
