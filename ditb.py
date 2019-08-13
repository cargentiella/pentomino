import numpy as np


class DITB:

    width = 4
    height = 5

    boad = np.zeros((width, height), dtype = 'int8')
    
    blocks = [
        {
            'ptr' : np.array([[1, 1], [1, 1]]),
            'pos' : np.array([1, 0])
        }, # ñ∫ DA
        {
            'ptr' : np.array([[1], [1]]),
            'pos' : np.array([0, 0])
        }, # ïÉ FA
        {
            'ptr' : np.array([[1], [1]]),
            'pos' : np.array([3, 0])
        }, # ïÍ MO
        {
            'ptr' : np.array([[1], [1]]),
            'pos' : np.array([0, 2])
        }, # ëcïÉ GF
        {
            'ptr' : np.array([[1], [1]]),
            'pos' : np.array([3, 2])
        }, # ëcïÍ GM
        {
            'ptr' : np.array([[1, 1]]),
            'pos' : np.array([1, 2])
        }, # åZíÌ BR
        {
            'ptr' : np.array([[1]]),
            'pos' : np.array([0, 4])
        }, # òaçŸ SE
        {
            'ptr' : np.array([[1]]),
            'pos' : np.array([1, 3])
        }, # âÿìπ FL
        {
            'ptr' : np.array([[1]]),
            'pos' : np.array([2, 3])
        }, # íÉìπ TE
        {
            'ptr' : np.array([[1]]),
            'pos' : np.array([3, 4])
        }  # èëìπ CA
    ]

    _blank = -1
    blanks = [
        np.array([1, 4]),
        np.array([2, 4])
    ]


    def __init__(self):
        for block_number in range(len(self.blocks)):
            block = self.blocks[block_number]
            for j in range(block['ptr'].shape[0]):
                for i in range(block['ptr'].shape[1]):
                    self.boad[block['pos'][0] + i, block['pos'][1] + j] = block['ptr'][j][i] * block_number
        for blank_number in range(len(self.blanks)):
            blank = self.blanks[blank_number]
            self.boad[blank[0], blank[1]] = blank_number - 2


    def show(self):
        for j in range(5):
            for i in range(4):
                print(self.boad[i, j], end="")
                print('\t', end="")
            print('\n', end="")
        
    def finished(self):
        return self.blocks[0].pos == [1, 3]


    def movable_left(self):
        blocks = []
        for blank in self.blanks:
            if not self.__right_edge(blank):
                target_block = self.__right_side(blank)
                block_number = self.boad[target_block[0], target_block[1]]
                if not self.__is_blank(block_number):
                    blocks.append(block_number)
        return blocks

    def movable_right(self):
        blocks = []
        for blank in self.blanks:
            if not self.__left_edge(blank):
                target_block = self.__left_side(blank)
                block_number = self.boad[target_block[0], target_block[1]]
                if not self.__is_blank(block_number):
                    blocks.append(block_number)
        return blocks

    def movable_up(self):
        blocks = []
        for blank in self.blanks:
            if not self.__down_edge(blank):
                target_block = self.__down_side(blank)
                block_number = self.boad[target_block[0], target_block[1]]
                if not self.__is_blank(block_number):
                    blocks.append(block_number)
        return blocks

    def movable_down(self):
        blocks = []
        for blank in self.blanks:
            if not self.__up_edge(blank):
                target_block = self.__up_side(blank)
                block_number = self.boad[target_block[0], target_block[1]]
                if not self.__is_blank(block_number):
                    blocks.append(block_number)
        return blocks


    def move_left(self, block_number):
        block = self.blocks[block_number]

        if self.__left_edge(block['pos']):
            print('edge')
            return False
        
        for j in range(block['ptr'].shape[0]):
            print(self.boad[block['pos'][0] - 1, block['pos'][1] + j])
            if not self.__is_blank(self.boad[block['pos'][0] - 1, block['pos'][1] + j]):
                print('not blank')
                return False
        
        for j in range(block['ptr'].shape[0]):
            self.boad[block['pos'][0] + ]    
            self.boad[block['pos'][0] - 1, block['pos'][1] + j] = block['ptr'][j][0] * block_number

        block['pos'] -= [-1, 0]
        
        return True

#    def move_right(self, block_number):
#        if self.__left_edge(blanks[blank_number]):
#            return False
#
#        block_number = boad(self.__left_side)
#        if block_number == _blank:
#            return False
#
#        block = self.blocks[block_number]
#        for j in range(block['ptr'].shape[0]):
#            if self.boad(block['pos'] + block['ptr'].shape[1], block['pos'][1] + j) != blank_number:
#                return False
#            
#        block['pos'] = block['pos'] + [1, 0]
#        for j in range(block['ptr'].shape[0]):
            
                
        #        next = np.copy()

    def __is_blank(self, block_number):
        return (block_number < 0)


    def __left_edge(self, pos):
        return (pos[0] <= 0)

    def __right_edge(self, pos):
        return (pos[0] >= self.width - 1)

    def __up_edge(self, pos):
        return (pos[1] <= 0)
    
    def __down_edge(self, pos):
        return (pos[1] >= self.height - 1)


    def __left_side(self, pos):
        return (pos + np.array([-1, 0]))

    def __right_side(self, pos):
        return pos + np.array([1, 0])

    def __up_side(self, pos):
        return pos + np.array([0, -1])

    def __down_side(self, pos):
        return pos + np.array([0, 1])
        
        

def solve_ditb():
    ditb = DITB()
    ditb.show()

    print(ditb.movable_down())
    ditb.move_left(9)
    ditb.show()


if __name__ == '__main__':

    solve_ditb()
    
    
    