import pytest
from refactored.icecream import *

# New concrete component
class CupWithStick:
    def __init__(self):
        self.description = "Icecream Cup with Stick"

    def getDescription(self):
        return self.description

    def cost(self):
        return 2.00

# New concrete decorator
class Nuts(IcecreamDecorator):
    def __init__(self, icecream):
        super().__init__(icecream)
        self.description = "Nuts"
    
    def getDescription(self):
        return self.icecream.getDescription() + ", " + self.description
    
    def cost(self):
        return self.icecream.cost() + 0.70

def test_cup_with_stick_cost_and_description():
    cup_stick = CupWithStick()
    assert cup_stick.getDescription() == "Icecream Cup with Stick"
    assert cup_stick.cost() == 2.00

def test_nuts_decorator():
    cup_stick = CupWithStick()
    nuts = Nuts(cup_stick)
    assert nuts.getDescription() == "Icecream Cup with Stick, Nuts"
    assert nuts.cost() == 2.70

