from abc import ABC, abstractmethod


class Stall:
    def __init__(self):
        self.state = FreeState(self)

    def set_state(self, state):
        self.state = state

    def assign(self):
        state_actions = {
            FreeState: self._assign_free,
            AssignedState: self._assign_assigned,
            OccupiedState: self._assign_occupied,
            MaintenanceState: self._assign_maintenance,
        }
        state_actions[type(self.state)]()

    def _assign_free(self):
        print("Stall assigned.")
        self.set_state(AssignedState(self))

    def _assign_assigned(self):
        print("Already assigned.")

    def _assign_occupied(self):
        print("Cannot assign while occupied.")

    def _assign_maintenance(self):
        print("Cannot assign. Stall is under maintenance.")

    def start_market(self):
        state_actions = {
            FreeState: self._start_market_free,
            AssignedState: self._start_market_assigned,
            OccupiedState: self._start_market_occupied,
            MaintenanceState: self._start_market_maintenance,
        }
        state_actions[type(self.state)]()

    def _start_market_free(self):
        print("Cannot start market without assignment.")

    def _start_market_assigned(self):
        print("Market started.")
        self.set_state(OccupiedState(self))

    def _start_market_occupied(self):
        print("Already in market.")

    def _start_market_maintenance(self):
        print("Cannot start market. Stall is under maintenance.")

    def end_market(self):
        state_actions = {
            FreeState: self._end_market_free,
            AssignedState: self._end_market_assigned,
            OccupiedState: self._end_market_occupied,
            MaintenanceState: self._end_market_maintenance,
        }
        state_actions[type(self.state)]()

    def _end_market_free(self):
        print("Market is not running.")

    def _end_market_assigned(self):
        print("Market not started yet.")

    def _end_market_occupied(self):
        print("Market ended. Moving to free state.")
        self.set_state(FreeState(self))

    def _end_market_maintenance(self):
        print("Market is not running.")

    def report_issue(self):
        state_actions = {
            FreeState: self._report_issue_free,
            AssignedState: self._report_issue_assigned,
            OccupiedState: self._report_issue_occupied,
            MaintenanceState: self._report_issue_maintenance,
        }
        state_actions[type(self.state)]()

    def _report_issue_free(self):
        print("Issue reported. Moving to maintenance.")
        self.set_state(MaintenanceState(self))

    def _report_issue_assigned(self):
        print("Issue reported. Moving to maintenance.")
        self.set_state(MaintenanceState(self))

    def _report_issue_occupied(self):
        print("Issue reported. Moving to maintenance.")
        self.set_state(MaintenanceState(self))

    def _report_issue_maintenance(self):
        print("Already under maintenance.")

    def finish_maintenance(self):
        state_actions = {
            FreeState: self._finish_maintenance_free,
            AssignedState: self._finish_maintenance_assigned,
            OccupiedState: self._finish_maintenance_occupied,
            MaintenanceState: self._finish_maintenance_maintenance,
        }
        state_actions[type(self.state)]()

    def _finish_maintenance_free(self):
        print("Already in a free state.")

    def _finish_maintenance_assigned(self):
        print("Cannot finish maintenance in assigned state.")

    def _finish_maintenance_occupied(self):
        print("Cannot finish maintenance in occupied state.")

    def _finish_maintenance_maintenance(self):
        print("Maintenance finished. Moving to free state.")
        self.set_state(FreeState(self))


# State Classes
class StallState(ABC):
    def __init__(self, stall):
        self.stall = stall


class FreeState(StallState):
    def __init__(self, stall):
        super().__init__(stall)


class AssignedState(StallState):
    def __init__(self, stall):
        super().__init__(stall)


class OccupiedState(StallState):
    def __init__(self, stall):
        super().__init__(stall)


class MaintenanceState(StallState):
    def __init__(self, stall):
        super().__init__(stall)


