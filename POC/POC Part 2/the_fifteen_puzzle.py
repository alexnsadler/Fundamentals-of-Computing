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
        self._final_string = ""
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
        self._final_string += move_string
    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        
        rows_to_check = self.get_height() - target_row - 1
        cols_to_check = self.get_width() - target_col - 1

        # If the current position of 0 isn't the target (row, col),
        # returns false
        if self.current_position(0,0) != (target_row, target_col):
            return False
        
        # If there are rows to check, the loop checks each cell in the 
        # row below the target row to see if they're in the correct spot
        if rows_to_check > 0:
            for row_pos in range(self.get_width()):
                if self.current_position(target_row + 1, row_pos) != (target_row + 1, row_pos):
                    return False
                
        # If there are columns to check, the loop checks each cell to the
        # right of the target column to see if they're in the correct spot
        if cols_to_check > 0:
            for col_pos in range(target_col + 1, self.get_width()):                
                if self.current_position(target_row, col_pos) != (target_row, col_pos):
                    return False
        
        # If all conditions pass, return True
        return True

    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col), "lower_row_invariant error"
        target_tile_pos = self.current_position(target_row, target_col)

        clone = self.clone()
        
        move_string = ""
        init_up_moves = "u" * (target_row - target_tile_pos[0])
        init_r_moves = "r" * (target_tile_pos[1] - target_col)
        init_l_moves = "l" * (target_col - target_tile_pos[1])
        move_string += init_up_moves + init_r_moves + init_l_moves
        clone.update_puzzle(move_string)
        
        target_tile_pos = clone.current_position(target_row, target_col)
        
        # While loop that loops until the target tile is in the correct column
        while target_col != target_tile_pos[1]:
            if target_tile_pos[1] > target_col:
                if target_tile_pos[0] < target_row - 1:
                    col_move = "dllur"
                else:
                    col_move = "ulldr"
            if target_tile_pos[1] < target_col:
                if target_tile_pos[0] < target_row -1:
                    col_move = "drrul"
                else:
                    col_move = "urrdl"
            move_string += col_move
            clone.update_puzzle(col_move)
            target_tile_pos = clone.current_position(target_row, target_col)
        
        # Following if statements move the zero tile to be above the
        # target tile
        if clone.current_position(0,0)[1] > target_tile_pos[1]:
            if clone.current_position(0,0)[0] < target_row - 1:
                cyclic_move = "dlu"
            else: 
                cyclic_move = "ul"
        if clone.current_position(0,0)[1] < target_tile_pos[1]:
            if clone.current_position(0,0)[0] < target_row - 1:
                cyclic_move = "dru"
            else:
                cyclic_move = "ur"
        elif clone.current_position(0,0)[1] == target_tile_pos[1]:
            cyclic_move = ""
        move_string += cyclic_move
        clone.update_puzzle(cyclic_move)
        target_tile_pos = clone.current_position(target_row, target_col)
        
        # While the target tile isn't in the correct spot, keep applying "lddru"
        while target_tile_pos != (target_row, target_col):
            final_move = "lddru"
            move_string += final_move
            clone.update_puzzle(final_move)
            target_tile_pos = clone.current_position(target_row, target_col)
        
        # Move the zero tile to the left of the target tile
        placement_move = "ld"
        move_string += placement_move
        clone.update_puzzle(placement_move)
        
        self.update_puzzle(move_string)
        
        assert self.lower_row_invariant(target_row, target_col - 1), "lower_row_invariant error"
        
        return move_string


    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0), "lower_row_invariant error"
        clone = self.clone()
        
        move_string = "ur"
        clone.update_puzzle(move_string)
        target_tile_pos = clone.current_position(target_row, 0)
        
        # If the target tile is in the correct position, move the
        # zero tile to the end of row i - 1 and return the move string
        if target_tile_pos == (target_row, 0):
            move_string += ((self._width - 2) * "r")
            self.update_puzzle(move_string)
            return move_string
        
        init_up_moves = "u" * (target_row - target_tile_pos[0] - 1)
        init_r_moves = "r" * (target_tile_pos[1] - 1)
        init_l_moves = "l" * (1 - target_tile_pos[1])
        init_moves = init_up_moves + init_r_moves + init_l_moves
        move_string += init_moves
        clone.update_puzzle(init_moves)
        target_tile_pos = clone.current_position(target_row, 0)
        
        # While loop that keeps applying cyclic moves until the target
        # tile is in column 1
        while target_tile_pos[1] !=  1:
            if target_tile_pos[0] < target_row - 1:
                cyclic_move = "dllur"   
            else:
                cyclic_move = "ulldr"
            move_string += cyclic_move
            clone.update_puzzle(cyclic_move)
            target_tile_pos = clone.current_position(target_row, 0)
        
        if clone.current_position(0, 0)[1] == 0:
            if clone.current_position(0, 0)[0] == 0:
                zero_move = "drru"
            else:
                zero_move = "urrd"
            move_string += zero_move
            clone.update_puzzle(zero_move)
            target_tile_pos = clone.current_position(target_row, 0)
        
        # If the target tile is in the top row, apply "dlurd"
        if target_tile_pos[0] == 0:
            cyclic_move_1 = "dlurd"
            move_string += cyclic_move_1
            clone.update_puzzle(cyclic_move_1)
            target_tile_pos = clone.current_position(target_row, 0)
        
        if clone.current_position(0, 0)[0] < target_tile_pos[0]:
            move_string += "rd"
            clone.update_puzzle("rd")
            target_tile_pos  = clone.current_position(target_row, 0)
        
        # Keeps applying "dlu" until the target tile is in the row above
        # the target row
        while target_tile_pos[0] != target_row - 1:
            cyclic_move_2 = "dlu"
            move_string += cyclic_move_2
            clone.update_puzzle(cyclic_move_2)
            target_tile_pos = clone.current_position(target_row, 0)
        
        # Positions the zero tile above the target tile if it isn't there
        if clone.current_position(0,0)[1] != 1:
            next_move = "ul"
            move_string += next_move
            clone.update_puzzle(next_move)
            target_tile_pos = clone.current_position(target_row, 0)
            
        # Moves the zero tile to the left of the target tile, then moves
        # the target tile to the correct spot and then the zero tile to
        # the end of the row above the target row
        final_move = "ldruldrdlurdluurddlu" + ((self._width - 1)* "r" )
        clone.update_puzzle(final_move)
        move_string += final_move
        target_tile_pos = clone.current_position(target_row, 0)
        
        self.update_puzzle(move_string)
        
        return move_string
    
    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # If the 0 tile isn't in row0 at the target column, return false
        if self.current_position(0,0) != (0, target_col):
            return False
        
        # Checks the tiles from rows 2 to the end if they're all in the right pos
        if self._height > 2:
            for row in range(2, self._height):
                for col in range(self.get_width()):
                    if self.current_position(row, col) != (row, col):
                        return False
        
        # If the cell at (1, target_col) isn't in the right position, return False           
        if self.current_position(1, target_col) != (1, target_col):
            return False
        
        # If there are columns to check, returns false if there are any tiles
        # in the wrong position to the right of the target tile
        if target_col < self._width - 1:
            for col in range(target_col + 1, self._width):
                if self.current_position(0, col) != (0, col):
                    return False
        
        return True
    
    
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """       
        # If the 0 tile isn't in row 1 a the target column, return false
        if self.current_position(0,0) != (1, target_col):
            return False
        
        # If there are rows to check, returns false if there are any tiles
        # in the wrong position below the target tile
        if self._height > 2:
            for row in range(2, self._height):
                for col in range(self.get_width()):
                    if self.current_position(row, col) != (row, col):
                        return False
        
        # If there are columns to check, returns false if there are any tiles
        # in the wrong position to the right of the target tile
        if target_col < self._width - 1:
            for col in range(target_col + 1, self._width):
                if self.current_position(1, col) != (1, col):
                    return False
        
        return True


    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        
        clone = self.clone()
        
        move_string = ""
        first_move = "ld"
        move_string += first_move
        clone.update_puzzle(first_move)
        target_tile_pos = clone.current_position(0, target_col)
        
        if target_tile_pos == (0, target_col):
            self.update_puzzle(move_string)
            return move_string
        
        init_l_moves = "l" * (clone.current_position(0,0)[1] - target_tile_pos[1])
        init_up_moves = "u" * (clone.current_position(0,0)[0] - target_tile_pos[0])
        init_moves = init_up_moves + init_l_moves
        move_string += init_moves
        clone.update_puzzle(init_moves)
        target_tile_pos = clone.current_position(0, target_col)
        
        # Moves the target tile to target_col - 1
        while target_tile_pos[1] != target_col - 1:
            if target_tile_pos[0] == 1:
                cyclic_move = "urrdl"
            else:
                cyclic_move = "drrul" 
            move_string += cyclic_move
            clone.update_puzzle(cyclic_move)
            target_tile_pos = clone.current_position(0, target_col)
        
        # If the target tile is in the top row, move it a row down and
        # place the zero tile to the left of it
        if target_tile_pos[0] == 0:
            next_move = "druld"
            move_string += next_move
            clone.update_puzzle(next_move)
            target_tile_pos = clone.current_position(0, target_col)
        
        if clone.current_position(0,0) != (1, target_col - 2):
            zero_move = "ld"
            move_string += zero_move
            clone.update_puzzle(zero_move)
            target_tile_pos = clone.current_position(0, target_col)
        
        # Final move taken from quiz 10 to put tiles in the correct place    
        final_move = "urdlurrdluldrruld"
        move_string += final_move
        clone.update_puzzle(final_move)
        target_tile_pos = clone.current_position(0, target_col)
        
        self.update_puzzle(move_string)
        
        assert self.row1_invariant(target_col - 1)

        return move_string


    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col), "row1 error"
        target_tile_pos = self.current_position(1, target_col)
        
        clone = self.clone()

        move_string = ""
        init_up_moves = "u" * (1 - target_tile_pos[0])
        init_r_moves = "r" * (target_tile_pos[1] - target_col)
        init_l_moves = "l" * (target_col - target_tile_pos[1])
        move_string += init_up_moves + init_r_moves + init_l_moves
        clone.update_puzzle(move_string)
        target_tile_pos = clone.current_position(1, target_col)        
        
        while target_col != target_tile_pos[1]:
            if target_tile_pos[0] == 0:
                col_move = "drrul"
            else:
                col_move = "urrdl"
            move_string += col_move
            clone.update_puzzle(col_move)
            target_tile_pos = clone.current_position(1, target_col)
        
        if target_tile_pos[0] == 0:
            final_move = "dru"
        elif clone.current_position(0,0)[0] == 1:
            final_move = "ur"
        else:
            final_move = ""
        move_string += final_move

        self.update_puzzle(move_string)
   
        assert self.row0_invariant(target_col)	
        
        return move_string
    
    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        clone = self.clone()
        if clone.current_position(0,0) == (0,0):
            first_move = ""
        elif clone.current_position(0,0) == (0,1):
            first_move = "dlu"
        elif clone.current_position(0,0) == (1,1):
            first_move = "lu"
        else:
            first_move = "u"
        move_string += first_move
        clone.update_puzzle(first_move)
        
        proper_positions = ((0,0), (0,1), (1,1), (1,0))
        while ((clone.current_position(0,0)), (clone.current_position(0,1)), (clone.current_position(1,1)), (clone.current_position(1,0))) != proper_positions:
            cyclic_string = "rdlu"
            move_string += cyclic_string
            clone.update_puzzle(cyclic_string)
        
        self.update_puzzle(move_string)
        
        return move_string


    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        height = range(self._height)
        width = range(self._width)
        height.reverse()
        width.reverse()
        
        for row in height:
            for col in width:
                if self.current_position(row, col) != (row, col):
                    break
                else:
                    init_moves = ""
                   
        
        if self.current_position(0, 0) == (self._width - 1, self._height - 1):
            init_moves = ""
        else:
            init_r_moves = "r" * (self._width - self.current_position(0, 0)[1] - 1)
            init_up_moves = "d" * (self._height - self.current_position(0, 0)[0] - 1)
            init_moves = init_r_moves + init_up_moves
        
        self.update_puzzle(init_moves)
        
        p1_row_range = range(2,self._height)
        print p1_row_range
        p1_col_range = range(1, self._width)
        p1_row_range.reverse()
        p1_col_range.reverse()
       
        p2_col_range = range(2, self._width)
        p2_col_range.reverse()
        print p2_col_range
       
        for row in p1_row_range:
            for col in p1_col_range:
                print row, col
                self.solve_interior_tile(row, col)
                if col == 1:
                    self.solve_col0_tile(row)
      
        for col in p2_col_range:
            self.solve_row1_tile(col)
            self.solve_row0_tile(col)

        self.solve_2x2()

        return self._final_string 


# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(obj)

