import pytest
from base.monster import Monster, ZombieLeg, SkeletonLeg, ZombieArm, SkeletonArm

def test_zombie_monster_creation():
    legs = [ZombieLeg(), ZombieLeg()]  # Each leg speed = 5 * 0.75 = 3.75
    arms = [ZombieArm(), ZombieArm()]  # Each arm attack = 10 * 0.85 = 8.5
    monster = Monster("Zombie", legs, arms)

    assert monster.get_total_speed() == pytest.approx(3.75)
    assert monster.get_total_attack() == pytest.approx(17.0)

def test_skeleton_monster_creation():
    legs = [SkeletonLeg(), SkeletonLeg()]  # Each leg speed = 8 * 1.0 = 8.0
    arms = [SkeletonArm(), SkeletonArm()]  # Each arm attack = 15 * 1.25 = 18.75
    monster = Monster("Skeleton", legs, arms)

    assert monster.get_total_speed() == pytest.approx(8.0)
    assert monster.get_total_attack() == pytest.approx(37.5)

def test_ghoul_monster_creation():
    legs = [ZombieLeg(), SkeletonLeg()]  # 3.75 and 8.0
    arms = [ZombieArm(), SkeletonArm()]  # 8.5 and 18.75
    monster = Monster("Ghoul", legs, arms)

    expected_speed = (3.75 + 8.0) / 2
    expected_attack = 8.5 + 18.75

    assert monster.get_total_speed() == pytest.approx(expected_speed)
    assert monster.get_total_attack() == pytest.approx(expected_attack)

