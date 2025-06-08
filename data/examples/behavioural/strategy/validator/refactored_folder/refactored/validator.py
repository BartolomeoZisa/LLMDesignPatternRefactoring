import re
from abc import ABC, abstractmethod

class Validator(ABC):
    @abstractmethod
    def validate(self, value: str) -> bool:
        pass

class NumericValidator(Validator):
    def validate(self, value: str) -> bool:
        return value.isdigit()

class AlphanumericValidator(Validator):
    def validate(self, value: str) -> bool:
        return value.isalnum()

class TelNumberValidator(Validator):
    TEL_PATTERN = re.compile(r'^\+?[\d\s\-\(\)]+$')

    def validate(self, value: str) -> bool:
        if not value:
            return False
        return bool(self.TEL_PATTERN.match(value))


class ValidationContext:
    def __init__(self):
        self.current_strategy: Validator = None

    def set_strategy(self, strategy: Validator) -> None:
        if not isinstance(strategy, Validator):
            raise TypeError("Strategy must be a subclass of Validator.")
        self.current_strategy = strategy
    def validate(self, value: str) -> bool:
        if self.current_strategy is None:
            raise RuntimeError("Validation strategy not set.")
        return self.current_strategy.validate(value)


        