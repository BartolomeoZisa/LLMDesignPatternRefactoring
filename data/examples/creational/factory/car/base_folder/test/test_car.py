import pytest
from base.car import (
    CarFactory,
    SportsEngine, EconomyEngine,
    SportsTank, EconomyTank,
)

def test_sports_car_creation():
    factory = CarFactory()
    car = factory.create_car("sports")

    assert isinstance(car.engine, SportsEngine)
    assert isinstance(car.tank, SportsTank)
    assert car.engine.speed == 250
    assert car.engine.fuel_consumption_per_km == 0.2
    assert car.tank.capacity == 50
    assert car.tank.fuel == 50

def test_economy_car_creation():
    factory = CarFactory()
    car = factory.create_car("economy")

    assert isinstance(car.engine, EconomyEngine)
    assert isinstance(car.tank, EconomyTank)
    assert car.engine.speed == 120
    assert car.engine.fuel_consumption_per_km == 0.05
    assert car.tank.capacity == 40
    assert car.tank.fuel == 40

def test_car_travel_within_fuel_range():
    car = CarFactory().create_car("sports")
    car.travel(100)
    assert car.check_kms() == 100
    assert car.tank.fuel == 30

def test_car_travel_exceeding_fuel_range():
    car = CarFactory().create_car("economy")
    car.travel(1000)
    assert car.check_kms() == 0
    assert car.tank.fuel == 40

def test_car_refill():
    car = CarFactory().create_car("economy")
    car.travel(200)
    assert car.tank.fuel == 30
    car.tank.refill()
    assert car.tank.fuel == 40

def test_multiple_travels_accumulate_distance():
    car = CarFactory().create_car("sports")
    car.travel(50)
    car.travel(100)
    assert car.check_kms() == 150

# -------------------------
# Edge Case Tests
# -------------------------

def test_zero_distance_travel():
    car = CarFactory().create_car("sports")
    initial_fuel = car.tank.fuel
    car.travel(0)
    assert car.check_kms() == 0
    assert car.tank.fuel == initial_fuel

def test_travel_exact_fuel_limit():
    car = CarFactory().create_car("economy")
    max_distance = car.tank.fuel / car.engine.fuel_consumption_per_km
    car.travel(max_distance)
    assert pytest.approx(car.check_kms()) == 800
    assert pytest.approx(car.tank.fuel) == 0

def test_travel_with_zero_fuel():
    car = CarFactory().create_car("sports")
    car.tank.fuel = 0
    car.travel(10)
    assert car.check_kms() == 0
    assert car.tank.fuel == 0

def test_refill_after_empty_travel():
    car = CarFactory().create_car("economy")
    car.tank.fuel = 0
    car.tank.refill()
    assert car.tank.fuel == car.tank.capacity

def test_floating_point_precision_travel():
    car = CarFactory().create_car("economy")
    car.travel(0.1)
    assert pytest.approx(car.tank.fuel, 0.0001) == 39.995

