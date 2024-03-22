class Maze_Solver:
    def __init__(self, grid_cells, start_cell, end_cell):
        self.grid_cells = grid_cells
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.stack = []
        self.maze_solved = False
        self.start_end_choosen = False
    
    def recursion(self, cell):
            counting = cell.number
            next_cells = cell.verify_next_cells()
            for cell in next_cells:
                counting += 1
                print(f"Cell x: {cell.x}, Cell y: {cell.y}")
                cell.number = counting
                self.recursion(cell)
                for c in cell.verify_next_cells():
                    print(f"NEXT --- Cell x: {c.x}, Cell y: {c.y}")
                    
    def dfs_resolution(self):
        print('Starting DFS resolution')

        self.recursion(self.start_cell)  

        return True
