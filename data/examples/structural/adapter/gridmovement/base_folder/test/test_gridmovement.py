# test_movement.py

import pytest
from base.gridmovement import GridMover

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

def test_grid_mover_bounds():
    results = {
        "up": (0, -3),
        "down": (0, 3),
        "left": (-3, 0),
        "right": (3, 0)
    }

    for direction in results:
        mover = GridMover()
        for _ in range(3):
            mover.move(direction)
        assert mover.get_position() == results[direction]
        with pytest.raises(ValueError):
            mover.move(direction)



