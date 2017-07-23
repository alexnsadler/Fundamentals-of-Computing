"""
Clone of 2048 game.
"""

# import poc_2048_gui
#import poc_format_testsuite
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
    Function that merges a single row or column in 2048.
    """
    
    # this code shifts all non-zero values to the beginning,
    # then combines pairs and repeats step one
    
    result_list = [0]*len(line)
    result_list_1 = [0]*len(line)
    
    for idx in line:
        if idx != 0:
            result_list[result_list.index(0)] = idx
    
    for idx in range(len(line) - 1):
        if result_list[idx] == result_list[idx+1]:
            result_list[idx] = result_list[idx] * 2
            result_list[idx+1] = 0
    
    for idx in result_list:
        if idx != 0:
            result_list_1[result_list_1.index(0)] = idx
        
    return result_list_1


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        
        up_list = []
        for col in range(self._grid_width):
            up_list.append((0, col))
        
        down_list = []
        for col in range(self._grid_width):
            down_list.append((self._grid_height - 1, col))
        
        left_list =[]
        for row in range(self._grid_height):
            left_list.append((row, 0))
        
        right_list = []
        for row in range(self._grid_height):
            right_list.append((row, self._grid_width - 1))
        
        self._direction = {UP: up_list,
                          DOWN: down_list,
                          LEFT: left_list,
                          RIGHT: right_list}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # sets all values to zero
        self._board = [[row + col for col in range(self._grid_width)]
                                for row in range(self._grid_height)]
        
        for col in range(self._grid_width):
            for row in range(self._grid_height):
                self._board[row][col] = 0
                
        # calls self.new_tile() to add a tile                
        self.new_tile()
        
        # if there is more than one empty cell, 
        # self.new_tile() is called again
        if len(self.random_cell_list()) == (self.get_grid_height() * self.get_grid_width())-1:
            self.new_tile()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._board)
        
        #for row in range(self.grid_height):
            #print self.board[row]
        #print
        #print self.board[0]

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        
        if direction == 1:
            num_steps = self._grid_height
            start_cell = self._direction[UP]
        
        if direction == 2:
            num_steps = self._grid_height
            start_cell = self._direction[DOWN]
            
        if direction == 3: 
            num_steps = self._grid_width
            start_cell = self._direction[LEFT]
        
        if direction == 4:
            num_steps = self._grid_width
            start_cell = self._direction[RIGHT]
        
        values = []
        #self.traverse_grid(start_cell[0], direction, num_steps)

        for idx in range(len(start_cell)):
            self.traverse_grid(start_cell[idx], direction, num_steps)
            values.append(self._temp_list)

        #print values
        #print self.board
        #print values == self.board
        if (values != self._board or direction == 3):
            self.new_tile()

    def traverse_grid(self, start_cell, direction, num_steps):
        """
        Traverses the grid in a given direction depending on the start cell
        and creates a list of those values. Then the function merges the values
        and sets the tiles of the grid to the merged list.
        """
        self._temp_list = []
        for step in range(num_steps):
            row = start_cell[0] + step * OFFSETS[direction][0]
            col = start_cell[1] + step * OFFSETS[direction][1]
            self._temp_list.append(self._board[row][col])
        
        self._temp_list = merge(self._temp_list)

        for step in range(num_steps):
            row = start_cell[0] + step * OFFSETS[direction][0]
            col = start_cell[1] + step * OFFSETS[direction][1]
            self.set_tile(row, col, self._temp_list[step])
        
        #print self.temp_list
        #print self.board

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # picks a random value out of the list then sets that cell
        # to either 2 or 4.
        if len(self.random_cell_list()) == 0:
            return None
        random_cell_pos = random.choice(self.random_cell_list())
        self.set_tile(random_cell_pos[0], random_cell_pos[1], self.random_cell_value())
        
    def random_cell_list(self):
        """
        Starts with an empty list and adds the position of values
        that equal zero to the list.
        """
        rand_cell_list = []
        for col in range(self._grid_width):
            for row in range(self._grid_height):
                if self._board[row][col] == 0:
                    rand_cell_list.append((row, col))
        return rand_cell_list
        
    def random_cell_value(self):
        """
        Picks a value from 1 to 10. If the value is greater than 2,
        the cell value is 2. Otherwise it is 4.
        """
        random_int = random.random()
        if random_int > .1:
            return 2
        else: 
            return 4

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._board[row][col] = value
        

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        value = self._board[row][col]
        return value


#print
#obj = TwentyFortyEight(4,4)
#obj.set_tile(0, 0, 4)
#obj.set_tile(0, 1, 4)
#obj.set_tile(0, 2, 4)
#obj.set_tile(0, 3, 4)
#obj.set_tile(1, 0, 4)
#obj.set_tile(1, 1, 0)
#obj.set_tile(1, 2, 0)
#obj.set_tile(1, 3, 4)
#obj.set_tile(2, 0, 4)
#obj.set_tile(2, 1, 0)
#obj.set_tile(2, 2, 0)
#obj.set_tile(2, 3, 4)
#obj.set_tile(3, 0, 4)
#obj.set_tile(3, 1, 4)
#obj.set_tile(3, 2, 4)
#obj.set_tile(3, 3, 4)
#obj.move(UP)
#print
#obj.__str__()

    
# poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
# poc_format_testsuite.run_suite(TwentyFortyEight)
