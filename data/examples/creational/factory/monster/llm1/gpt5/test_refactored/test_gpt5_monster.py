import pytest
from refactored.monster import (
    ZombieFactory, SkeletonFactory, GhoulFactory,
    ZombieLeg, SkeletonLeg, ZombieArm, SkeletonArm
)

def test_zombie_factory_creates_correct_monster():
    factory = ZombieFactory()
    monster = factory.create_monster("Zombie")

    # Assert all legs and arms are of Zombie types
    assert all(isinstance(leg, ZombieLeg) for leg in monster.legs)
    assert all(isinstance(arm, ZombieArm) for arm in monster.arms)

    # Speed: base=5, modifier=0.75 -> 3.75 per leg
    assert monster.get_total_speed() == pytest.approx(3.75)
    # Attack: base=10, modifier=0.85 -> 8.5 per arm
    assert monster.get_total_attack() == pytest.approx(17.0)

def test_skeleton_factory_creates_correct_monster():
    factory = SkeletonFactory()
    monster = factory.create_monster("Skeleton")

    # Assert all legs and arms are of Skeleton types
    assert all(isinstance(leg, SkeletonLeg) for leg in monster.legs)
    assert all(isinstance(arm, SkeletonArm) for arm in monster.arms)

    # Speed: base=8, modifier=1.0 -> 8.0 per leg
    assert monster.get_total_speed() == pytest.approx(8.0)
    # Attack: base=15, modifier=1.25 -> 18.75 per arm
    assert monster.get_total_attack() == pytest.approx(37.5)

def test_ghoul_factory_creates_mixed_monster():
    factory = GhoulFactory()
    monster = factory.create_monster("Ghoul")

    # Assert one leg is ZombieLeg and one is SkeletonLeg
    assert any(isinstance(leg, ZombieLeg) for leg in monster.legs)
    assert any(isinstance(leg, SkeletonLeg) for leg in monster.legs)

    # Assert one arm is ZombieArm and one is SkeletonArm
    assert any(isinstance(arm, ZombieArm) for arm in monster.arms)
    assert any(isinstance(arm, SkeletonArm) for arm in monster.arms)

    # Speed: (ZombieLeg = 3.75, SkeletonLeg = 8.0) -> average
    expected_speed = (3.75 + 8.0) / 2
    assert monster.get_total_speed() == pytest.approx(expected_speed)

    # Attack: (ZombieArm = 8.5, SkeletonArm = 18.75) -> sum
    expected_attack = 8.5 + 18.75
    assert monster.get_total_attack() == pytest.approx(expected_attack)
