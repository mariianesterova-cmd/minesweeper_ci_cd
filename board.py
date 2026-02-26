import random
from cell import Cell

class Board:
    def __init__(self, rows, cols, cell_size, mines):
        self.rows, self.cols, self.cell_size, self.mines = rows, cols, cell_size, mines
        self.grid = [[Cell(r, c, cell_size) for c in range(cols)] for r in range(rows)]
        self.first_click = True 

    def generate(self, start_r, start_c):
        positions = []
        for r in range(self.rows):
            for c in range(self.cols):
                if abs(r - start_r) > 1 or abs(c - start_c) > 1:
                    positions.append((r, c))
        
        mines_to_place = min(self.mines, len(positions))
        for r, c in random.sample(positions, mines_to_place):
            self.grid[r][c].is_mine = True

        for r in range(self.rows):
            for c in range(self.cols):
                if not self.grid[r][c].is_mine:
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if 0 <= r+dr < self.rows and 0 <= c+dc < self.cols:
                                if self.grid[r+dr][c+dc].is_mine: count += 1
                    self.grid[r][c].adjacent_mines = count

    def reveal(self, r, c):
        if self.first_click:
            self.generate(r, c)
            self.first_click = False
        
        if not (0 <= r < self.rows and 0 <= c < self.cols): return True
        cell = self.grid[r][c]
        if cell.is_revealed or cell.is_flagged: return True 
        
        cell.is_revealed = True
        if cell.is_mine: return False
        
        if cell.adjacent_mines == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    self.reveal(r + dr, c + dc)
        return True

    def check_win(self):
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed: return False
        return True

    def draw(self, screen, theme, nums):
        for row in self.grid:
            for cell in row:
                cell.draw(screen, theme, nums)