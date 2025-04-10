class Artist:
    def __init__(self, name, role_modifier):
        self.name = name
        self.role_modifier = role_modifier

    def get_name(self):
        return self.name

    def calculate_score_BM(self, base_points):
        if self.role_modifier == "starter":
            return base_points
        elif self.role_modifier == "reserve":
            return 0
        elif self.role_modifier == "captain":
            return base_points
        else:
            return 0

    def calculate_position_score(self, base_points):
        if self.role_modifier == "starter":
            return base_points
        elif self.role_modifier == "reserve":
            return 0
        elif self.role_modifier == "captain":
            return base_points * 2
        else:   
            return 0
