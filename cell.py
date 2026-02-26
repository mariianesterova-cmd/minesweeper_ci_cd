import pygame

class Cell:
    def __init__(self, row, col, size):
        self.row, self.col, self.size = row, col, size
        self.rect = pygame.Rect(col * size, row * size, size, size)
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def draw(self, screen, theme, number_colors):
        padding = 2
        draw_rect = self.rect.inflate(-padding, -padding)
        
        if self.is_revealed:
            pygame.draw.rect(screen, theme['revealed'], draw_rect, border_radius=6)
            if self.is_mine:
                pygame.draw.circle(screen, theme['mine'], self.rect.center, self.size // 3)
            elif self.adjacent_mines > 0:
                font = pygame.font.SysFont('Verdana', int(self.size * 0.5), bold=True)
                color = number_colors.get(self.adjacent_mines, (0, 0, 0))
                text = font.render(str(self.adjacent_mines), True, color)
                screen.blit(text, text.get_rect(center=self.rect.center))
        else:
            pygame.draw.rect(screen, theme['hidden'], draw_rect, border_radius=6)
            if self.is_flagged:
                pygame.draw.rect(screen, theme['flag'], self.rect.inflate(-self.size//1.8, -self.size//1.8), border_radius=2)