import pytest
from refactored.wand import (
    OakPhoenixRubyFactory,
    WillowPhoenixSapphireFactory,
    ElderPhoenixEmeraldFactory,
    Oak,
    Willow,
    Elder,
    PhoenixFeather,
    Ruby,
    Sapphire,
    Emerald,
)

def test_oak_phoenix_ruby_factory():
    factory = OakPhoenixRubyFactory()
    wand = factory.create_wand()

    assert isinstance(wand.wood, Oak)
    assert isinstance(wand.core, PhoenixFeather)
    assert isinstance(wand.gem, Ruby)

    # mana=50, damage=100, power=1
    expected_attack = 50 * (100 ** 1)  # 50 * 100 = 5000
    assert wand.attack == expected_attack

def test_willow_phoenix_sapphire_factory():
    factory = WillowPhoenixSapphireFactory()
    wand = factory.create_wand()

    assert isinstance(wand.wood, Willow)
    assert isinstance(wand.core, PhoenixFeather)
    assert isinstance(wand.gem, Sapphire)

    # mana=40, damage=100, power=1.25
    expected_attack = 40 * (100 ** 1.25)  
    # 100 ** 1.25 = 100 ** (5/4) = 100^(1) * 100^(0.25) = 100 * 3.16227766017 = 316.227766017
    # So 40 * 316.227766017 = 12649.11064068
    assert abs(wand.attack - 12649.11064068) < 1e-6

def test_elder_phoenix_emerald_factory():
    factory = ElderPhoenixEmeraldFactory()
    wand = factory.create_wand()

    assert isinstance(wand.wood, Elder)
    assert isinstance(wand.core, PhoenixFeather)
    assert isinstance(wand.gem, Emerald)

    # mana=70, damage=100, power=1.5
    expected_attack = 70 * (100 ** 1.5)
    # 100 ** 1.5 = 100^(3/2) = (100^(1))^(3/2) = 1000
    # So 70 * 1000 = 70000
    assert wand.attack == expected_attack
