class IceCream:
    """Base IceCream class."""
    
    def cost(self):
        """Calculate and return the total cost of the ice cream."""
        raise NotImplementedError

    def getDescription(self):
        """Return a description of the ice cream."""
        raise NotImplementedError


class IceCreamBase(IceCream):
    """Concrete base class for Ice Cream (Cone or Cup)."""
    
    CONTAINER_PRICES = {
        "cone": 1.00,
        "cup": 1.50
    }
    
    def __init__(self, container):
        """Initialize an IceCreamBase object with a container."""
        if container not in IceCreamBase.CONTAINER_PRICES:
            raise ValueError(f"Invalid container type '{container}'. Choose 'cone' or 'cup'.")
        
        self.container = container
        self.description = f"Icecream {self.container.capitalize()}"

    def cost(self):
        """Calculate and return the total cost of the ice cream."""
        return IceCreamBase.CONTAINER_PRICES[self.container]

    def getDescription(self):
        """Return a simplified description."""
        return self.description


class IceCreamDecorator(IceCream):
    """Base class for IceCream decorators."""
    
    def __init__(self, ice_cream):
        """Initialize an IceCreamDecorator with an existing IceCream."""
        self.ice_cream = ice_cream

    def cost(self):
        """Forward cost calculation to the decorated IceCream."""
        return self.ice_cream.cost()

    def getDescription(self):
        """Forward description to the decorated IceCream."""
        return self.ice_cream.getDescription()


class Chocolate(IceCreamDecorator):
    """Decorator for adding chocolate flavor."""
    
    FLAVOR_PRICE = 0.50

    def cost(self):
        """Add chocolate flavor cost."""
        return self.ice_cream.cost() + Chocolate.FLAVOR_PRICE

    def getDescription(self):
        """Add chocolate flavor to the description."""
        return f"{self.ice_cream.getDescription()}, Chocolate"


class Strawberry(IceCreamDecorator):
    """Decorator for adding strawberry flavor."""
    
    FLAVOR_PRICE = 0.75

    def cost(self):
        """Add strawberry flavor cost."""
        return self.ice_cream.cost() + Strawberry.FLAVOR_PRICE

    def getDescription(self):
        """Add strawberry flavor to the description."""
        return f"{self.ice_cream.getDescription()}, Strawberry"


class Vanilla(IceCreamDecorator):
    """Decorator for adding vanilla flavor."""
    
    FLAVOR_PRICE = 0.60

    def cost(self):
        """Add vanilla flavor cost."""
        return self.ice_cream.cost() + Vanilla.FLAVOR_PRICE

    def getDescription(self):
        """Add vanilla flavor to the description."""
        return f"{self.ice_cream.getDescription()}, Vanilla"


class Cone(IceCreamBase):
    """Concrete class for Cone container."""
    def __init__(self):
        super().__init__("cone")


class Cup(IceCreamBase):
    """Concrete class for Cup container."""
    def __init__(self):
        super().__init__("cup")
