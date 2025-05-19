from abc import ABC, abstractmethod


# ------------------------------
# Abstract Base Classes
# ------------------------------

class Leg(ABC):
    def __init__(self, base_speed, speed_modifier):
        self.base_speed = base_speed
        self.speed_modifier = speed_modifier

    def get_speed(self):
        return self.base_speed * self.speed_modifier

    def __str__(self):
        return f"Speed: {self.get_speed():.2f}"


class Arm(ABC):
    def __init__(self, base_attack, attack_modifier):
        self.base_attack = base_attack
        self.attack_modifier = attack_modifier

    def get_attack_power(self):
        return self.base_attack * self.attack_modifier

    def __str__(self):
        return f"Attack: {self.get_attack_power():.2f}"


# ------------------------------
# Concrete Leg Classes
# ------------------------------

class ZombieLeg(Leg):
    def __init__(self):
        super().__init__(base_speed=5, speed_modifier=0.75)


class SkeletonLeg(Leg):
    def __init__(self):
        super().__init__(base_speed=8, speed_modifier=1.00)


# ------------------------------
# Concrete Arm Classes
# ------------------------------

class ZombieArm(Arm):
    def __init__(self):
        super().__init__(base_attack=10, attack_modifier=0.85)


class SkeletonArm(Arm):
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
        return sum(leg.get_speed() for leg in self.legs) / len(self.legs)

    def get_total_attack(self):
        return sum(arm.get_attack_power() for arm in self.arms)

    def __str__(self):
        legs_str = ", ".join(str(leg) for leg in self.legs)
        arms_str = ", ".join(str(arm) for arm in self.arms)
        return (f"{self.name}:\n"
                f"  Legs: {legs_str}\n"
                f"  Arms: {arms_str}\n"
                f"  Total Speed: {self.get_total_speed():.2f}\n"
                f"  Total Attack: {self.get_total_attack():.2f}")


# ------------------------------
# Factory Method Pattern
# ------------------------------

class MonsterFactory(ABC):
    @abstractmethod
    def create_leg(self):
        pass

    @abstractmethod
    def create_arm(self):
        pass

    def create_monster(self, name):
        legs = [self.create_leg() for _ in range(2)]
        arms = [self.create_arm() for _ in range(2)]
        return Monster(name, legs, arms)


class ZombieFactory(MonsterFactory):
    def create_leg(self):
        return ZombieLeg()

    def create_arm(self):
        return ZombieArm()


class SkeletonFactory(MonsterFactory):
    def create_leg(self):
        return SkeletonLeg()

    def create_arm(self):
        return SkeletonArm()


class GhoulFactory(MonsterFactory):
    def create_leg(self):
        # Alternates between ZombieLeg and SkeletonLeg
        if not hasattr(self, '_leg_toggle'):
            self._leg_toggle = False
        self._leg_toggle = not self._leg_toggle
        return ZombieLeg() if self._leg_toggle else SkeletonLeg()

    def create_arm(self):
        # Alternates between ZombieArm and SkeletonArm
        if not hasattr(self, '_arm_toggle'):
            self._arm_toggle = False
        self._arm_toggle = not self._arm_toggle
        return ZombieArm() if self._arm_toggle else SkeletonArm()
