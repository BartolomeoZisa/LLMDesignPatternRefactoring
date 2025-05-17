class IceCream:
    def cost(self):
        raise NotImplementedError("Subclass must implement abstract method.")
    
    def getDescription(self):
        raise NotImplementedError("Subclass must implement abstract method.")

class BaseIceCream(IceCream):
    CONTAINER_PRICES = {
        "cone": 1.00,
        "cup": 1.50
    }
    
    FLAVOR_PRICES = {
        "chocolate": 0.50,
        "strawberry": 0.75,
        "vanilla": 0.60
    }
    
    def __init__(self, container, scoops=None):
        if container not in BaseIceCream.CONTAINER_PRICES:
            raise ValueError(f"Invalid container type '{container}'. Choose 'cone' or 'cup'.")
        
        if scoops is None:
            scoops = []
        
        for flavor in scoops:
            if flavor not in BaseIceCream.FLAVOR_PRICES:
                raise ValueError(f"Invalid flavor '{flavor}'. Choose from {list(BaseIceCream.FLAVOR_PRICES.keys())}.")
        
        self.container = container
        self.scoops = scoops
        self.description = f"Icecream {self.container.capitalize()}, {', '.join(flavor.capitalize() for flavor in self.scoops)}"
    
    def cost(self):
        total_cost = BaseIceCream.CONTAINER_PRICES[self.container]
        for flavor in self.scoops:
            total_cost += BaseIceCream.FLAVOR_PRICES[flavor]
        return total_cost
    
    def getDescription(self):
        return self.description

class Decorator(IceCream):
    def __init__(self, icecream):
        self._icecream = icecream

    def cost(self):
        return self._icecream.cost()
    
    def getDescription(self):
        return self._icecream.getDescription()

class Cone(BaseIceCream):
    def __init__(self):
        super().__init__("cone")

class Cup(BaseIceCream):
    def __init__(self):
        super().__init__("cup")

class Chocolate(Decorator):
    def __init__(self, icecream):
        super().__init__(icecream)
        self._flavor = "chocolate"
    
    def cost(self):
        return self._icecream.cost() + BaseIceCream.FLAVOR_PRICES[self._flavor]
    
    def getDescription(self):
        return f"{self._icecream.getDescription()}, {self._flavor.capitalize()}"

class Strawberry(Decorator):
    def __init__(self, icecream):
        super().__init__(icecream)
        self._flavor = "strawberry"
    
    def cost(self):
        return self._icecream.cost() + BaseIceCream.FLAVOR_PRICES[self._flavor]
    
    def getDescription(self):
        return f"{self._icecream.getDescription()}, {self._flavor.capitalize()}"

class Vanilla(Decorator):
    def __init__(self, icecream):
        super().__init__(icecream)
        self._flavor = "vanilla"
    
    def cost(self):
        return self._icecream.cost() + BaseIceCream.FLAVOR_PRICES[self._flavor]
    
    def getDescription(self):
        return f"{self._icecream.getDescription()}, {self._flavor.capitalize()}"
