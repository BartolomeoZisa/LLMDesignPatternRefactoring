from abc import ABC, abstractmethod

# Defining the interface (abstract base class)
class ICalculator(ABC):
    @abstractmethod
    def add(self, a, b):
        pass

    @abstractmethod
    def subtract(self, a, b):
        pass

    @abstractmethod
    def multiply(self, a, b):
        pass

    @abstractmethod
    def divide(self, a, b):
        pass


# The legacy calculator (old API)
class OldCalculator:
    def operation(self, a, b, op):
        if op == "add":
            return a + b
        elif op == "sub":
            return a - b
        elif op == "mul":
            return a * b
        elif op == "div":
            if b == 0:
                raise ValueError("Division by zero is not allowed")
            return a / b
        else:
            raise ValueError("Unsupported operation")


# The Adapter that implements the ICalculator interface
class CalculatorAdapter(ICalculator):
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



