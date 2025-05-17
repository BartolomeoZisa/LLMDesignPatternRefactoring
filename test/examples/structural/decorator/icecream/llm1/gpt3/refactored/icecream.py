class IceCream:
    def cost(self):
        raise NotImplementedError

    def getDescription(self):
        raise NotImplementedError


class Cone(IceCream):
    def cost(self):
        return IceCream.CONTAINER_PRICES['cone']

    def getDescription(self):
        return "Icecream Cone"


class Cup(IceCream):
    def cost(self):
        return IceCream.CONTAINER_PRICES['cup']

    def getDescription(self):
        return "Icecream Cup"


class IceCreamDecorator(IceCream):
    def __init__(self, ice_cream):
        self._ice_cream = ice_cream

    def cost(self):
        return self._ice_cream.cost()

    def getDescription(self):
        return self._ice_cream.getDescription()


class Chocolate(IceCreamDecorator):
    def cost(self):
        return self._ice_cream.cost() + IceCream.FLAVOR_PRICES['chocolate']

    def getDescription(self):
        return f"{self._ice_cream.getDescription()}, Chocolate"


class Strawberry(IceCreamDecorator):
    def cost(self):
        return self._ice_cream.cost() + IceCream.FLAVOR_PRICES['strawberry']

    def getDescription(self):
        return f"{self._ice_cream.getDescription()}, Strawberry"


class Vanilla(IceCreamDecorator):
    def cost(self):
        return self._ice_cream.cost() + IceCream.FLAVOR_PRICES['vanilla']

    def getDescription(self):
        return f"{self._ice_cream.getDescription()}, Vanilla"