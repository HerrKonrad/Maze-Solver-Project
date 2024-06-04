import time 
import pygame
class Maze_Solver:
    def __init__(self, grid_cells, start_cell, end_cell):
        self.grid_cells = grid_cells
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.stack = []
        self.queue = []
        self.counting = 0
        self.maze_solved = False
        self.start_end_choosen = False
    
    
    def create_path(self):
        print('Creating the path')
        path_stack = []
        next = self.end_cell.verify_next_cell()
        if next is not None:
            path_stack.append(next)
            while next != self.start_cell:
                next.is_path = True
                next = next.verify_next_cell()
                path_stack.append(next)
        return True

    def clear_resolution(self):
        for cell in self.grid_cells:
            self.counting = 0
            cell.analyzed = False
            cell.number = 0
            cell.is_path = False

    def dfs_resolution(self):
        print('Starting DFS resolution')
        start = time.perf_counter()
        
        if self.start_cell is None or self.end_cell is None:
            return False
        self.stack.append(self.start_cell)
        while len(self.stack) > 0:
            current_cell = self.stack[-1]
            if not current_cell.analyzed:
                    self.counting += 1
                    current_cell.number = self.counting
            # Check if the current cell has any neighbours
            neighbours = current_cell.verify_next_cells()
            # If the current cell has no neighbours
            if len(neighbours) == 0:
                # Remove the cell from the stack (the last element)
                self.stack.pop()
            else:
                next_cell = neighbours[0]
                self.stack.append(next_cell)
        end = time.perf_counter()
        self.counting = 0
        return end - start

    def bfs_resolution(self):
        print('Starting BFS resolution')
        start = time.perf_counter()
        self.counting = 1
        if self.start_cell is None or self.end_cell is None:
            return False
        self.queue.append(self.start_cell)
        while len(self.queue) > 0:
            # Remove the first element from the queue
            current_cell = self.queue.pop(0)
            neighbours = current_cell.verify_next_cells()
            for neighbour in neighbours:
                if not neighbour.analyzed:
                    self.counting += 1
                    neighbour.number = self.counting
                    self.queue.append(neighbour)
        end = time.perf_counter()
        self.counting = 0
        return end - start
    
