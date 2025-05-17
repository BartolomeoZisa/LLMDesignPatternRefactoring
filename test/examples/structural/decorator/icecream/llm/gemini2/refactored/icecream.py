class IceCreamComponent:
    def cost(self):
        raise NotImplementedError

    def getDescription(self):
        raise NotImplementedError

class Cone(IceCreamComponent):
    PRICE = 1.00
    DESCRIPTION = "Icecream Cone"

    def cost(self):
        return Cone.PRICE

    def getDescription(self):
        return Cone.DESCRIPTION

class Cup(IceCreamComponent):
    PRICE = 1.50
    DESCRIPTION = "Icecream Cup"

    def cost(self):
        return Cup.PRICE

    def getDescription(self):
        return Cup.DESCRIPTION

class IceCreamDecorator(IceCreamComponent):
    def __init__(self, component):
        self.component = component

    def cost(self):
        return self.component.cost()

    def getDescription(self):
        return self.component.getDescription()

class Chocolate(IceCreamDecorator):
    PRICE = 0.50
    DESCRIPTION = "Chocolate"

    def cost(self):
        return super().cost() + Chocolate.PRICE

    def getDescription(self):
        return f"{super().getDescription()}, {Chocolate.DESCRIPTION}"

class Strawberry(IceCreamDecorator):
    PRICE = 0.75
    DESCRIPTION = "Strawberry"

    def cost(self):
        return super().cost() + Strawberry.PRICE

    def getDescription(self):
        return f"{super().getDescription()}, {Strawberry.DESCRIPTION}"

class Vanilla(IceCreamDecorator):
    PRICE = 0.60
    DESCRIPTION = "Vanilla"

    def cost(self):
        return super().cost() + Vanilla.PRICE

    def getDescription(self):
        return f"{super().getDescription()}, {Vanilla.DESCRIPTION}"
