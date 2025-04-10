
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



