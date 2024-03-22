import pygame
from random import choice
from cell import Cell
from maze_solver import Maze_Solver

RES = WIDTH, HEIGHT = 800, 640
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
font = pygame.font.Font(None, 28)
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

grid_cells = []
for row in range(rows):
    for col in range(cols):
        grid_cells.append(Cell(col, row, TILE, sc, cols, rows, grid_cells, font))
current_cell = grid_cells[0]
stack = []
colors, color = [], 40

start_end_choosen = False
maze_solved = False

start_cell = None
end_cell = None

def choose_entry_exit():
        print('Stack is empty, now choosing entry and exit cells')
        # Choose the start cell randomly from the border cells
        start_candidates = [cell for cell in grid_cells if cell.x == 0 or cell.x == cols - 1 or cell.y == 0 or cell.y == rows - 1]
        s_cell = choice(start_candidates)

        # Choose the end cell randomly from the border cells excluding the start cell
        end_candidates = [cell for cell in start_candidates if cell != s_cell]
        e_cell = choice(end_candidates)

        # Defining the entry and exit cells
        s_cell.is_entry = True
        e_cell.is_exit = True

        # Now we define the entry cell as the number 1 of the maze resolution algorithm
        s_cell.number = 1

        return s_cell, e_cell

while True:
    sc.fill(pygame.Color('darkslategray'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    [cell.draw() for cell in grid_cells]
    current_cell.visited = True

    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        colors.append((min(color, 255), 10, 100))
        color += 1
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
        
       
    elif stack:
        #current_cell.is_exit = True
        current_cell = stack.pop()   
    # Now we can randomly choose the entry and exit cell
    if len(stack) == 0 and not start_end_choosen:
        start_cell, end_cell = choose_entry_exit()
        print('Start cell: ' + str(start_cell.x) + ' ' + str(start_cell.y))
        print('End cell: ' + str(end_cell.x) + ' ' + str(end_cell.y))
        start_end_choosen = True

    if start_end_choosen and maze_solved == False:
        # Now we can start solving the maze
        print('Solving the maze...')
        maze_solver = Maze_Solver(grid_cells, start_cell, end_cell)
        maze_solved = maze_solver.dfs_resolution()


    pygame.display.flip()
    clock.tick(500)