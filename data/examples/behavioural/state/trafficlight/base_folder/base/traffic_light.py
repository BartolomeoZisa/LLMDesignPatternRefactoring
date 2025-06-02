from abc import ABC, abstractmethod


class TrafficLight:
    def __init__(self):
        self.state = "RED"

    def change(self) -> str:
        if self.state == "RED":
            self.state = "GREEN"
            return "Switching from RED to GREEN"
        elif self.state == "GREEN":
            self.state = "YELLOW"
            return "Switching from GREEN to YELLOW"
        elif self.state == "YELLOW":
            self.state = "RED"
            return "Switching from YELLOW to RED"
        else:
            raise ValueError(f"Invalid state: {self.state}")

    def show(self) -> str:
        if self.state == "RED":
            return "RED light - Stop!"
        elif self.state == "GREEN":
            return "GREEN light - Go!"
        elif self.state == "YELLOW":
            return "YELLOW light - Caution!"
        else:
            raise ValueError(f"Invalid state: {self.state}")

