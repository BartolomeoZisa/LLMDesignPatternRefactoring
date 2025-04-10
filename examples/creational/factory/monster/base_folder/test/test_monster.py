import pytest
from base.monster import Monster, Leg, Arm

def test_zombie_monster_creation():
    legs = [Leg(base_speed=5, modifier=0.75) for _ in range(2)]  # Speed per leg = 3.75
    arms = [Arm(base_attack=10, modifier=0.85) for _ in range(2)]  # Attack per arm = 8.5
    monster = Monster("Zombie", legs, arms)

    assert monster.get_total_speed() == pytest.approx(3.75)
    assert monster.get_total_attack() == pytest.approx(17.0)

def test_skeleton_monster_creation():
    legs = [Leg(base_speed=8, modifier=1.0) for _ in range(2)]  # Speed per leg = 8.0
    arms = [Arm(base_attack=15, modifier=1.25) for _ in range(2)]  # Attack per arm = 18.75
    monster = Monster("Skeleton", legs, arms)

    assert monster.get_total_speed() == pytest.approx(8.0)
    assert monster.get_total_attack() == pytest.approx(37.5)

def test_ghoul_monster_creation():
    legs = [
        Leg(base_speed=5, modifier=0.75),  # 3.75
        Leg(base_speed=8, modifier=1.0)    # 8.0
    ]
    arms = [
        Arm(base_attack=10, modifier=0.85),   # 8.5
        Arm(base_attack=15, modifier=1.25)    # 18.75
    ]
    monster = Monster("Ghoul", legs, arms)

    expected_speed = (3.75 + 8.0) / 2
    expected_attack = 8.5 + 18.75

    assert monster.get_total_speed() == pytest.approx(expected_speed)
    assert monster.get_total_attack() == pytest.approx(expected_attack)

