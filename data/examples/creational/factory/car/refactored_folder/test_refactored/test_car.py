import pytest
from refactored.car import (
    SportsCarFactory, EconomyCarFactory,
    SportsEngine, EconomyEngine,
    SportsTank, EconomyTank,
    Car
)

def test_sports_car_creation():
    factory = SportsCarFactory()
    car = factory.create_car()

    assert isinstance(car.engine, SportsEngine)
    assert isinstance(car.tank, SportsTank)
    assert car.engine.speed == 250
    assert car.engine.fuel_consumption_per_km == 0.2
    assert car.tank.capacity == 50
    assert car.tank.fuel == 50

def test_economy_car_creation():
    factory = EconomyCarFactory()
    car = factory.create_car()

    assert isinstance(car.engine, EconomyEngine)
    assert isinstance(car.tank, EconomyTank)
    assert car.engine.speed == 120
    assert car.engine.fuel_consumption_per_km == 0.05
    assert car.tank.capacity == 40
    assert car.tank.fuel == 40

def test_car_travel_within_fuel_range():
    car = SportsCarFactory().create_car()
    car.travel(100)  # should consume 20L

    assert car.check_kms() == 100
    assert car.tank.fuel == 30

def test_car_travel_exceeding_fuel_range():
    car = EconomyCarFactory().create_car()
    car.travel(1000)  # requires 50L, but has only 40L

    assert car.check_kms() == 0
    assert car.tank.fuel == 40  # unchanged

def test_car_refill():
    car = EconomyCarFactory().create_car()
    car.travel(200)  # uses 10L
    assert car.tank.fuel == 30

    car.tank.refill()
    assert car.tank.fuel == 40

def test_multiple_travels_accumulate_distance():
    car = SportsCarFactory().create_car()
    car.travel(50)
    car.travel(100)

    assert car.check_kms() == 150

# -------------------------
# Edge Case Tests
# -------------------------

def test_zero_distance_travel():
    car = SportsCarFactory().create_car()
    initial_fuel = car.tank.fuel

    car.travel(0)
    assert car.check_kms() == 0
    assert car.tank.fuel == initial_fuel  # no fuel used

def test_travel_exact_fuel_limit():
    car = EconomyCarFactory().create_car()
    max_distance = car.tank.fuel / car.engine.fuel_consumption_per_km  # 40 / 0.05 = 800

    car.travel(max_distance)
    assert pytest.approx(car.check_kms()) == 800
    assert pytest.approx(car.tank.fuel) == 0

def test_travel_with_zero_fuel():
    car = SportsCarFactory().create_car()
    car.tank.fuel = 0  # manually empty tank
    car.travel(10)

    assert car.check_kms() == 0
    assert car.tank.fuel == 0

def test_refill_after_empty_travel():
    car = EconomyCarFactory().create_car()
    car.tank.fuel = 0
    car.tank.refill()

    assert car.tank.fuel == car.tank.capacity

def test_floating_point_precision_travel():
    car = EconomyCarFactory().create_car()
    car.travel(0.1)  # should consume 0.005L
    assert pytest.approx(car.tank.fuel, 0.0001) == 39.995
