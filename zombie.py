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
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for man in self._human_list:
            yield man
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self.get_grid_height(),self.get_grid_width())
        distance_field = [[ self._grid_width * self._grid_height for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            for man in self.humans():
                boundary.enqueue(man)
        elif entity_type == ZOMBIE:
            for zombie in self.zombies():
                boundary.enqueue(zombie)
        for item in boundary:
            visited.set_full(item[0],item[1])
            distance_field[item[0]][item[1]] = 0
        
        while len(boundary) > 0 :
            current_cell = boundary.dequeue()
            all_neighbor_cell = poc_grid.Grid.four_neighbors(self,current_cell[0],current_cell[1])
            for neighbor_cell in all_neighbor_cell:
                if visited.is_empty(neighbor_cell[0],neighbor_cell[1]):
                    visited.set_full(neighbor_cell[0],neighbor_cell[1])
                    
                    if self._cells[neighbor_cell[0]][neighbor_cell[1]] == EMPTY:
                        boundary.enqueue(neighbor_cell)
                        distance_field[neighbor_cell[0]][neighbor_cell[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
        return distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for man_idx in range(self.num_humans()):
            neighbors = poc_grid.Grid.eight_neighbors(self, self._human_list[man_idx][0],self._human_list[man_idx][1])
            max_val = 0
            max_pos = tuple()
            for neighbor in neighbors:
                if self._cells[neighbor[0]][neighbor[1]] == FULL:
                    continue
                if (neighbor[0],neighbor[1]) in self._human_list:
                    continue
                if zombie_distance_field[neighbor[0]][neighbor[1]] > max_val:
                    max_val = zombie_distance_field[neighbor[0]][neighbor[1]]
                    max_pos = (neighbor[0],neighbor[1])
            if max_pos is not ():
                self._human_list[man_idx] = max_pos
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie_idx in range(self.num_zombies()):
            if human_distance_field[self._zombie_list[zombie_idx][0]][self._zombie_list[zombie_idx][1]] == 0:
                continue
            neighbors = poc_grid.Grid.four_neighbors(self, self._zombie_list[zombie_idx][0],self._zombie_list[zombie_idx][1])
            min_val = 5000000000
            min_pos = tuple()
            for neighbor in neighbors: 
                if self._cells[neighbor[0]][neighbor[1]] == FULL:
                    continue
                if (neighbor[0],neighbor[1]) in self._zombie_list:
                    continue
                if human_distance_field[neighbor[0]][neighbor[1]] < min_val:
                    min_val = human_distance_field[neighbor[0]][neighbor[1]]
                    min_pos = (neighbor[0],neighbor[1])
            if min_pos is not ():
                self._zombie_list[zombie_idx] = min_pos

# Start up gui for simulation - You will need to write some code above
# before this will work without errors
poc_zombie_gui.run_gui(Apocalypse(30, 40))
