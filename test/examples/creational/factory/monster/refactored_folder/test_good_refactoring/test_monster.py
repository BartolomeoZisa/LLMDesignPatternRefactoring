import pytest
from refactored.monster import *

# ------------------------------
# New Concrete Subclasses
# ------------------------------

class GhostArm(Arm):
    def __init__(self):
        super().__init__(base_attack=8, attack_modifier=1.50)

class GhostLeg(Leg):
    def __init__(self):
        super().__init__(base_speed=10, speed_modifier=1.20)

# ------------------------------
# Concrete Factory for Ghost Monsters
# ------------------------------

class GhostFactory(MonsterFactory):
    def create_right_leg(self):
        return GhostLeg()

    def create_left_leg(self):
        return GhostLeg()

    def create_right_arm(self):
        return GhostArm()

    def create_left_arm(self):
        return GhostArm()

# from monster_factory import GhostFactory, GhostArm, GhostLeg

def test_ghost_factory_creates_ghost_monster():
    factory = GhostFactory()
    monster = factory.create_monster("Spectral Terror")

    # Check monster name
    assert monster.name == "Spectral Terror"

    # Check all legs are GhostLeg
    assert all(isinstance(leg, GhostLeg) for leg in monster.legs)

    # Check all arms are GhostArm
    assert all(isinstance(arm, GhostArm) for arm in monster.arms)

    # Check total speed: each GhostLeg has base_speed 10 * 1.20 = 12.0
    expected_speed = pytest.approx((12.0 + 12.0) / 2)
    assert monster.get_total_speed() == expected_speed

    # Check total attack: each GhostArm has base_attack 8 * 1.5 = 12.0
    expected_attack = pytest.approx(12.0 + 12.0)
    assert monster.get_total_attack() == expected_attack

    # Optional: check __str__ contains expected values
    output = str(monster)
    assert "Spectral Terror" in output
    assert "Total Speed" in output
    assert "Total Attack" in output
