from unittest.mock import MagicMock
from board import Board
import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_board_reveal_calls_generate_on_first_click(board):
    board.generate = MagicMock()
    board.reveal(0, 0)

    board.generate.assert_called_once_with(0, 0)
    assert board.first_click is False


@pytest.fixture
def board():
    return Board(5, 5, 30, 5)


def test_board_creation(board):
    assert len(board.grid) == 5
    assert len(board.grid[0]) == 5


@pytest.mark.parametrize("rows, cols, mines", [
    (10, 10, 12),
    (14, 14, 28),
    (18, 18, 55)
])
def test_board_sizes(rows, cols, mines):
    board = Board(rows, cols, 30, mines)

    assert len(board.grid) == rows
    assert len(board.grid[0]) == cols
