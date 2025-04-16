class CalculatorAdapter:
    def __init__(self, old_calculator):
        self._old_calculator = old_calculator

    def add(self, a, b):
        return self._old_calculator.operation(a, b, "add")

    def subtract(self, a, b):
        return self._old_calculator.operation(a, b, "sub")

    def multiply(self, a, b):
        return self._old_calculator.operation(a, b, "mul")

    def divide(self, a, b):
        return self._old_calculator.operation(a, b, "div")