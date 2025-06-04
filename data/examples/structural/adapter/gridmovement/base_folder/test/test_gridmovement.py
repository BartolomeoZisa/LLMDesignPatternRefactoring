# test_movement.py

import pytest
from base.gridmovement import GridMover, KeyboardController

def test_grid_mover_basic_movement():
    mover = GridMover()
    mover.move("up")
    assert mover.get_position() == (0, -1)
    mover.move("right")
    assert mover.get_position() == (1, -1)

def test_grid_mover_invalid_direction():
    mover = GridMover()
    with pytest.raises(ValueError):
        mover.move("diagonal")

def test_keyboard_controller():
    mover = GridMover()
    controller = KeyboardController(mover)
    controller.execute_commands(["right", "right", "down"])
    assert mover.get_position() == (2, 1)


