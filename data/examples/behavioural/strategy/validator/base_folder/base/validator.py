import re

class ValidationContext:
    def __init__(self):
        self.current_strategy = None
        self._tel_pattern = re.compile(r'^\+?[\d\s\-\(\)]+$')

    def set_strategy(self, strategy_name: str):
        if strategy_name not in {"numeric", "alphanumeric", "telnumber"}:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        self.current_strategy = strategy_name

    def validate(self, value: str) -> bool:
        if self.current_strategy is None:
            raise RuntimeError("No strategy set")

        if self.current_strategy == "numeric":
            return self._validate_numeric(value)
        elif self.current_strategy == "alphanumeric":
            return self._validate_alphanumeric(value)
        elif self.current_strategy == "telnumber":
            return self._validate_telnumber(value)

    def _validate_numeric(self, value: str) -> bool:
        return value.isdigit()

    def _validate_alphanumeric(self, value: str) -> bool:
        return value.isalnum()

    def _validate_telnumber(self, value: str) -> bool:
        if not value:
            return False
        return bool(self._tel_pattern.match(value))


