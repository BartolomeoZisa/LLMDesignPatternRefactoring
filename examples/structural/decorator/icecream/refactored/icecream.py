from abc import ABC, abstractmethod


class Icecream:
    def __init__(self):
        self.description = "Icecream"

    def getDescription(self):
        return self.description
    
    @abstractmethod    
    def cost(self):
        pass

#concrete component
class Cone:
    def __init__(self):
        self.description = "Icecream Cone"

    def getDescription(self):
        return self.description
    
    def cost(self):
        return 1.00

class Cup:
    def __init__(self):
        self.description = "Icecream Cup"

    def getDescription(self):
        return self.description

    def cost(self):
        return 1.50

#Decorator
class IcecreamDecorator(Icecream):
    def __init__(self, icecream):
        self.icecream = icecream
    
    @abstractmethod 
    def getDescription(self):         
        pass

#Concrete Decorator
class Chocolate(IcecreamDecorator):
    def __init__(self, icecream):
        super().__init__(icecream)
        self.description = "Chocolate"
    
    def getDescription(self):
        return self.icecream.getDescription() + ", " + self.description
    
    def cost(self):
        return self.icecream.cost() + 0.50

class Strawberry(IcecreamDecorator):
    def __init__(self, icecream):
        super().__init__(icecream)
        self.description = "Strawberry"
    
    def getDescription(self):
        return self.icecream.getDescription() + ", " + self.description
    
    def cost(self):
        return self.icecream.cost() + 0.75
class Vanilla(IcecreamDecorator):
    def __init__(self, icecream):
        super().__init__(icecream)
        self.description = "Vanilla"
    
    def getDescription(self):
        return self.icecream.getDescription() + ", " + self.description
    
    def cost(self):
        return self.icecream.cost() + 0.60