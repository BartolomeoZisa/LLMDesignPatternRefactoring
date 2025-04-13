class IceCreamComponent:
    def cost(self):
        raise NotImplementedError

    def getDescription(self):
        raise NotImplementedError

class Container(IceCreamComponent):
    def __init__(self, container_type, price):
        self.container_type = container_type
        self.price = price

    def cost(self):
        return self.price

    def getDescription(self):
        return f"Icecream {self.container_type.capitalize()}"

class Cone(Container):
    def __init__(self):
        super().__init__("cone", 1.00)

class Cup(Container):
    def __init__(self):
        super().__init__("cup", 1.50)

class FlavorDecorator(IceCreamComponent):
    def __init__(self, component, flavor_name, flavor_price):
        self.component = component
        self.flavor_name = flavor_name
        self.flavor_price = flavor_price

    def cost(self):
        return self.component.cost() + self.flavor_price

    def getDescription(self):
        return f"{self.component.getDescription()}, {self.flavor_name.capitalize()}"

class Chocolate(FlavorDecorator):
    def __init__(self, component):
        super().__init__(component, "chocolate", 0.50)

class Strawberry(FlavorDecorator):
    def __init__(self, component):
        super().__init__(component, "strawberry", 0.75)

class Vanilla(FlavorDecorator):
    def __init__(self, component):
        super().__init__(component, "vanilla", 0.60)
