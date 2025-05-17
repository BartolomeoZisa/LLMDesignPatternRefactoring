import pytest
from base.icecream import IceCream

def test_cone():
    icecream = IceCream("cone", [])
    assert icecream.cost() == 1.00
    assert icecream.getDescription() == "Icecream Cone, "

def test_cup():
    icecream = IceCream("cup", [])
    assert icecream.cost() == 1.50
    assert icecream.getDescription() == "Icecream Cup, "

def test_chocolate_flavor():
    icecream = IceCream("cone", ["chocolate"])
    assert icecream.getDescription() == "Icecream Cone, Chocolate"
    assert icecream.cost() == 1.50

def test_strawberry_flavor():
    icecream = IceCream("cone", ["strawberry"])
    assert icecream.getDescription() == "Icecream Cone, Strawberry"
    assert icecream.cost() == 1.75

def test_vanilla_flavor():
    icecream = IceCream("cup", ["vanilla"])
    assert icecream.getDescription() == "Icecream Cup, Vanilla"
    assert icecream.cost() == 2.10

def test_multiple_flavors():
    icecream = IceCream("cone", ["chocolate", "vanilla"])
    assert icecream.getDescription() == "Icecream Cone, Chocolate, Vanilla"
    assert icecream.cost() == 2.10

    icecream = IceCream("cup", ["vanilla", "strawberry"])
    assert icecream.getDescription() == "Icecream Cup, Vanilla, Strawberry"
    assert icecream.cost() == 2.85

def test_invalid_container():
    with pytest.raises(ValueError, match="Invalid container type 'bowl'. Choose 'cone' or 'cup'."):
        IceCream("bowl", ["vanilla"])

def test_invalid_flavor():
    with pytest.raises(ValueError, match="Invalid flavor 'blueberry'. Choose from .*"):
        IceCream("cone", ["blueberry"])