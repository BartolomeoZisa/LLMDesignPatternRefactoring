import pytest
from base.sword import BasicSword

def test_basic_sword():
    sword = BasicSword()
    assert sword.description() == "Basic sword"
    assert sword.damage() == 10

def test_flaming_sword():
    sword = BasicSword()
    sword.add_decoration("flame")
    assert sword.description() == "Basic sword, with flames"
    assert sword.damage() == 15

def test_poisoned_sword():
    sword = BasicSword()
    sword.add_decoration("poison")
    assert sword.description() == "Basic sword, coated in poison"
    assert sword.damage() == 13

def test_ice_sword():
    sword = BasicSword()
    sword.add_decoration("ice")
    assert sword.description() == "Basic sword, imbued with ice"
    assert sword.damage() == 14

def test_stacked_decorators():
    sword = BasicSword()
    sword.add_decoration("flame")
    sword.add_decoration("poison")
    sword.add_decoration("ice")
    assert sword.description() == "Basic sword, with flames, coated in poison, imbued with ice"
    assert sword.damage() == 10 + 5 + 3 + 4  # 22

def test_same_decorators():
    sword = BasicSword()
    sword.add_decoration("flame")
    sword.add_decoration("flame")  # Duplicated flame
    assert sword.description() == "Basic sword, with flames, with flames"  # "with flames" twice
    assert sword.damage() == 10 + 5 + 5  # 20 (double the flame bonus)
