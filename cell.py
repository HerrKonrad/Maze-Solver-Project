import pygame
from random import choice


class Cell:
    def __init__(self, x, y, tile, sc, cols, rows, grid_cells):
        self.x, self.y, self.tile, self.sc, self.cols, self.rows = x, y, tile, sc, cols, rows
        self.sc = sc
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.grid_cells = grid_cells
        self.is_entry = False
        self.is_exit = False

    def draw_current_cell(self):
        x, y = self.x * self.tile, self.y * self.tile
        pygame.draw.rect(self.sc, pygame.Color('saddlebrown'), (x + 2, y + 2, self.tile - 2, self.tile - 2))
        
    def draw(self):
        x, y = self.x * self.tile, self.y * self.tile

        if self.visited:
            pygame.draw.rect(self.sc, pygame.Color('black'), (x, y, self.tile, self.tile))

        if self.is_entry:
            pygame.draw.rect(self.sc, pygame.Color('green'), (x, y, self.tile, self.tile))
        elif self.is_exit:
            pygame.draw.rect(self.sc, pygame.Color('red'), (x, y, self.tile, self.tile))
        else:
            if self.walls['top']:
                pygame.draw.line(self.sc, pygame.Color('purple'), (x, y), (x + self.tile, y), 2)
            if self.walls['right']:
                pygame.draw.line(self.sc, pygame.Color('purple'), (x + self.tile, y), (x + self.tile, y + self.tile), 2)
            if self.walls['bottom']:
                pygame.draw.line(self.sc, pygame.Color('purple'), (x + self.tile, y + self.tile), (x, y + self.tile), 2)
            if self.walls['left']:
                pygame.draw.line(self.sc, pygame.Color('purple'), (x, y + self.tile), (x, y), 2)

    def check_cell(self, x, y):
        if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
            return False
        find_index = lambda x, y: x + y * self.cols
        return self.grid_cells[find_index(x, y)]
        
    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
