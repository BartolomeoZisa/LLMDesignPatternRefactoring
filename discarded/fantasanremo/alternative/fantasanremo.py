class Artist:
    def __init__(self, name, role_modifier):
        self.name = name
        self.role_modifier = role_modifier

    def get_name(self):
        return self.name

    def calculate_score_BM(self, base_points):
        role_score_map = {
            "starter": base_points,
            "reserve": 0,
            "captain": base_points,
        }
        return role_score_map.get(self.role_modifier, 0)

    def calculate_position_score(self, base_points):
        role_position_score_map = {
            "starter": base_points,
            "reserve": 0,
            "captain": base_points * 2,
        }
        return role_position_score_map.get(self.role_modifier, 0)
