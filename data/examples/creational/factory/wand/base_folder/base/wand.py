from abc import ABC

# Base component classes
class Wood(ABC):
    def __init__(self, mana: int):
        self.mana = mana

class Core(ABC):
    def __init__(self, damage: int):
        self.damage = damage

class Gem(ABC):
    def __init__(self, power: float):
        self.power = power


# Concrete Wood classes
class Oak(Wood):
    def __init__(self):
        super().__init__(mana=50)

class Willow(Wood):
    def __init__(self):
        super().__init__(mana=40)

class Elder(Wood):
    def __init__(self):
        super().__init__(mana=70)


# Concrete Core classes
class PhoenixFeather(Core):
    def __init__(self):
        super().__init__(damage=100)


# Concrete Gem classes
class Ruby(Gem):
    def __init__(self):
        super().__init__(power=1)

class Sapphire(Gem):
    def __init__(self):
        super().__init__(power=1.25)

class Emerald(Gem):
    def __init__(self):
        super().__init__(power=1.5)


# Wand product class
class Wand:
    def __init__(self, wood: Wood, core: Core, gem: Gem):
        self.wood = wood
        self.core = core
        self.gem = gem

    @property
    def attack(self):
        return self.wood.mana * (self.core.damage ** self.gem.power)


# Single Factory class with string-based switching
class WandFactory:
    def create_wood(self, wood_type: str) -> Wood:
        wood_type = wood_type.lower()
        if wood_type == "oak":
            return Oak()
        elif wood_type == "willow":
            return Willow()
        elif wood_type == "elder":
            return Elder()
        else:
            raise ValueError(f"Unknown wood type: {wood_type}")

    def create_core(self, core_type: str) -> Core:
        core_type = core_type.lower()
        if core_type == "phoenix":
            return PhoenixFeather()
        else:
            raise ValueError(f"Unknown core type: {core_type}")

    def create_gem(self, gem_type: str) -> Gem:
        gem_type = gem_type.lower()
        if gem_type == "ruby":
            return Ruby()
        elif gem_type == "sapphire":
            return Sapphire()
        elif gem_type == "emerald":
            return Emerald()
        else:
            raise ValueError(f"Unknown gem type: {gem_type}")

    def create_wand(self, wood_type: str, core_type: str, gem_type: str) -> Wand:
        wood = self.create_wood(wood_type)
        core = self.create_core(core_type)
        gem = self.create_gem(gem_type)
        return Wand(wood, core, gem)

