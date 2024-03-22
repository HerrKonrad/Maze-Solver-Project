class Maze_Solver:
    def __init__(self, grid_cells, cols, rows, start_cell, end_cell):
        self.grid_cells = grid_cells
        self.cols = cols
        self.rows = rows
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.stack = []
        self.maze_solved = False
        self.start_end_choosen = False