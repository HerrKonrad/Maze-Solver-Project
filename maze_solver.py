class Maze_Solver:
    def __init__(self, grid_cells, start_cell, end_cell):
        self.grid_cells = grid_cells
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.stack = []
        self.counting = 0
        self.maze_solved = False
        self.start_end_choosen = False
    
    def create_dfs_path(self):
        print('Creating the DFS path')
        path_stack = []

        next = self.end_cell.verify_next_cell_dfs()
        if next is not None:
            path_stack.append(next)
            while next != self.start_cell:
                next = next.verify_next_cell_dfs()
                path_stack.append(next)

        print('Path stack: ', )
        for cell in path_stack:
            print(cell.number)

        
    
                    
    def dfs_resolution(self):
        print('Starting DFS resolution')
        self.stack.append(self.start_cell)
        while len(self.stack) > 0:
            current_cell = self.stack[-1]
            #print('Current cell:', current_cell.x, current_cell.y)
            if not current_cell.analyzed:
                    self.counting += 1
                    current_cell.number = self.counting
                    #print('Current cell number:', current_cell.number)
            if current_cell == self.end_cell:
                print('End cell reached')
                self.maze_solved = True
                break
            else:
                # Check if the current cell has any neighbours
                neighbours = current_cell.verify_next_cells()
                if len(neighbours) == 0:
                    self.stack.pop()
                else:
                    next_cell = neighbours[0]
                    self.stack.append(next_cell)
        

        return self.maze_solved
