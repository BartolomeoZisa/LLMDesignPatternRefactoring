class IceCream:
    def cost(self):
        pass

    def getDescription(self):
        pass

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

class IceCreamDecorator(IceCream):
    def __init__(self, ice_cream):
        self.ice_cream = ice_cream

    def cost(self):
        return self.ice_cream.cost()

    def getDescription(self):
        return self.ice_cream.getDescription()

class Chocolate(IceCreamDecorator):
    def __init__(self, ice_cream):
        super().__init__(ice_cream)

    def cost(self):
        return super().cost() + IceCream.FLAVOR_PRICES["chocolate"]

    def getDescription(self):
        return super().getDescription() + ", Chocolate"

class Strawberry(IceCreamDecorator):
    def __init__(self, ice_cream):
        super().__init__(ice_cream)

    def cost(self):
        return super().cost() + IceCream.FLAVOR_PRICES["strawberry"]

    def getDescription(self):
        return super().getDescription() + ", Strawberry"

class Vanilla(IceCreamDecorator):
    def __init__(self, ice_cream):
        super().__init__(ice_cream)

    def cost(self):
        return super().cost() + IceCream.FLAVOR_PRICES["vanilla"]

    def getDescription(self):
        return super().getDescription() + ", Vanilla"