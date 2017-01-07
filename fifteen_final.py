"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row,target_col) != 0:
            return False
        for row in range(target_row + 1,self._height):
            for col in range(self._width):
                if self.get_number(row,col) != col + self._width * row:
                    return False
        for col in range(target_col+1,self._width):
            if self.get_number(target_row,col) != col + self._width * target_row:
                return False
        return True

    def move_right(self,solving_pos,target_col):
        """
        take solving position and target colomn and return the move string
        """
        mov_string = ''
        for index in range(solving_pos[1] - target_col):
            index = index + 1
            mov_string += 'r'
        if solving_pos[0] == 0:#first row
            for index in range(solving_pos[1] - target_col - 1):
                mov_string += 'dllur'
            mov_string += 'dl'
        else:
            for index in range(solving_pos[1] - target_col - 1):
                mov_string += 'ulldr'
            mov_string += 'ullddr'
        return mov_string 
    
    def move_left(self,solving_pos,target_col):
        """
        take solving position and target colomn and return the move string
        """
        mov_string = ''
        for index in range(target_col - solving_pos[1]):
            index = index + 1
            mov_string += 'l'
        if solving_pos[0] == 0:#first row
            for index in range(target_col - solving_pos[1] - 1):
                mov_string += 'drrul'
        else:
            for index in range(target_col - solving_pos[1] - 1):
                mov_string += 'urrdl'
        return mov_string 
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        solving_pos = self.current_position(target_row,target_col)
        mov_string = ""
        for index in range(target_row - solving_pos[0]):
            mov_string += "u"
            index = index + 1
        if solving_pos[1] == target_col:
            for index in range(target_row - solving_pos[0] - 1):
                mov_string += "lddru"
            mov_string += 'ld'
        else:
            if solving_pos[1] > target_col:#right
                mov_string += self.move_right(solving_pos,target_col)
            else:
                mov_string += self.move_left(solving_pos,target_col)
                if target_row != solving_pos[0]:
                    mov_string += 'dr'
                else:
                    self.update_puzzle(mov_string) 
                    return mov_string
            for index in range(target_row - solving_pos[0] - 1):
                mov_string += "d"
            new_puzzle = self.clone()
            new_puzzle.update_puzzle(mov_string)            
            mov_string += new_puzzle.solve_interior_tile(target_row,target_col)
        self.update_puzzle(mov_string) 
        return mov_string

    def position_tile(self,target_row):
        """
        position the target tile to position (target_row-1,1) 
        and the zero tile to position (target_row-1,0)
        """
        mov_string = ''
        solving_pos = self.current_position(target_row,0)
        for index in range(target_row - solving_pos[0]):
            mov_string += "u"
            index = index + 1
        if solving_pos[1] == 0:
            for index in range(target_row - solving_pos[0] - 2):
                mov_string += "rddlu"
            mov_string += 'rdl'
            self.update_puzzle(mov_string)
            return mov_string
        for index in range(solving_pos[1] ):
            mov_string += 'r'
        if solving_pos[0] == 0:#first row
            for index in range(solving_pos[1] - 1):
                mov_string += 'dllur'
        else:
            for index in range(solving_pos[1] - 1):
                mov_string += 'dllur'
        mov_string += 'dl'
        for index in range(target_row - solving_pos[0] - 1):
            mov_string += "d"
        self.update_puzzle(mov_string)
        return mov_string + self.position_tile(target_row)
            
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0),"fuck u"
        solving_pos = self.current_position(target_row,0)
        if solving_pos[1] == 0 and solving_pos[0] == target_row - 1:
            mov_string = "u"
            for index in range (self.get_width() - 1):
                mov_string += "r"
                index = index + 1
            self.update_puzzle(mov_string) 
            assert self.lower_row_invariant(target_row-1, self.get_width() - 1),"fuck u"
            return mov_string
        #position the target tile to position (target_rowâˆ’1,1) 
        #and the zero tile to position (target_rowâˆ’1,0)
        tmp = self.position_tile(target_row)
        
        if self.get_number(target_row-1,1) == self._width * target_row and self.get_number(target_row-1,0) == 0:
            mov_string = 'rrdluldruldrru'
            for index in range(self.get_width() -3):
                mov_string += "r"
            self.update_puzzle(mov_string) 
            assert self.lower_row_invariant(target_row-1, self.get_width() - 1),"fuck u"
            return tmp + mov_string
        assert False,'Error'
        

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(0,target_col) != 0:
            return False
        for row in range(2,self._height):
            for col in range(self._width):
                if self.get_number(row,col) != col + self._width * row:
                    return False
        for col in range(target_col,self._width):
            if self.get_number(1,col) != col + self._width:
                return False
        for col in range(target_col+1,self._width):
            if self.get_number(0,col) != col :
                return False
        return True
        
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(1,target_col) != 0:
            return False
        for row in range(2,self._height):
            for col in range(self._width):
                if self.get_number(row,col) != col + self._width * row:
                    return False
        for col in range(target_col+1,self._width):
            if self.get_number(1,col) != col + self._width:
                return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col),"fuck u"
        mov_string = ''
        solving_pos = self.current_position(0,target_col)
        if solving_pos[1] == target_col - 1:
            if solving_pos[0] == 0:
                mov_string += 'ld'
                self.update_puzzle(mov_string) 
                assert self.row1_invariant(target_col - 1),"fuck u"
                return mov_string
            elif solving_pos[0] == 1:
                mov_string += 'lld'
                mov_string += 'urdlurrdluldrruld'
                self.update_puzzle(mov_string)
                assert self.row1_invariant(target_col - 1),"fuck u"
                return mov_string
        else:
            mov_string += 'ld'
            for index in range(target_col - solving_pos[1]-1):
                index = index + 1
                mov_string += 'l'
            mov_string += 'u'
            tmp_str = ''
            for ch_mov in mov_string:
                if ch_mov == 'l':
                    tmp_str += 'r'
            mov_string += tmp_str
            self.update_puzzle(mov_string) 
            return mov_string + self.solve_row0_tile( target_col)
               
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col),"fuck u"
        mov_string = ''
        solving_pos = self.current_position(1,target_col)
        if solving_pos[1] == target_col:
            mov_string += 'u'
            self.update_puzzle(mov_string) 
            assert self.row0_invariant(target_col ),"fuck u"
            return mov_string
        if solving_pos[1] < target_col:
            if solving_pos[0] == 0:
                mov_string += 'u'
                for index in range(target_col - solving_pos[1]):
                    index = index + 1
                    mov_string += 'l'
                tmp_str = ''
                for ch_mov in mov_string:
                    if ch_mov == 'u':
                        tmp_str += 'd'
                    elif ch_mov == 'l':
                        tmp_str += 'r'
                mov_string += tmp_str
                self.update_puzzle(mov_string) 
                return mov_string + self.solve_row1_tile( target_col)
            else:
                for index in range(target_col - solving_pos[1]):
                    index = index + 1
                    mov_string += 'l'
                mov_string += 'ur'
                for index in range(target_col - solving_pos[1] - 1):
                    mov_string += 'rdlur'
                self.update_puzzle(mov_string) 
                assert self.row0_invariant(target_col ),"fuck u"
                return mov_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1),"fuck u"
        mov_string = 'lu'
        if self.lower_row_invariant(0,0):
            return mov_string
        self.update_puzzle(mov_string)
        for index in range(3):
            index = index + 1
            mov_string += 'rdlu'
            self.update_puzzle(mov_string[-4:])
            if self.lower_row_invariant(0,0):
                return mov_string
        return mov_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        #check if the game is already solved
        if self.lower_row_invariant(0,0):
            return ''
        mov_string_tmp = ""
        #move zero tile to the right down corner
        zero_pos = self.current_position(0,0)
        for index in range(zero_pos[0] + 1,self._height):
            index = index + 1
            mov_string_tmp += 'd'
        for index in range(zero_pos[1] + 1,self._width):
            mov_string_tmp += 'r'
            
        #print mov_string,111111111
        self.update_puzzle(mov_string_tmp)
        mov_string = ''
        
        #solve bottom rows of the puzzle in a row by row manner from bottom to top m-2
        for row in range(self._height - 1,1,-1):
            for col in range(self._width - 1,-1,-1):
                if col == 0:
                    mov_string += self.solve_col0_tile(row)
                else:
                    mov_string += self.solve_interior_tile(row,col)
        
        for col in range(self._width - 1,1,-1):
            mov_string += self.solve_row1_tile(col)
            mov_string += self.solve_row0_tile(col)
        mov_string += self.solve_2x2()
        return mov_string_tmp + mov_string
                    
# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4,4))
