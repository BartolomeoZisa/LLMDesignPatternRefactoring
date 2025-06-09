import pytest
from base.roundhole import RoundHole, RoundPeg, SquarePeg
import math

def test_round_peg_fits_hole_exact():
    assert RoundHole(5).fits(RoundPeg(5)) is True

def test_round_peg_too_big():
    assert RoundHole(5).fits(RoundPeg(6)) is False

def test_square_peg_fits():
    peg = SquarePeg(5)
    assert RoundHole(5).fits_other(peg, "square") is True

def test_square_peg_too_big():
    peg = SquarePeg(10)
    assert RoundHole(5).fits_other(peg, "square") is False

def test_square_peg_exact_fit():
    width = 5 * 2 / math.sqrt(2)
    peg = SquarePeg(width)
    assert RoundHole(5).fits_other(peg, "square") is True

def test_square_peg_just_over_threshold():
    width = 5 * 2 / math.sqrt(2) + 0.001
    peg = SquarePeg(width)
    assert RoundHole(5).fits_other(peg, "square") is False

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

