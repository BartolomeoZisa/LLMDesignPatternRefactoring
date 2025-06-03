from abc import ABC, abstractmethod

# Base Component
class Sword(ABC):
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def damage(self) -> int:
        pass

# Concrete Component
class BasicSword(Sword):
    def description(self) -> str:
        return "Basic sword"

    def damage(self) -> int:
        return 10

# Base Decorator
class SwordDecorator(Sword):
    def __init__(self, sword: Sword):
        self._sword = sword

    def description(self) -> str:
        return self._sword.description()

    def damage(self) -> int:
        return self._sword.damage()

# Concrete Decorators
class FlamingDecorator(SwordDecorator):
    def description(self) -> str:
        return self._sword.description() + ", with flames"

    def damage(self) -> int:
        return self._sword.damage() + 5

class PoisonedDecorator(SwordDecorator):
    def description(self) -> str:
        return self._sword.description() + ", coated in poison"

    def damage(self) -> int:
        return self._sword.damage() + 3

class IceDecorator(SwordDecorator):
    def description(self) -> str:
        return self._sword.description() + ", imbued with ice"

    def damage(self) -> int:
        return self._sword.damage() + 4
