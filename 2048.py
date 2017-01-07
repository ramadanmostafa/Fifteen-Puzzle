"""
Clone of 2048 game.
2048 game developed by my during take a coursera course in rice university using python programming language
just click execute button and enjoy playing
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code from the previous mini-project
    result=[0]*len(line)
    index = 0
    for iterator in range(len(line)):
        if line[iterator] != 0:
            result[0]=line[iterator]
            index = iterator
            break
    tmp_i = 0
    for iterator in range(index+1,len(line)):
        if line[iterator] == 0 :
            continue
        elif line[iterator] == result[tmp_i] :
            result[tmp_i] *= 2
            tmp_i+=1
            if len(line) < iterator+1:
                result[tmp_i]=line[iterator+1]
        else:
            tmp_i+=1
            result[tmp_i] = line[iterator]
    
    tmp=[0]*len(line)
    itx=0
    for item in result: 
        if item != 0:
            tmp[itx] = item
            itx+=1
    return tmp

def lst_not_updated(lst1,lst2):
    """
    check if 2 lists are identical or not
    """
    if len(lst1) == len(lst2):
        for index in range(len(lst1)):
            if lst1[index] != lst2[index]:
                return False
        return True
    else:
        return False

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self.__height__ = grid_height
        self.__width__ = grid_width
        self.__initial_tiles__ = self.comput_init_tiles()
        self.reset()

    def comput_init_tiles(self):
        """
        compute initial tiles dictionary for move function
        """
        
        up_list = []
        down_list = []
        for idx in range(self.__width__):
            up_list.append((0,idx))
            down_list.append((self.__height__-1,idx))
        left_list=[]
        right_list=[]
        for idy in range(self.__height__):
            left_list.append((idy,0))
            right_list.append((idy,self.__width__-1))
        return {UP: up_list,
                DOWN: down_list,
                LEFT: left_list,
                RIGHT: right_list}
        
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self.__grid__= [[i*j*0 for i in range(self.__width__)] for j in range(self.__height__)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        grid_string="["
        for idx in range(len(self.__grid__)):
            grid_string+= str(self.__grid__[idx])+"\n"      
        return grid_string+"]"

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self.__height__

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self.__width__

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        offset = OFFSETS[direction]
        iteration_num = 0
        is_moved = False
        if direction == UP or direction == DOWN:
            iteration_num = self.__height__
        elif direction == LEFT or direction == RIGHT:
            iteration_num = self.__width__
        for init_tile in self.__initial_tiles__[direction]:
            tmp_lst=[]
            tmp_lst.append(self.__grid__[init_tile[0]][init_tile[1]])            
            for idx in range(1,iteration_num):
                tmp_lst.append(self.__grid__[init_tile[0]+idx*offset[0]][init_tile[1]+idx*offset[1]])
            result_lst = merge(tmp_lst)
            if not lst_not_updated(result_lst,tmp_lst):
                
                row = init_tile[0]
                col = init_tile[1]
                for result_item in result_lst:
                    self.__grid__[row][col] = result_item
                    row += offset[0]
                    col += offset[1] 
                is_moved = True
        if is_moved :
            self.new_tile()
        

    def get_empty_grid_cells(self):
        """
        return a list of tubles of indexes of all empty cells(0 values)
        """
        tmp_lst=[]
        for idx in range(len(self.__grid__)):
            for idy in range(len(self.__grid__[0])):
                if self.__grid__[idx][idy] == 0:
                    tmp_lst.append((idx,idy))
        return tmp_lst
        
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        empty_cells = self.get_empty_grid_cells()
        if len(empty_cells) > 0:
            index = random.choice(empty_cells)
            self.__grid__[index[0]][index[1]] = random.choice([2,2,2,2,2,2,2,2,2,4])

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self.__grid__[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self.__grid__[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(3, 4))
