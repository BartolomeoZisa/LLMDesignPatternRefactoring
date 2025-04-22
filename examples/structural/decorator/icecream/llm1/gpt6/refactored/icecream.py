class IceCream:
    def cost(self):
        raise NotImplementedError

    def getDescription(self):
        raise NotImplementedError


class Cone(IceCream):
    def __init__(self):
        self.container = "cone"

    def cost(self):
        return IceCream.CONTAINER_PRICES[self.container]

    def getDescription(self):
        return f"Icecream {self.container.capitalize()}"


class Cup(IceCream):
    def __init__(self):
        self.container = "cup"

    def cost(self):
        return IceCream.CONTAINER_PRICES[self.container]

    def getDescription(self):
        return f"Icecream {self.container.capitalize()}"


class FlavorDecorator(IceCream):
    def __init__(self, ice_cream):
        self.ice_cream = ice_cream

    def cost(self):
        return self.ice_cream.cost()

    def getDescription(self):
        return self.ice_cream.getDescription()


class Chocolate(FlavorDecorator):
    def cost(self):
        return self.ice_cream.cost() + IceCream.FLAVOR_PRICES["chocolate"]

    def getDescription(self):
        return f"{self.ice_cream.getDescription()}, Chocolate"


class Strawberry(FlavorDecorator):
    def cost(self):
        return self.ice_cream.cost() + IceCream.FLAVOR_PRICES["strawberry"]

    def getDescription(self):
        return f"{self.ice_cream.getDescription()}, Strawberry"


class Vanilla(FlavorDecorator):
    def cost(self):
        return self.ice_cream.cost() + IceCream.FLAVOR_PRICES["vanilla"]

    def getDescription(self):
        return f"{self.ice_cream.getDescription()}, Vanilla"