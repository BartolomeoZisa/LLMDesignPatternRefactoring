class IceCream:
    def cost(self):
        pass

    def getDescription(self):
        pass


class Cone(IceCream):
    def __init__(self):
        self.container = "cone"
        self.description = f"Icecream {self.container.capitalize()}"

    def cost(self):
        return IceCream.CONTAINER_PRICES[self.container]

    def getDescription(self):
        return self.description


class Cup(IceCream):
    def __init__(self):
        self.container = "cup"
        self.description = f"Icecream {self.container.capitalize()}"

    def cost(self):
        return IceCream.CONTAINER_PRICES[self.container]

    def getDescription(self):
        return self.description


class IceCreamDecorator(IceCream):
    def __init__(self, icecream):
        self.icecream = icecream

    def cost(self):
        return self.icecream.cost()

    def getDescription(self):
        return self.icecream.getDescription()


class Chocolate(IceCreamDecorator):
    def cost(self):
        return self.icecream.cost() + IceCream.FLAVOR_PRICES["chocolate"]

    def getDescription(self):
        return f"{self.icecream.getDescription()}, Chocolate"


class Strawberry(IceCreamDecorator):
    def cost(self):
        return self.icecream.cost() + IceCream.FLAVOR_PRICES["strawberry"]

    def getDescription(self):
        return f"{self.icecream.getDescription()}, Strawberry"


class Vanilla(IceCreamDecorator):
    def cost(self):
        return self.icecream.cost() + IceCream.FLAVOR_PRICES["vanilla"]

    def getDescription(self):
        return f"{self.icecream.getDescription()}, Vanilla"


IceCream.CONTAINER_PRICES = {
    "cone": 1.00,
    "cup": 1.50
}

IceCream.FLAVOR_PRICES = {
    "chocolate": 0.50,
    "strawberry": 0.75,
    "vanilla": 0.60
}