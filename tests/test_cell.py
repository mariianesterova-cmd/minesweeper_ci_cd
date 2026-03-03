from cell import Cell
import sys
import os
import pytest
import pygame
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_cell_initial_state():
    cell = Cell(0, 0, 30)

    assert cell.is_mine is False
    assert cell.is_revealed is False
    assert cell.is_flagged is False


@pytest.mark.graphics
def test_cell_draw_mock():
    pygame.init()

    screen = pygame.Surface((100, 100))

    cell = Cell(0, 0, 30)
    cell.is_revealed = True

    theme = {
        'revealed': (255, 255, 255),
        'mine': (255, 0, 0)
    }

    cell.draw(screen, theme, {})

    pygame.quit()

