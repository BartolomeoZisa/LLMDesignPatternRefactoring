class IceCreamComponent:
    """Abstract Component class for Ice Cream."""
    def cost(self):
        raise NotImplementedError("Subclasses must implement the cost method.")

    def getDescription(self):
        raise NotImplementedError("Subclasses must implement the getDescription method.")


class Cone(IceCreamComponent):
    """Concrete Component for Cone."""
    def cost(self):
        return 1.00

    def getDescription(self):
        return "Icecream Cone"


class Cup(IceCreamComponent):
    """Concrete Component for Cup."""
    def cost(self):
        return 1.50

    def getDescription(self):
        return "Icecream Cup"


class IceCreamDecorator(IceCreamComponent):
    """Abstract Decorator class for Ice Cream."""
    def __init__(self, component):
        self.component = component

    def cost(self):
        return self.component.cost()

    def getDescription(self):
        return self.component.getDescription()


class Chocolate(IceCreamDecorator):
    """Concrete Decorator for Chocolate flavor."""
    def cost(self):
        return self.component.cost() + 0.50

    def getDescription(self):
        return f"{self.component.getDescription()}, Chocolate"


class Strawberry(IceCreamDecorator):
    """Concrete Decorator for Strawberry flavor."""
    def cost(self):
        return self.component.cost() + 0.75

    def getDescription(self):
        return f"{self.component.getDescription()}, Strawberry"


class Vanilla(IceCreamDecorator):
    """Concrete Decorator for Vanilla flavor."""
    def cost(self):
        return self.component.cost() + 0.60

    def getDescription(self):
        return f"{self.component.getDescription()}, Vanilla"
