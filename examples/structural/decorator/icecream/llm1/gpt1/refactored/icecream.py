class IceCream:
    def cost(self):
        raise NotImplementedError

    def getDescription(self):
        raise NotImplementedError


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


class Decorator(IceCream):
    def __init__(self, ice_cream):
        self._ice_cream = ice_cream

    def cost(self):
        return self._ice_cream.cost()

    def getDescription(self):
        return self._ice_cream.getDescription()


class Chocolate(Decorator):
    def cost(self):
        return super().cost() + 0.50

    def getDescription(self):
        return super().getDescription() + ", Chocolate"


class Strawberry(Decorator):
    def cost(self):
        return super().cost() + 0.75

    def getDescription(self):
        return super().getDescription() + ", Strawberry"


class Vanilla(Decorator):
    def cost(self):
        return super().cost() + 0.60

    def getDescription(self):
        return super().getDescription() + ", Vanilla"