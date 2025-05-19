class Calculator:
    def add(self, a, b):
        pass

    def subtract(self, a, b):
        pass

    def multiply(self, a, b):
        pass

    def divide(self, a, b):
        pass


class CalculatorAdapter(Calculator):
    def __init__(self, old_calculator):
        self.old_calculator = old_calculator

    def add(self, a, b):
        return self.old_calculator.operation(a, b, "add")

    def subtract(self, a, b):
        return self.old_calculator.operation(a, b, "sub")

    def multiply(self, a, b):
        return self.old_calculator.operation(a, b, "mul")

    def divide(self, a, b):
        return self.old_calculator.operation(a, b, "div")