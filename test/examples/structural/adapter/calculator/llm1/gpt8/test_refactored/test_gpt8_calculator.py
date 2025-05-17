import pytest
from refactored.calculator import CalculatorAdapter, OldCalculator

# Creating a test instance of the adapter with the old calculator
@pytest.fixture
def adapter():
    old_calculator = OldCalculator()
    return CalculatorAdapter(old_calculator)

def test_add(adapter):
    result = adapter.add(2, 3)
    assert result == 5

def test_sub(adapter):
    result = adapter.subtract(5, 3)
    assert result == 2

def test_mul(adapter):
    result = adapter.multiply(4, 3)
    assert result == 12

def test_div(adapter):
    result = adapter.divide(10, 2)
    assert result == 5

def test_division_by_zero(adapter):
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        adapter.divide(10, 0)

def test_unsupported_operation(adapter):
    with pytest.raises(AttributeError):  # CalculatorAdapter should not allow unsupported operations
        adapter.mod(4, 2)  # Calling a method that does not exist
