import pygame
from random import choice


class Cell:
    def __init__(self, x, y, tile, sc, cols, rows, grid_cells, font, number=None):
        self.x, self.y, self.tile, self.sc, self.cols, self.rows = x, y, tile, sc, cols, rows
        self.sc = sc
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.grid_cells = grid_cells
        self.is_entry = False
        self.is_exit = False
        self.font = font
        self.number = number
        self.analyzed = False

    def draw_current_cell(self):
        x, y = self.x * self.tile, self.y * self.tile
        pygame.draw.rect(self.sc, pygame.Color('saddlebrown'), (x + 2, y + 2, self.tile - 2, self.tile - 2))
        
    def draw(self):
        
        x, y = self.x * self.tile, self.y * self.tile

        if self.visited:
            pygame.draw.rect(self.sc, pygame.Color('black'), (x, y, self.tile, self.tile))
        if self.is_entry:
            pygame.draw.rect(self.sc, pygame.Color('green'), (x, y, self.tile, self.tile))
        if self.is_exit:
            pygame.draw.rect(self.sc, pygame.Color('red'), (x, y, self.tile, self.tile))
       
        if self.walls['top']:
            pygame.draw.line(self.sc, pygame.Color('purple'), (x, y), (x + self.tile, y), 2)
        if self.walls['right']:
            pygame.draw.line(self.sc, pygame.Color('purple'), (x + self.tile, y), (x + self.tile, y + self.tile), 2)
        if self.walls['bottom']:
            pygame.draw.line(self.sc, pygame.Color('purple'), (x + self.tile, y + self.tile), (x, y + self.tile), 2)
        if self.walls['left']:
            pygame.draw.line(self.sc, pygame.Color('purple'), (x, y + self.tile), (x, y), 2)
        
        if self.number is not None:
            text_surface = self.font.render(str(self.number), True, pygame.Color('white'))
            text_rect = text_surface.get_rect(center=(x + self.tile // 2, y + self.tile // 2))
            self.sc.blit(text_surface, text_rect)

    def check_cell(self, x, y):
        if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
            return False
        find_index = lambda x, y: x + y * self.cols
        return self.grid_cells[find_index(x, y)]
    
    def verify_next_cells(self, filter=lambda cell: not cell.analyzed):
        neighbors = []

        # Verify if the cell has neighbors and if there are no walls
        if not self.walls['top']:
            top_cell = self.check_cell(self.x, self.y - 1)
            if top_cell and filter(top_cell):
                neighbors.append(top_cell)

        if not self.walls['right']:
            right_cell = self.check_cell(self.x + 1, self.y)
            if right_cell and filter(right_cell):
                neighbors.append(right_cell)

        if not self.walls['bottom']:
            bottom_cell = self.check_cell(self.x, self.y + 1)
            if bottom_cell and filter(bottom_cell):
                neighbors.append(bottom_cell)

        if not self.walls['left']:
            left_cell = self.check_cell(self.x - 1, self.y)
            if left_cell and filter(left_cell):
                neighbors.append(left_cell)
        
        self.analyzed = True

        return neighbors
    
    
    def verify_next_cell_dfs(self):
        next_cell = None
        neighbors = self.verify_next_cells(lambda cell: cell.number is not None)

        if neighbors:
            self.next_cell = min(neighbors, key=lambda cell: cell.number)
            
        return self.next_cell



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
