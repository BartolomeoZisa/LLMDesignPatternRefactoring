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
    
    def __init__(self, container, scoops):
        """
        Initialize an IceCream object.
        
        Parameters:
        - container (str): either 'cone' or 'cup'
        - scoops (list of str): list of flavors (e.g., ['chocolate', 'vanilla'])
        """
        # Validate container choice
        if container not in IceCream.CONTAINER_PRICES:
            raise ValueError(f"Invalid container type '{container}'. Choose 'cone' or 'cup'.")
        
        # Validate scoop flavors
        for flavor in scoops:
            if flavor not in IceCream.FLAVOR_PRICES:
                raise ValueError(f"Invalid flavor '{flavor}'. Choose from {list(IceCream.FLAVOR_PRICES.keys())}.")
        
        self.container = container
        self.scoops = scoops
        self.description = f"Icecream {self.container.capitalize()}, {', '.join(flavor.capitalize() for flavor in self.scoops)}"


    def cost(self):
        """Calculate and return the total cost of the ice cream."""
        total_cost = IceCream.CONTAINER_PRICES[self.container]
        for flavor in self.scoops:
            total_cost += IceCream.FLAVOR_PRICES[flavor]
        return total_cost
    
    def getDescription(self):
        """Return a simplified description in the format 'Icecream Container, Flavor1, Flavor2'."""
        return self.description