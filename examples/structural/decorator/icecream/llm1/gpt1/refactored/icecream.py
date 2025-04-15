```python
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


class FlavorDecorator(IceCream):
    def __init__(self, ice_cream):
        self._ice_cream = ice_cream

    def cost(self):
        return self._ice_cream.cost()

    def getDescription(self):
        return self._ice_cream.getDescription()


class Chocolate(FlavorDecorator):
    def cost(self):
        return super().cost() + IceCream.FLAVOR_PRICES['chocolate']

    def getDescription(self):
        return super().getDescription() + ", Chocolate"


class Strawberry(FlavorDecorator):
    def cost(self):
        return super().cost() + IceCream.FLAVOR_PRICES['strawberry']

    def getDescription(self):
        return super().getDescription() + ", Strawberry"


class Vanilla(FlavorDecorator):
    def cost(self):
        return super().cost() + IceCream.FLAVOR_PRICES['vanilla']

    def getDescription(self):
        return super().getDescription() + ", Vanilla"


IceCream.CONTAINER_PRICES = {
    "cone": 1.00,
    "cup": 1.50
}

IceCream.FLAVOR_PRICES = {
    "chocolate": 0.50,
    "strawberry": 0.75,
    "vanilla": 0.60
}
```