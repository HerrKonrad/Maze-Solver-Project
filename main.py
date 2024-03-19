import pygame
from random import choice
from cell import Cell

RES = WIDTH, HEIGHT = 800, 640
TILE = 40
cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
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
        grid_cells.append(Cell(col, row, TILE, sc, cols, rows, grid_cells))
current_cell = grid_cells[0]
stack = []
colors, color = [], 40


while True:
    sc.fill(pygame.Color('darkslategray'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()
   # [pygame.draw.rect(sc, colors[i], (cell.x * TILE + 5, cell.y * TILE + 5, 
   #                                  TILE - 10, TILE -10), border_radius=12) for i, cell in enumerate(stack)]

    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        colors.append((min(color, 255), 10, 100))
        color += 1
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()   
        #current_cell.remove_walls(next_cell)
        #current_cell = next_cell
    
    pygame.display.flip()
    clock.tick(100)