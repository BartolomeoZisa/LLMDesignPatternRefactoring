import pytest
from refactored.roundhole import RoundHole, RoundPeg, SquarePeg, SquarePegAdapter
import math

def test_round_peg_fits_hole_exact():
    assert RoundHole(5).fits(RoundPeg(5)) is True

def test_round_peg_too_big():
    assert RoundHole(5).fits(RoundPeg(6)) is False

def test_square_peg_adapter_fits():
    adapter = SquarePegAdapter(SquarePeg(5))
    assert RoundHole(5).fits(adapter) is True

def test_square_peg_adapter_too_big():
    adapter = SquarePegAdapter(SquarePeg(10))
    assert RoundHole(5).fits(adapter) is False

def test_square_peg_exact_fit():
    width = 5 * 2 / math.sqrt(2)
    adapter = SquarePegAdapter(SquarePeg(width))
    assert RoundHole(5).fits(adapter) is True

def test_square_peg_just_over_threshold():
    width = 5 * 2 / math.sqrt(2) + 0.001
    adapter = SquarePegAdapter(SquarePeg(width))
    assert RoundHole(5).fits(adapter) is False

def test_invalid_hole_radius_raises():
    with pytest.raises(ValueError, match="Hole radius must be positive"):
        RoundHole(0)
    with pytest.raises(ValueError):
        RoundHole(-1)

def test_invalid_peg_radius_raises():
    with pytest.raises(ValueError, match="Peg radius must be positive"):
        RoundPeg(0)
    with pytest.raises(ValueError):
        RoundPeg(-3)

def test_invalid_square_peg_width_raises():
    with pytest.raises(ValueError, match="Square peg width must be positive"):
        SquarePeg(0)
    with pytest.raises(ValueError):
        SquarePeg(-5)



