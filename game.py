import pygame
import sys
from board import Board

THEME = {
    'bg': (25, 15, 45),
    'hidden': (75, 35, 135),
    'revealed': (250, 250, 255),
    'mine': (255, 60, 110),
    'flag': (160, 255, 0),
    'text': (255, 255, 255),
    'accent': (160, 255, 0)
}
NUM_COLORS = {1: (40, 140, 255), 2: (160, 255, 0), 3: (255, 60, 110), 4: (180, 0, 255)}


class Game:
    def __init__(self, bg_color=None):
        pygame.init()
        self.current_bg = bg_color if bg_color else THEME['bg']
        self.screen = pygame.display.set_mode((450, 650))
        self.clock = pygame.time.Clock()
        self.state = "MENU"
        self.buttons = [
            {'rect': pygame.Rect(125, 150, 200, 60), 'text': "Easy"},
            {'rect': pygame.Rect(125, 250, 200, 60), 'text': "Medium"},
            {'rect': pygame.Rect(125, 350, 200, 60), 'text': "Hard"},
            {'rect': pygame.Rect(125, 450, 200, 60), 'text': "Exit"}
        ]

    def start_game(self, level):
        configs = {'Easy': (10, 10, 45, 12), 'Medium': (14, 14, 32, 28), 'Hard': (18, 18, 25, 55)}
        r, c, sz, m = configs[level]
        self.board = Board(r, c, sz, m)
        self.screen = pygame.display.set_mode((c * sz, r * sz))
        self.state = "PLAY"

    def run(self):
        while True:
            if self.state == "MENU":
                self._menu_loop()
            elif self.state == "PLAY":
                self._play_loop()
            self.clock.tick(60)

    def _menu_loop(self):
        self.screen.fill(THEME['bg'])
        for b in self.buttons:
            pygame.draw.rect(self.screen, THEME['hidden'], b['rect'])
            txt = pygame.font.SysFont(None, 40).render(b['text'], True, THEME['text'])
            self.screen.blit(txt, (b['rect'].x + 20, b['rect'].y + 15))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                for b in self.buttons:
                    if b['rect'].collidepoint(e.pos):
                        if b['text'] == "Exit":
                            sys.exit()
                        self.start_game(b['text'])

    def _play_loop(self):
        self.screen.fill(self.current_bg)
        self.board.draw(self.screen, THEME, NUM_COLORS)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self._back_to_menu()
            if e.type == pygame.MOUSEBUTTONDOWN:
                self._handle_click(e)
        if self.board.check_win():
            self._back_to_menu()

    def _handle_click(self, e):
        r, c = e.pos[1] // self.board.cell_size, e.pos[0] // self.board.cell_size
        if e.button == 1:
            if not self.board.reveal(r, c):
                self._back_to_menu()
        elif e.button == 3:
            self.board.grid[r][c].is_flagged = not self.board.grid[r][c].is_flagged

    def _back_to_menu(self):
        self.state = "MENU"
        self.screen = pygame.display.set_mode((450, 650))
