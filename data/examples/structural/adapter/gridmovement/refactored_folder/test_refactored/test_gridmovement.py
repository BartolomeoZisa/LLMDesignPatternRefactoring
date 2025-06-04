# test_movement.py

import pytest
from refactored.gridmovement import GridMover, KeyboardController, TouchAdapter

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

def test_touch_adapter_swipe():
    mover = GridMover()
    adapter = TouchAdapter(mover)
    adapter.swipe("swipe_up")
    assert mover.get_position() == (0, -1)
    adapter.swipe("swipe_left")
    assert mover.get_position() == (-1, -1)

def test_touch_adapter_invalid_swipe():
    mover = GridMover()
    adapter = TouchAdapter(mover)
    with pytest.raises(ValueError):
        adapter.swipe("swipe_diagonal")



