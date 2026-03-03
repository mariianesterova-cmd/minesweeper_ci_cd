import argparse
import pygame
from game import Game

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minesweeper CLI")
    parser.add_argument('--level', type=str, choices=['Easy', 'Medium', 'Hard'], help='Складність')
    parser.add_argument('--color', type=str, help='Колір фону (напр. black, red, gray)')

    args = parser.parse_args()
    pygame.init()

    custom_bg = None
    if args.color:
        try:
            custom_bg = pygame.Color(args.color)
        except Exception:
            print(f"Колір '{args.color}' не знайдено, буде стандартний.")
    app = Game(bg_color=custom_bg)

    if args.level:
        app.start_game(args.level)

    app.run()
