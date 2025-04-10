from abc import ABC, abstractmethod

# Strategy Interface for Role
class Role(ABC):
    @abstractmethod
    def calculate_score_BM(self, base_points: int) -> int:
        pass
    
    @abstractmethod
    def calculate_position_score(self, base_points: int) -> int:
        pass

# Concrete strategy for "Starter"
class Starter(Role):
    def calculate_score_BM(self, base_points: int) -> int:
        return base_points
    
    def calculate_position_score(self, base_points: int) -> int:
        return base_points

# Concrete strategy for "Captain"
class Captain(Role):
    def calculate_score_BM(self, base_points: int) -> int:
        return base_points
    
    def calculate_position_score(self, base_points: int) -> int:
        return base_points * 2

# Concrete strategy for "Reserve"
class Reserve(Role):
    def calculate_score_BM(self, base_points: int) -> int:
        return 0
    
    def calculate_position_score(self, base_points: int) -> int:
        return 0

# Concrete strategy for "Unknown" role
class Unknown(Role):
    def calculate_score_BM(self, base_points: int) -> int:
        return 0
    
    def calculate_position_score(self, base_points: int) -> int:
        return 0

# Factory class to choose corresponding role
class RoleFactory:
    @staticmethod
    def create_role(role_modifier: str) -> Role:
        if role_modifier == "starter":
            return Starter()
        elif role_modifier == "captain":
            return Captain()
        elif role_modifier == "reserve":
            return Reserve()
        else:
            return Unknown()  # Default to Unknown role

# Artist class using the Strategy pattern
class Artist:
    def __init__(self, name, role_modifier: str):
        self.name = name
        self.role = RoleFactory.create_role(role_modifier)

    def get_name(self):
        return self.name

    def set_role(self, role_modifier: str):
        self.role = RoleFactory.create_role(role_modifier)

    def calculate_score_BM(self, base_points: int) -> int:
        return self.role.calculate_score_BM(base_points)

    def calculate_position_score(self, base_points: int) -> int:
        return self.role.calculate_position_score(base_points)

