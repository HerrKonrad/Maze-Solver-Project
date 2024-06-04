import pygame
import pygame_menu
from random import choice
from cell import Cell
from maze_solver import Maze_Solver
from time import sleep
from maze_solver import Maze_Solver
import sys
# Initial values for TILE, cols and rows
RES = WIDTH, HEIGHT = 1280, 720
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE

def change_size(r, c):
    global TILE, cols, rows, WIDTH, HEIGHT, font
    cols, rows = c, r
    TILE = min(WIDTH // cols, HEIGHT // rows) 
    font = pygame.font.Font(None, int(TILE / 1.5))


pygame.init()
pygame.display.set_caption('Maze Solver')
font = pygame.font.Font(None, 28)
font_letters = pygame.font.Font(None, 40)
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

menu = pygame_menu.Menu('Maze Configuration', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

grid_cells = []
stack = []
start_end_choosen = False
maze_solved = False
start_cell = None
end_cell = None
current_cell = None
show_maze_generation = True

resolutions = {
    'DFS': Maze_Solver.dfs_resolution,
    'BFS': Maze_Solver.bfs_resolution
}

resolution_times = {}

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

def set_maze_size(value, size):
    print('Selected size:', size)
    change_size(size)
    #TILE = size

def generate_maze(show_generation=False):
    global current_cell, start_cell, end_cell, stack
    
    while True:
        current_cell.visited = True
        # Maze generation algorithm
        next_cell = current_cell.check_neighbors()
        if next_cell:
                next_cell.visited = True
                stack.append(current_cell)
                remove_walls(current_cell, next_cell)
                current_cell = next_cell

        elif stack:
                current_cell = stack.pop()
        
        if show_generation:
            [cell.draw() for cell in grid_cells]
            pygame.display.flip()
        
        if len(stack) == 0:
            break


def program_loop():
    # Update the size of the maze based on the selected values in the menu
    change_size(rows, cols)
    global current_cell, start_end_choosen, maze_solved, start_cell, end_cell, stack, res

    print('Starting the program...')
    
    for row in range(rows):
        for col in range(cols):
            grid_cells.append(Cell(col, row, TILE, sc, cols, rows, grid_cells, font))
    current_cell = grid_cells[0]
    stack.clear()
    start_end_choosen = False
    maze_solved = False
    start_cell = None
    end_cell = None

    while True:
        sc.fill(pygame.Color('darkslategray'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        [cell.draw() for cell in grid_cells]

        generate_maze(show_generation=show_maze_generation)
          
        
        # Now we can randomly choose the entry and exit cell
        if len(stack) == 0 and not start_end_choosen:
            start_cell, end_cell = choose_entry_exit()
            start_end_choosen = True

        if start_end_choosen and not maze_solved:
            # Now we can start solving the maze
            print('Solving the maze...')
            maze_solver = Maze_Solver(grid_cells, start_cell, end_cell)
            
            for res_name, func_res in resolutions.items():
                print(f"Resolution: {res_name}")
                maze_solver.clear_resolution()
                time_elapsed = func_res(maze_solver)
                maze_solver.create_path()
                if time_elapsed:
                    print(f"Time elapsed during the {res_name} resolution: {time_elapsed}")
                    resolution_times[res_name] = time_elapsed
                [cell.draw() for cell in grid_cells]
                # Write the number of the resolution on the top right corner
                pygame.display.set_caption(f"Maze Solver - Resolution: {res_name}")
                pygame.display.flip()
                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN:
                        break
                pygame.event.clear()  # Clear any remaining events from the queue
            
            maze_solved = True
            
        
        if maze_solved:
            print('Maze solved')
            # Clear the screen
            sc.fill(pygame.Color('darkslategray'))
            
            # Write the resolution times on the screen
            text = font_letters.render('Resolution Times:', True, pygame.Color('white'))
            sc.blit(text, (10, 10))
            
            y = 40
            for res_name, time_elapsed in resolution_times.items():
                text = font_letters.render(f'{res_name}: {time_elapsed} seconds', True, pygame.Color('white'))
                sc.blit(text, (10, y))
                y += 30
                
            pygame.display.flip()     
            while True:
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN:
                        break
            pygame.event.clear()  # Clear any remaining events from the queue
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        #clock.tick(120)

rows = 10
cols = 10

def set_rows(value, r):
  global rows
  rows = r

def set_cols(value, c):
  global cols
  cols = c

def set_show_generation(value, show):
    global show_maze_generation
    show_maze_generation = show

menu.add.selector('Rows:', [('10', 10), ('20', 20), ('30', 30), ('40', 40), ('50', 50), ('60', 60), ('70', 70)], onchange=set_rows)
menu.add.selector('Cols:', [('10', 10), ('20', 20), ('30', 30), ('40', 40), ('50', 50), ('60', 60), ('70', 70)], onchange=set_cols)
menu.add.selector('Show Generation:', [('Yes', True), ('No', False)], onchange=set_show_generation)
menu.add.button('Start', program_loop)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(sc)

