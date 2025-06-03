import pytest
from refactored.sword import BasicSword, FlamingDecorator, PoisonedDecorator, IceDecorator

def test_basic_sword():
    sword = BasicSword()
    assert sword.description() == "Basic sword"
    assert sword.damage() == 10

def test_flaming_sword():
    sword = FlamingDecorator(BasicSword())
    assert sword.description() == "Basic sword, with flames"
    assert sword.damage() == 15

def test_poisoned_sword():
    sword = PoisonedDecorator(BasicSword())
    assert sword.description() == "Basic sword, coated in poison"
    assert sword.damage() == 13

def test_ice_sword():
    sword = IceDecorator(BasicSword())
    assert sword.description() == "Basic sword, imbued with ice"
    assert sword.damage() == 14

def test_stacked_decorators():
    sword = IceDecorator(PoisonedDecorator(FlamingDecorator(BasicSword())))
    assert sword.description() == "Basic sword, with flames, coated in poison, imbued with ice"
    assert sword.damage() == 10 + 5 + 3 + 4  # 22

def test_same_decorators():
    sword = FlamingDecorator(BasicSword())
    sword = FlamingDecorator(sword)  # Adding FlamingDecorator again
    assert sword.description() == "Basic sword, with flames, with flames"
    assert sword.damage() == 15 + 5  # 20


