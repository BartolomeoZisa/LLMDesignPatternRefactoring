class BasicSword:
    def __init__(self):
        self.decorations = []

    def add_decoration(self, effect: str):
        self.decorations.append(effect)

    def description(self) -> str:
        desc = "Basic sword"
        effects = {
            "flame": "with flames",
            "poison": "coated in poison",
            "ice": "imbued with ice"
        }
        for effect in self.decorations:
            if effect in effects:
                desc += f", {effects[effect]}"
        return desc

    def damage(self) -> int:
        base = 10
        bonuses = {
            "flame": 5,
            "poison": 3,
            "ice": 4
        }
        return base + sum(bonuses.get(effect, 0) for effect in self.decorations)

