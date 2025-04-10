# Component Classes
class Leg:
    def __init__(self, base_speed, modifier):
        self.base_speed = base_speed
        self.modifier = modifier

    def get_speed(self):
        return self.base_speed * self.modifier

    def __str__(self):
        return f"Speed: {self.get_speed()}"

class Arm:
    def __init__(self, base_attack, modifier):
        self.base_attack = base_attack
        self.modifier = modifier

    def get_attack(self):
        return self.base_attack * self.modifier

    def __str__(self):
        return f"Attack: {self.get_attack()}"

# Monster Class
class Monster:
    def __init__(self, name, legs, arms):
        self.name = name
        self.legs = legs
        self.arms = arms

    def get_total_speed(self):
        return sum(leg.get_speed() for leg in self.legs) / len(self.legs)

    def get_total_attack(self):
        return sum(arm.get_attack() for arm in self.arms)

    def __str__(self):
        return (f"{self.name}:\n"
                f"  Legs: {[str(leg) for leg in self.legs]}\n"
                f"  Arms: {[str(arm) for arm in self.arms]}\n"
                f"  Total Speed: {self.get_total_speed()}\n"
                f"  Total Attack: {self.get_total_attack()}")

