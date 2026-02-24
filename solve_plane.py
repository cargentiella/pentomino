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
        'f' : np.array([[0, 1, 1],
                        [1, 1, 0],
                        [0, 1, 0]]),
        'i' : np.array([[1],
                        [1],
                        [1],
                        [1],
                        [1]]),
        'l' : np.array([[1, 0],
                        [1, 0],
                        [1, 0],
                        [1, 1]]),
        'n' : np.array([[0, 1],
                        [0, 1],
                        [1, 1],
                        [1, 0]]),
        'p' : np.array([[1, 1],
                        [1, 1],
                        [1, 0]]),
        't' : np.array([[1, 1, 1],
                        [0, 1, 0],
                        [0, 1, 0]]),
        'u' : np.array([[1, 0, 1],
                        [1, 1, 1]]),
        'v' : np.array([[1, 0, 0],
                        [1, 0, 0],
                        [1, 1, 1]]),
        'w' : np.array([[1, 0, 0],
                        [1, 1, 0],
                        [0, 1, 1]]),
        'x' : np.array([[0, 1, 0],
                        [1, 1, 1],
                        [0, 1, 0]]),
        'y' : np.array([[0, 1],
                        [1, 1],
                        [0, 1],
                        [0, 1]]),
        'z' : np.array([[1, 1, 0],
                        [0, 1, 0],
                        [0, 1, 1]])
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
        'f' : [0, 1, 2, 3, 4, 5, 6, 7],
        'i' : [0,          4         ],
        'l' : [0, 1, 2, 3, 4, 5, 6, 7],
        'n' : [0, 1, 2, 3, 4, 5, 6, 7],
        'p' : [0, 1, 2, 3, 4, 5, 6, 7],
        't' : [0, 1, 2, 3            ],
        'u' : [0, 1, 2, 3            ],
        'v' : [0, 1, 2, 3            ],
        'w' : [0, 1, 2, 3            ],
        'x' : [0                     ],
        'y' : [0, 1, 2, 3, 4, 5, 6, 7],
        'z' : [0, 1,       4, 5      ]
    }

    # blockの番号割り当て
    def _encode(self, block):
        return np.where(PENTOMINO.blocks == block)[0][0] + 1

    def _head(self, shape):
        y, x = np.where(shape > 0)
        return np.array([y[0], x[0]])

    def _transform(self, shape, t):
        # 反転
        if t // 4 == 1:
            shape = shape.T

        # 回転
        return np.rot90(shape, t % 4)

    # blockの変換パターン作成
    def _create_images(self, width, height):
        self.images = {}

        for block in PENTOMINO.blocks:
            images = []

            for t in PENTOMINO.transformation[block]:
                shape = self._transform(PENTOMINO.shape[block], t)
                h, w = shape.shape

                if w <= width and h <= height:
                    images.append({
                        'shape' : shape * self._encode(block),
                        'head'   : self._head(shape)
                    })

            self.images[block] = images

    def __init__(self, width=60, height=60):
        self._create_images(width, height)


class PLANE:
    def _box_put_a_shape(self, box, ptr, shape):
        h, w = shape.shape

        for y in range(h):
            for x in range(w):
                box[ptr[0] + y][ptr[1] + x] += shape[y, x]

        return box

    def _put_a_block(self, box, blocks):
        y, x = np.where(box < 1)
        ptr = np.array([y[0], x[0]])

        for block in blocks:
            unused = blocks[blocks != block]

            for image in self.pentomino.images[block]:
                h, w = image['shape'].shape
                head = ptr - image['head']

                # imageがboxに収まるかの確認
                if head[1] < 0 or self.width < head[1] + w:
                    continue
                if head[0] < 0 or self.height < head[0] + h:
                    continue

                # imageが既存のblockと重ならないかの確認
                y, x = np.where(image['shape'] > 0)
                for i in range(5):
                    if box[head[0] + y[i], head[1] + x[i]] != 0:
                        break
                else:
                    if len(unused) == 0:
                        self.writer.writerow(self._box_put_a_shape(np.copy(box), ptr - image['head'], image['shape']).flatten())
                    else:
                        self._put_a_block(self._box_put_a_shape(np.copy(box), ptr - image['head'], image['shape']), unused)

    # 器の作成（長方形）
    def create_box_rectangle(self, width, height):
        self.box = np.zeros((height, width), dtype=int)

    # 器の作成（正方形、8x8のみ）
    def create_box_square(self):
        self.box = np.zeros((8, 8), dtype=int)
        for w in range(3, 5):
            for h in range(3, 5):
                self.box[h][w] = BLANK

    def _is_box_size_60(self):
        return len(np.where(self.box < 1)[0]) == 60

    def _measure_box_size(self):
        self.height, self.width = self.box.shape

    def solve(self, file):
        if not self._is_box_size_60():
            logger.error("BOXのサイズが60に合致しません。")
            return False

        self._measure_box_size()
        self.pentomino = PENTOMINO(self.width, self.height)

        with open(file, 'w', encoding='utf-8') as f:
            self.writer = csv.writer(f, delimiter=',', lineterminator='\n')
            self._put_a_block(self.box, self.pentomino.blocks)
            return True

    def __enter__(self):
        return self

    def __init__(self):
        self.file = ""
        self.box = np.empty([0, 0])

    def __exit__(self, ex_type, ex_value, trace):
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Solve a pentomino 2D puzzle',
    )
    subparsers = parser.add_subparsers(help='sub-command help', required=True)
    parser_rectangle = subparsers.add_parser('rectangle', help='rectangle help')
    parser_rectangle.set_defaults(shape='rectangle')
    parser_rectangle.add_argument('width', type=int)
    parser_rectangle.add_argument('height', type=int)
    parser_square = subparsers.add_parser('square', help='square help')
    parser_square.set_defaults(shape='square')
    args = parser.parse_args()

    with PLANE() as plane:
        if args.shape == 'rectangle':
            file = "plane_rectangle_" + str(args.width) + "x" + str(args.height) + ".txt"
            plane.create_box_rectangle(args.width, args.height)
        elif args.shape == 'square':
            file = "plane_square_8x8.txt"
            plane.create_box_square()

        plane.solve(file)
