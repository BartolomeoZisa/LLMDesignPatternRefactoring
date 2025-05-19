class IceCream:
    # Prices for containers
    CONTAINER_PRICES = {
        "cone": 1.00,
        "cup": 1.50
    }

    def __init__(self, container):
        if container not in IceCream.CONTAINER_PRICES:
            raise ValueError(f"Invalid container type '{container}'. Choose 'cone' or 'cup'.")
        self.container = container

    def cost(self):
        return IceCream.CONTAINER_PRICES[self.container]

    def getDescription(self):
        return f"Icecream {self.container.capitalize()}"


class FlavorDecorator:
    def __init__(self, icecream):
        self.icecream = icecream

    def cost(self):
        return self.icecream.cost()

    def getDescription(self):
        return self.icecream.getDescription()


class Chocolate(FlavorDecorator):
    FLAVOR_PRICE = 0.50

    def cost(self):
        return self.icecream.cost() + Chocolate.FLAVOR_PRICE

    def getDescription(self):
        return f"{self.icecream.getDescription()}, Chocolate"


class Strawberry(FlavorDecorator):
    FLAVOR_PRICE = 0.75

    def cost(self):
        return self.icecream.cost() + Strawberry.FLAVOR_PRICE

    def getDescription(self):
        return f"{self.icecream.getDescription()}, Strawberry"


class Vanilla(FlavorDecorator):
    FLAVOR_PRICE = 0.60

    def cost(self):
        return self.icecream.cost() + Vanilla.FLAVOR_PRICE

    def getDescription(self):
        return f"{self.icecream.getDescription()}, Vanilla"


class Cone(IceCream):
    def __init__(self):
        super().__init__("cone")


class Cup(IceCream):
    def __init__(self):
        super().__init__("cup")