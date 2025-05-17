class IceCream:
    # Prices for containers and flavors
    CONTAINER_PRICES = {
        "cone": 1.00,
        "cup": 1.50
    }

    FLAVOR_PRICES = {
        "chocolate": 0.50,
        "strawberry": 0.75,
        "vanilla": 0.60
    }

    def __init__(self, container):
        """
        Initialize an IceCream object.

        Parameters:
        - container (str): either 'cone' or 'cup'
        """
        if container not in IceCream.CONTAINER_PRICES:
            raise ValueError(f"Invalid container type '{container}'. Choose 'cone' or 'cup'.")
        
        self.container = container
        self.description = f"Icecream {self.container.capitalize()}"
        self._cost = IceCream.CONTAINER_PRICES[self.container]

    def cost(self):
        """Calculate and return the total cost of the ice cream."""
        return self._cost

    def getDescription(self):
        """Return a simplified description in the format 'Icecream Container'."""
        return self.description


class Decorator(IceCream):
    def __init__(self, icecream):
        self.icecream = icecream

    def cost(self):
        return self.icecream.cost()

    def getDescription(self):
        return self.icecream.getDescription()


class Chocolate(Decorator):
    def __init__(self, icecream):
        super().__init__(icecream)
        self.icecream = icecream
        self._cost = IceCream.FLAVOR_PRICES['chocolate']
        self.description = f"{icecream.getDescription()}, Chocolate"

    def cost(self):
        return self._cost + self.icecream.cost()

    def getDescription(self):
        return self.description


class Strawberry(Decorator):
    def __init__(self, icecream):
        super().__init__(icecream)
        self.icecream = icecream
        self._cost = IceCream.FLAVOR_PRICES['strawberry']
        self.description = f"{icecream.getDescription()}, Strawberry"

    def cost(self):
        return self._cost + self.icecream.cost()

    def getDescription(self):
        return self.description


class Vanilla(Decorator):
    def __init__(self, icecream):
        super().__init__(icecream)
        self.icecream = icecream
        self._cost = IceCream.FLAVOR_PRICES['vanilla']
        self.description = f"{icecream.getDescription()}, Vanilla"

    def cost(self):
        return self._cost + self.icecream.cost()

    def getDescription(self):
        return self.description


class Cone(IceCream):
    def __init__(self):
        super().__init__("cone")


class Cup(IceCream):
    def __init__(self):
        super().__init__("cup")