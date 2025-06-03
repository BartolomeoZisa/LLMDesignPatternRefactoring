from abc import ABC, abstractmethod

# Base Engine
class Engine(ABC):
    def __init__(self, speed: float, fuel_consumption_per_km: float):
        self.speed = speed
        self.fuel_consumption_per_km = fuel_consumption_per_km

# Specific Engines
class SportsEngine(Engine):
    def __init__(self):
        super().__init__(speed=250, fuel_consumption_per_km=0.2)

class EconomyEngine(Engine):
    def __init__(self):
        super().__init__(speed=120, fuel_consumption_per_km=0.05)

# Base Fuel Tank
class FuelTank(ABC):
    def __init__(self, capacity: float):
        self.capacity = capacity
        self.fuel = capacity  # Start full

    def consume(self, amount: float) -> bool:
        if amount <= self.fuel:
            self.fuel -= amount
            return True
        return False

    def refill(self):
        self.fuel = self.capacity

# Specific Tanks
class SportsTank(FuelTank):
    def __init__(self):
        super().__init__(capacity=50)

class EconomyTank(FuelTank):
    def __init__(self):
        super().__init__(capacity=40)

# Car class
class Car:
    def __init__(self, engine: Engine, tank: FuelTank):
        self.engine = engine
        self.tank = tank
        self.kms_travelled = 0.0

    def travel(self, kms: float):
        required_fuel = kms * self.engine.fuel_consumption_per_km
        if self.tank.consume(required_fuel):
            self.kms_travelled += kms
            print(f"Travelled {kms} km at {self.engine.speed} km/h.")
        else:
            print("Not enough fuel to travel that distance.")

    def check_kms(self):
        return self.kms_travelled

class CarFactory:
    def create_car(self, car_type: str) -> Car:
        if car_type.lower() == "sports":
            engine = SportsEngine()
            tank = SportsTank()
        elif car_type.lower() == "economy":
            engine = EconomyEngine()
            tank = EconomyTank()
        else:
            raise ValueError(f"Unknown car type: {car_type}")
        return Car(engine, tank)
