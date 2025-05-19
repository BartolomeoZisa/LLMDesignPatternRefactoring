class IceCream:
    # Prices for containers and flavors
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

class IceCreamDecorator(IceCream):
    def __init__(self, icecream):
        self.icecream = icecream

    def cost(self):
        return self.icecream.cost()
    
    def getDescription(self):
        return self.icecream.getDescription()

class Chocolate(IceCreamDecorator):
    def __init__(self, icecream):
        super().__init__(icecream)

    def cost(self):
        return self.icecream.cost() + 0.50
    
    def getDescription(self):
        return f"{self.icecream.getDescription()}, Chocolate"

class Strawberry(IceCreamDecorator):
    def __init__(self, icecream):
        super().__init__(icecream)

    def cost(self):
        return self.icecream.cost() + 0.75
    
    def getDescription(self):
        return f"{self.icecream.getDescription()}, Strawberry"

class Vanilla(IceCreamDecorator):
    def __init__(self, icecream):
        super().__init__(icecream)

    def cost(self):
        return self.icecream.cost() + 0.60
    
    def getDescription(self):
        return f"{self.icecream.getDescription()}, Vanilla"