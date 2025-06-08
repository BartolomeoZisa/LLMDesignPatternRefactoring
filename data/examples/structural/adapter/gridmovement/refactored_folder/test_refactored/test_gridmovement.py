# test_movement.py

import pytest
from refactored.gridmovement import GridMover, TouchAdapter



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

def test_touch_adapter_out_of_bounds():

    results = {
     "swipe_up": (0, -3),
     "swipe_down": (0, 3),
     "swipe_left": (-3, 0),
     "swipe_right": (3, 0)
     }
    for swipe in results:
        mover = GridMover()
        adapter = TouchAdapter(mover)
        for _ in range(3):
            adapter.swipe(swipe)
        assert mover.get_position() == results[swipe]
        with pytest.raises(ValueError):
            adapter.swipe(swipe)
    
