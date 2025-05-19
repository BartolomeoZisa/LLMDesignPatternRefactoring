class IceCream:
    """Base class for IceCream components."""
    def cost(self):
        """Calculate and return the total cost of the ice cream."""
        raise NotImplementedError("This method should be implemented by the decorator.")

    def getDescription(self):
        """Return a simplified description in the format 'Icecream Container, Flavor1, Flavor2'."""
        raise NotImplementedError("This method should be implemented by the decorator.")

class Cone(IceCream):
    """Concrete IceCream component representing a cone."""
    CONTAINER_PRICE = 1.00

    def cost(self):
        return self.CONTAINER_PRICE

    def getDescription(self):
        return "Icecream Cone"


class Cup(IceCream):
    """Concrete IceCream component representing a cup."""
    CONTAINER_PRICE = 1.50

    def cost(self):
        return self.CONTAINER_PRICE

    def getDescription(self):
        return "Icecream Cup"


class IceCreamDecorator(IceCream):
    """Base decorator class for extending IceCream functionality."""
    def __init__(self, ice_cream):
        self._ice_cream = ice_cream

    def cost(self):
        return self._ice_cream.cost()

    def getDescription(self):
        return self._ice_cream.getDescription()


class Chocolate(IceCreamDecorator):
    """Decorator for adding chocolate flavor to the IceCream."""
    FLAVOR_PRICE = 0.50

    def cost(self):
        return self._ice_cream.cost() + self.FLAVOR_PRICE

    def getDescription(self):
        return f"{self._ice_cream.getDescription()}, Chocolate"


class Strawberry(IceCreamDecorator):
    """Decorator for adding strawberry flavor to the IceCream."""
    FLAVOR_PRICE = 0.75

    def cost(self):
        return self._ice_cream.cost() + self.FLAVOR_PRICE

    def getDescription(self):
        return f"{self._ice_cream.getDescription()}, Strawberry"


class Vanilla(IceCreamDecorator):
    """Decorator for adding vanilla flavor to the IceCream."""
    FLAVOR_PRICE = 0.60

    def cost(self):
        return self._ice_cream.cost() + self.FLAVOR_PRICE

    def getDescription(self):
        return f"{self._ice_cream.getDescription()}, Vanilla"
