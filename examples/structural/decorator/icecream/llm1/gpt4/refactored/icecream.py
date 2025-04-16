class IceCream:
    CONTAINER_PRICES = {
        "cone": 1.00,
        "cup": 1.50
    }
    
    def __init__(self, container):
        if container not in IceCream.CONTAINER_PRICES:
            raise ValueError(f"Invalid container type '{container}'. Choose 'cone' or 'cup'.")
        self.container = container
        self.description = f"Icecream {self.container.capitalize()}"
    
    def cost(self):
        return IceCream.CONTAINER_PRICES[self.container]
    
    def getDescription(self):
        return self.description


class FlavorDecorator:
    def __init__(self, ice_cream):
        self.ice_cream = ice_cream

    def cost(self):
        return self.ice_cream.cost()

    def getDescription(self):
        return self.ice_cream.getDescription()


class Chocolate(FlavorDecorator):
    FLAVOR_PRICE = 0.50

    def cost(self):
        return self.ice_cream.cost() + Chocolate.FLAVOR_PRICE

    def getDescription(self):
        return f"{self.ice_cream.getDescription()}, Chocolate"


class Strawberry(FlavorDecorator):
    FLAVOR_PRICE = 0.75

    def cost(self):
        return self.ice_cream.cost() + Strawberry.FLAVOR_PRICE

    def getDescription(self):
        return f"{self.ice_cream.getDescription()}, Strawberry"


class Vanilla(FlavorDecorator):
    FLAVOR_PRICE = 0.60

    def cost(self):
        return self.ice_cream.cost() + Vanilla.FLAVOR_PRICE

    def getDescription(self):
        return f"{self.ice_cream.getDescription()}, Vanilla"


class Cone(IceCream):
    def __init__(self):
        super().__init__("cone")


class Cup(IceCream):
    def __init__(self):
        super().__init__("cup")