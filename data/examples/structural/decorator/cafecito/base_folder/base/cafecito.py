class Beverage:
    def __init__(self, description="Unknown Beverage", base_cost=0.0):
        self.description = description
        self.base_cost = base_cost
        self.condiments = []  # List of dicts: {"name": ..., "cost": ...}

    def add_condiment(self, name, cost):
        self.condiments.append({"name": name, "cost": cost})

    def get_description(self):
        if not self.condiments:
            return self.description
        cond_names = ", ".join([c["name"] for c in self.condiments])
        return f"{self.description}, {cond_names}"

    def cost(self):
        total = self.base_cost + sum(c["cost"] for c in self.condiments)
        return total


# Concrete beverages
class Espresso(Beverage):
    def __init__(self):
        super().__init__("Espresso", 1.99)


class HouseBlend(Beverage):
    def __init__(self):
        super().__init__("House Blend Coffee", 0.89)


class DarkRoast(Beverage):
    def __init__(self):
        super().__init__("Dark Roast Coffee", 0.99)


class Decaf(Beverage):
    def __init__(self):
        super().__init__("Decaf Coffee", 1.05)
