from abc import ABC, abstractmethod

# --- State Interface ---
class TrafficLightState(ABC):
    @abstractmethod
    def next(self, context):
        """Transition to next state. Returns a string message."""
        pass

    @abstractmethod
    def display(self):
        """Returns a string message for current light state."""
        pass


# --- Concrete States ---
class RedState(TrafficLightState):
    def next(self, context):
        context.set_state(GreenState())
        return "Switching from RED to GREEN"

    def display(self):
        return "RED light - Stop!"


class GreenState(TrafficLightState):
    def next(self, context):
        context.set_state(YellowState())
        return "Switching from GREEN to YELLOW"

    def display(self):
        return "GREEN light - Go!"


class YellowState(TrafficLightState):
    def next(self, context):
        context.set_state(RedState())
        return "Switching from YELLOW to RED"

    def display(self):
        return "YELLOW light - Caution!"


# --- Context ---
class TrafficLight:
    def __init__(self):
        self.state: TrafficLightState = RedState()

    def set_state(self, state: TrafficLightState):
        self.state = state

    def change(self) -> str:
        return self.state.next(self)

    def show(self) -> str:
        return self.state.display()



