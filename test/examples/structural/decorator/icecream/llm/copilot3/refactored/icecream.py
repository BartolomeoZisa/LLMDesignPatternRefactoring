class IceCream:
    def cost(self):
        raise NotImplementedError("Subclasses must implement this method")

    def getDescription(self):
        raise NotImplementedError("Subclasses must implement this method")


class Cone(IceCream):
    def cost(self):
        return 1.00

    def getDescription(self):
        return "Icecream Cone"


class Cup(IceCream):
    def cost(self):
        return 1.50

    def getDescription(self):
        return "Icecream Cup"


class FlavorDecorator(IceCream):
    def __init__(self, icecream):
        self._icecream = icecream

    def cost(self):
        return self._icecream.cost()

    def getDescription(self):
        return self._icecream.getDescription()


class Chocolate(FlavorDecorator):
    def cost(self):
        return self._icecream.cost() + 0.50

    def getDescription(self):
        return f"{self._icecream.getDescription()}, Chocolate"


class Strawberry(FlavorDecorator):
    def cost(self):
        return self._icecream.cost() + 0.75

    def getDescription(self):
        return f"{self._icecream.getDescription()}, Strawberry"


class Vanilla(FlavorDecorator):
    def cost(self):
        return self._icecream.cost() + 0.60

    def getDescription(self):
        return f"{self._icecream.getDescription()}, Vanilla"
