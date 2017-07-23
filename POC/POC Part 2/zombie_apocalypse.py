"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)      
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for idx in self._zombie_list:
            yield idx
                       
    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for idx in self._human_list:
            yield idx
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        if entity_type == HUMAN:
            entity_list = self._human_list
        if entity_type == ZOMBIE:
            entity_list = self._zombie_list
        
        visited = [[EMPTY for dummy_col in range(self._grid_width)]
                          for dummy_row in range(self._grid_height)]
        
        distance_field = [[self._grid_width * self._grid_height 
                           for dummy_col in range(self._grid_width)]
                           for dummy_row in range(self._grid_height)]
        
        boundary = list(entity_list)
        for cell in boundary:
            visited[cell[0]][cell[1]] = FULL
            distance_field[cell[0]][cell[1]] = 0
        
        while boundary != []:
            current_cell = boundary.pop(0)
            for neighbors in poc_grid.Grid.four_neighbors(self, current_cell[0], current_cell[1]):
                if visited[neighbors[0]][neighbors[1]] != FULL and self._cells[neighbors[0]][neighbors[1]] != FULL:
                    visited[neighbors[0]][neighbors[1]] = FULL
                    boundary.append(neighbors)
                    distance_field[neighbors[0]][neighbors[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
        
        for idx in distance_field:
            print idx
        
        return distance_field
                
                
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        hum_list = []
        for human in self._human_list:
            max_val = 0
            for neighbor in poc_grid.Grid.eight_neighbors(self, human[0], human[1]):
                print zombie_distance_field[neighbor[0]][neighbor[1]]
                if zombie_distance_field[neighbor[0]][neighbor[1]] > max_val and \
                   zombie_distance_field[neighbor[0]][neighbor[1]] != self._grid_height * self._grid_width:
                        max_val = zombie_distance_field[neighbor[0]][neighbor[1]]
                        human = neighbor             
            hum_list.append(human)
        
        self._human_list = hum_list

    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """ 
        zombie_list = []
        for zombie in self._zombie_list:
            min_val = self._grid_height * self._grid_width
            for neighbor in poc_grid.Grid.four_neighbors(self, zombie[0], zombie[1]):
                if human_distance_field[neighbor[0]][neighbor[1]] < min_val and \
                   human_distance_field[zombie[0]][zombie[1]] != 0:
                        min_val = human_distance_field[neighbor[0]][neighbor[1]]
                        zombie = neighbor             
            zombie_list.append(zombie)
        
        self._zombie_list = zombie_list


# poc_zombie_gui.run_gui(Apocalypse(30, 40))
