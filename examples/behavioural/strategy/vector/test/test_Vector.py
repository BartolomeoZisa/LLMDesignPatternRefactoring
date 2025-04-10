import pytest
from base.Vector import Vector  # Assuming the class is in a file named vector.py

def test_add():
    """Test adding elements increases size and stores values correctly."""
    vec = Vector()
    vec.add(10)
    assert vec.size == 1
    assert vec.get(0) == 10
    
    vec.add(20)
    assert vec.size == 2
    assert vec.get(1) == 20

def test_pop():
    """Test popping elements returns the correct value and decreases size."""
    vec = Vector()
    vec.add(5)
    vec.add(15)
    
    assert vec.pop() == 15  # Last-in, first-out
    assert vec.size == 1
    assert vec.pop() == 5
    assert vec.size == 0
    
    with pytest.raises(IndexError):
        vec.pop()  # Popping from empty vector should raise IndexError

def test_sort():
    """Test sorting functionality using various cases."""
    vec = Vector()
    vec.add(3)
    vec.add(1)
    vec.add(2)
    
    vec.sort()
    assert vec.get(0) == 1
    assert vec.get(1) == 2
    assert vec.get(2) == 3
    
    vec = Vector()  # Test empty vector sort
    vec.sort()  # Should not raise an error
    assert vec.to_string() == "[]"
    
    vec.add(7)  # Test single element sort
    vec.sort()
    assert vec.get(0) == 7

def test_get():
    """Test get method for valid and invalid indices."""
    vec = Vector()
    vec.add(100)
    assert vec.get(0) == 100
    
    with pytest.raises(IndexError):
        vec.get(1)  # Out of bounds
    
    with pytest.raises(IndexError):
        vec.get(-1)  # Negative index out of bounds

def test_to_string():
    """Test string representation of the vector using to_string method."""
    vec = Vector()
    assert vec.to_string() == "[]"
    
    vec.add(1)
    vec.add(2)
    assert vec.to_string() == "[1, 2]"
