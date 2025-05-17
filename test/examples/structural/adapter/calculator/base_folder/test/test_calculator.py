import pytest

from base.calculator import OldCalculator

def test_add():
    calc = OldCalculator()
    result = calc.operation(2, 3, "add")
    assert result == 5

def test_sub():
    calc = OldCalculator()
    result = calc.operation(5, 3, "sub")
    assert result == 2

def test_mul():
    calc = OldCalculator()
    result = calc.operation(4, 3, "mul")
    assert result == 12

def test_div():
    calc = OldCalculator()
    result = calc.operation(10, 2, "div")
    assert result == 5

def test_division_by_zero():
    calc = OldCalculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.operation(10, 0, "div")

def test_unsupported_operation():
    calc = OldCalculator()
    with pytest.raises(ValueError, match="Unsupported operation"):
        calc.operation(4, 2, "mod")

