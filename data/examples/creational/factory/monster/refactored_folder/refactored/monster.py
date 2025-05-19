from abc import ABC, abstractmethod


# Abstract Base Class for Legs
class Leg(ABC):
    def __init__(self, base_speed, speed_modifier):
        self.base_speed = base_speed
        self.speed_modifier = speed_modifier

    def get_speed(self):
        return self.base_speed * self.speed_modifier

    def __str__(self):
        return f"Speed: {self.get_speed()}"

# Abstract Base Class for Arms
class Arm(ABC):
    def __init__(self, base_attack, attack_modifier):
        self.base_attack = base_attack
        self.attack_modifier = attack_modifier

    def get_attack_power(self):
        return self.base_attack * self.attack_modifier

    def __str__(self):
        return f"Attack: {self.get_attack_power()}"

# ------------------------------
# Concrete Subclasses for Legs
# ------------------------------

class ZombieLeg(Leg):
    def __init__(self):
        super().__init__(base_speed=5, speed_modifier=0.75)


class SkeletonLeg(Leg):
    def __init__(self):
        super().__init__(base_speed=8, speed_modifier=1.00)


# ------------------------------
# Concrete Subclasses for Arms
# ------------------------------

class ZombieArm(Arm):
    def __init__(self):
        super().__init__(base_attack=10, attack_modifier=0.85)


class SkeletonArm(Arm):
    def __init__(self):
        super().__init__(base_attack=12, attack_modifier=1.10)

    def __init__(self):
        super().__init__(base_attack=15, attack_modifier=1.25)

# ------------------------------
# Monster Class
# ------------------------------

class Monster:
    def __init__(self, name, legs, arms):
        self.name = name
        self.legs = legs
        self.arms = arms

    def get_total_speed(self):
        total_speed_values = [leg.base_speed * leg.speed_modifier for leg in self.legs]
        return sum(total_speed_values) / len(total_speed_values)

    def get_total_attack(self):
        return sum(arm.base_attack * arm.attack_modifier for arm in self.arms)

    def __str__(self):
        return (f"{self.name}:\n"
                f"  Legs: {[str(leg) for leg in self.legs]}\n"
                f"  Arms: {[str(arm) for arm in self.arms]}\n"
                f"  Total Speed: {self.get_total_speed()}\n"
                f"  Total Attack: {self.get_total_attack()}")

# ------------------------------
# Monster Factory Classes
# ------------------------------

class MonsterFactory(ABC):
    # These methods will now return mixed legs and arms
    @abstractmethod
    def create_right_leg(self):
        pass
    @abstractmethod
    def create_left_leg(self):
        pass
    @abstractmethod
    def create_right_arm(self):
        pass
    @abstractmethod 
    def create_left_arm(self):
        pass

    def create_monster(self, name):
        # Creating a monster with mixed legs and arms
        
        legs = [self.create_left_leg(), self.create_right_leg()]
        arms = [self.create_left_arm(), self.create_right_arm()]
        return Monster(name, legs, arms)

# Concrete Factory for Mixed Monsters
class SkeletonFactory(MonsterFactory):
    def create_right_leg(self):
        return SkeletonLeg()

    def create_left_leg(self):
        return SkeletonLeg()

    def create_right_arm(self):
        return SkeletonArm()

    def create_left_arm(self):
        return SkeletonArm()
    
class ZombieFactory(MonsterFactory):
    def create_right_leg(self):
        return ZombieLeg()

    def create_left_leg(self):
        return ZombieLeg()

    def create_right_arm(self):
        return ZombieArm()

    def create_left_arm(self):
        return ZombieArm()

class GhoulFactory(MonsterFactory):
    def create_right_leg(self):
        return ZombieLeg()

    def create_left_leg(self):
        return SkeletonLeg()

    def create_right_arm(self):
        return ZombieArm()

    def create_left_arm(self):
        return SkeletonArm()


