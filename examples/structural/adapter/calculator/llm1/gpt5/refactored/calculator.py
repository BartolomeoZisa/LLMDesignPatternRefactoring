class Calculator:
    def add(self, a, b):
        return self.operation(a, b, "add")

    def subtract(self, a, b):
        return self.operation(a, b, "sub")

    def multiply(self, a, b):
        return self.operation(a, b, "mul")

    def divide(self, a, b):
        return self.operation(a, b, "div")


class CalculatorAdapter(Calculator):
    def __init__(self, old_calculator):
        self.old_calculator = old_calculator

    def operation(self, a, b, op):
        return self.old_calculator.operation(a, b, op)