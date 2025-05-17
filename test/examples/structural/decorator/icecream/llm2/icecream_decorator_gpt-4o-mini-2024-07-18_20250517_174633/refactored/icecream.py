class IceCream:
    CONTAINER_PRICES = {
        "cone": 1.00,
        "cup": 1.50
    }
    
    def __init__(self, container):
        if container not in IceCream.CONTAINER_PRICES:
            raise ValueError(f"Invalid container type '{container}'. Choose 'cone' or 'cup'.")
        
        self.container = container
        self.scoops = []
        self.description = f"Icecream {self.container.capitalize()}"

    def add_scoop(self, flavor):
        if flavor not in IceCream.FLAVOR_PRICES:
            raise ValueError(f"Invalid flavor '{flavor}'. Choose from {list(IceCream.FLAVOR_PRICES.keys())}.")
        self.scoops.append(flavor)
        self.description += f", {flavor.capitalize()}"

    def cost(self):
        total_cost = IceCream.CONTAINER_PRICES[self.container]
        for flavor in self.scoops:
            total_cost += IceCream.FLAVOR_PRICES[flavor]
        return total_cost
    
    def getDescription(self):
        return self.description

class Decorator(IceCream):
    def __init__(self, ice_cream):
        self._ice_cream = ice_cream

    def cost(self):
        return self._ice_cream.cost()

    def getDescription(self):
        return self._ice_cream.getDescription()

class Cone(IceCream):
    def __init__(self):
        super().__init__("cone")

class Cup(IceCream):
    def __init__(self):
        super().__init__("cup")

class Chocolate(Decorator):
    def __init__(self, ice_cream):
        super().__init__(ice_cream)
        self._ice_cream.add_scoop("chocolate")

class Strawberry(Decorator):
    def __init__(self, ice_cream):
        super().__init__(ice_cream)
        self._ice_cream.add_scoop("strawberry")

class Vanilla(Decorator):
    def __init__(self, ice_cream):
        super().__init__(ice_cream)
        self._ice_cream.add_scoop("vanilla")