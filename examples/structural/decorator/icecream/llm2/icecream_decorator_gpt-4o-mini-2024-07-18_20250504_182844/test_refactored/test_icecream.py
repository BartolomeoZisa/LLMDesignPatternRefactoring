import pytest
from refactored.icecream import *

def test_cone():
    cone = Cone()
    assert cone.cost() == 1.00
    assert cone.getDescription() == "Icecream Cone"

def test_cup():
    cup = Cup()
    assert cup.cost() == 1.50
    assert cup.getDescription() == "Icecream Cup"

def test_chocolate_decorator():
    icecream = Chocolate(Cone())
    assert icecream.getDescription() == "Icecream Cone, Chocolate"
    assert icecream.cost() == 1.50

def test_strawberry_decorator():
    icecream = Strawberry(Cone())
    assert icecream.getDescription() == "Icecream Cone, Strawberry"
    assert icecream.cost() == 1.75

def test_vanilla_decorator():
    icecream = Vanilla(Cup())
    assert icecream.getDescription() == "Icecream Cup, Vanilla"
    assert icecream.cost() == 2.10

def test_multiple_decorators():
    icecream = Vanilla(Chocolate(Cone()))
    assert icecream.getDescription() == "Icecream Cone, Chocolate, Vanilla"
    assert icecream.cost() == 2.10

    icecream = Strawberry(Vanilla(Cup()))
    assert icecream.getDescription() == "Icecream Cup, Vanilla, Strawberry"
    assert icecream.cost() == 2.85
