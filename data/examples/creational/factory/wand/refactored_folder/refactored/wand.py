from abc import ABC, abstractmethod

# Base component classes
class Wood(ABC):
    def __init__(self, mana: int):
        self.mana = mana

class Core(ABC):
    def __init__(self, damage: int):
        self.damage = damage

class Gem(ABC):
    def __init__(self, power: int):
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


# Factory Abstract Class
class WandFactory(ABC):
    @abstractmethod
    def create_wood(self) -> Wood:
        pass

    @abstractmethod
    def create_core(self) -> Core:
        pass

    @abstractmethod
    def create_gem(self) -> Gem:
        pass

    def create_wand(self) -> Wand:
        wood = self.create_wood()
        core = self.create_core()
        gem = self.create_gem()
        return Wand(wood, core, gem)


# Concrete Factories
class OakPhoenixRubyFactory(WandFactory):
    def create_wood(self) -> Wood:
        return Oak()

    def create_core(self) -> Core:
        return PhoenixFeather()

    def create_gem(self) -> Gem:
        return Ruby()

class WillowPhoenixSapphireFactory(WandFactory):
    def create_wood(self) -> Wood:
        return Willow()

    def create_core(self) -> Core:
        return PhoenixFeather()

    def create_gem(self) -> Gem:
        return Sapphire()

class ElderPhoenixEmeraldFactory(WandFactory):
    def create_wood(self) -> Wood:
        return Elder()

    def create_core(self) -> Core:
        return PhoenixFeather()

    def create_gem(self) -> Gem:
        return Emerald()




