from abc import ABC, abstractmethod

# Context Class
class Stall:
    def __init__(self):
        self.state = FreeState(self)
    
    def set_state(self, state):
        self.state = state
    
    def assign(self):
        self.state.assign()
    
    def start_market(self):
        self.state.start_market()
    
    def end_market(self):
        self.state.end_market()
    
    def report_issue(self):
        self.state.report_issue()
    
    def finish_maintenance(self):
        self.state.finish_maintenance()

# State Interface
class StallState(ABC):
    def __init__(self, stall):
        self.stall = stall
    
    @abstractmethod
    def assign(self):
        pass
    
    @abstractmethod
    def start_market(self):
        pass
    
    @abstractmethod
    def end_market(self):
        pass
    
    @abstractmethod
    def report_issue(self):
        pass
    
    @abstractmethod
    def finish_maintenance(self):
        pass

# Concrete States
class FreeState(StallState):
    def assign(self):
        print("Stall assigned.")
        self.stall.set_state(AssignedState(self.stall))
    
    def start_market(self):
        print("Cannot start market without assignment.")
    
    def end_market(self):
        print("Market is not running.")
    
    def report_issue(self):
        print("Issue reported. Moving to maintenance.")
        self.stall.set_state(MaintenanceState(self.stall))
    
    def finish_maintenance(self):
        print("Already in a free state.")

class AssignedState(StallState):
    def assign(self):
        print("Already assigned.")
    
    def start_market(self):
        print("Market started.")
        self.stall.set_state(OccupiedState(self.stall))
    
    def end_market(self):
        print("Market not started yet.")
    
    def report_issue(self):
        print("Issue reported. Moving to maintenance.")
        self.stall.set_state(MaintenanceState(self.stall))
    
    def finish_maintenance(self):
        print("Cannot finish maintenance in assigned state.")

class OccupiedState(StallState):
    def assign(self):
        print("Cannot assign while occupied.")
    
    def start_market(self):
        print("Already in market.")
    
    def end_market(self):
        print("Market ended. Moving to free state.")
        self.stall.set_state(FreeState(self.stall))
    
    def report_issue(self):
        print("Issue reported. Moving to maintenance.")
        self.stall.set_state(MaintenanceState(self.stall))
    
    def finish_maintenance(self):
        print("Cannot finish maintenance in occupied state.")

class MaintenanceState(StallState):
    def assign(self):
        print("Cannot assign. Stall is under maintenance.")
    
    def start_market(self):
        print("Cannot start market. Stall is under maintenance.")
    
    def end_market(self):
        print("Market is not running.")
    
    def report_issue(self):
        print("Already under maintenance.")
    
    def finish_maintenance(self):
        print("Maintenance finished. Moving to free state.")
        self.stall.set_state(FreeState(self.stall))