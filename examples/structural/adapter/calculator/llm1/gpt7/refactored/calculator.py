class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b


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