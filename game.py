import pygame
import sys
import os
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
        pygame.mixer.init()
        
        # Використовуємо колір з терміналу або стандартний
        self.current_bg = bg_color if bg_color else THEME['bg']
        
        self.screen = pygame.display.set_mode((450, 650))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        self.state = "MENU"
        
        # Звуки
        self.click_sound = None
        if os.path.exists("universfield-computer-mouse-click-352734.mp3"):
            self.click_sound = pygame.mixer.Sound("universfield-computer-mouse-click-352734.mp3")
        
        if os.path.exists("Cipher2.mp3"):
            pygame.mixer.music.load("Cipher2.mp3")
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)

        self.setup_menu()

    def play_click(self):
        if self.click_sound: self.click_sound.play()

    def setup_menu(self):
        self.buttons = []
        for i, text in enumerate(["Easy", "Medium", "Hard", "Exit"]):
            rect = pygame.Rect(100, 220 + i*85, 250, 65)
            self.buttons.append({'text': text, 'rect': rect})

    def draw_menu(self):
        self.screen.fill(self.current_bg)
        title = pygame.font.SysFont('Verdana', 46, bold=True).render("MINESWEEPER", True, THEME['accent'])
        self.screen.blit(title, title.get_rect(center=(225, 120)))

        m_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            hover = btn['rect'].collidepoint(m_pos)
            color = (100, 50, 180) if hover else THEME['hidden']
            pygame.draw.rect(self.screen, color, btn['rect'], border_radius=18)
            pygame.draw.rect(self.screen, THEME['accent'], btn['rect'], 3 if hover else 1, border_radius=18)
            txt = pygame.font.SysFont('Verdana', 24, bold=True).render(btn['text'], True, THEME['text'])
            self.screen.blit(txt, txt.get_rect(center=btn['rect'].center))
        pygame.display.flip()

    def start_game(self, level):
        self.play_click()
        conf = {"Easy": (10, 10, 12, 45), "Medium": (14, 14, 28, 32), "Hard": (18, 18, 55, 25)}
        r, c, m, size = conf[level]
        self.board = Board(r, c, size, m)
        self.screen = pygame.display.set_mode((c * size, r * size))
        self.state = "PLAY"

    def run(self):
        while True:
            if self.state == "MENU":
                self.draw_menu()
                for e in pygame.event.get():
                    if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        for b in self.buttons:
                            if b['rect'].collidepoint(e.pos):
                                if b['text'] == "Exit": pygame.quit(); sys.exit()
                                self.start_game(b['text'])
            elif self.state == "PLAY":
                self.screen.fill(self.current_bg)
                self.board.draw(self.screen, THEME, NUM_COLORS)
                pygame.display.flip()
                for e in pygame.event.get():
                    if e.type == pygame.QUIT: 
                        self.state = "MENU"
                        self.screen = pygame.display.set_mode((450, 650))
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        self.play_click()
                        r, c = e.pos[1] // self.board.cell_size, e.pos[0] // self.board.cell_size
                        if e.button == 1:
                            if not self.board.reveal(r, c): 
                                self.state = "MENU"
                                self.screen = pygame.display.set_mode((450, 650))
                        elif e.button == 3:
                            self.board.grid[r][c].is_flagged = not self.board.grid[r][c].is_flagged
                if self.board.check_win(): 
                    self.state = "MENU"
                    self.screen = pygame.display.set_mode((450, 650))
                self.clock.tick(60)