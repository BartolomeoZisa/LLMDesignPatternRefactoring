from abc import ABC, abstractmethod

# Context Class
class Stall:
    def __init__(self):
        self.state = FreeState(self)
    
    def set_state(self, state):
        self.state = state
    
    def assign(self):
        self.state.assign()
    
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
        self.stall.set_state(OccupiedState(self.stall))
    
    def end_market(self):
        raise Exception("Market is not running.")
    
    def report_issue(self):
        print("Issue reported. Moving to maintenance.")
        self.stall.set_state(FreeMaintenanceState(self.stall))
    
    def finish_maintenance(self):
        raise Exception("Already in a free state.")

class OccupiedState(StallState):
    def assign(self):
        raise Exception("Cannot assign while occupied.")
    
    def end_market(self):
        print("Market ended. Moving to free state.")
        self.stall.set_state(FreeState(self.stall))
    
    def report_issue(self):
        print("Issue reported. Moving to maintenance.")
        self.stall.set_state(OccupiedMaintenanceState(self.stall))
    
    def finish_maintenance(self):
        raise Exception("Cannot finish maintenance in occupied state.")

class OccupiedMaintenanceState(StallState):
    def assign(self):
        raise Exception("Cannot assign. Stall is under maintenance.")
    
    def end_market(self):
        print("Market ended, changing maintenance.")
        self.stall.set_state(FreeMaintenanceState(self.stall))
    
    def report_issue(self):
        raise Exception("Already under maintenance.")
    
    def finish_maintenance(self):
        print("Maintenance finished. Moving to free state.")
        self.stall.set_state(OccupiedState(self.stall))

class FreeMaintenanceState(StallState):
    def assign(self):
        raise Exception("Cannot assign. Stall is under maintenance.")
    
    def end_market(self):
        raise Exception("Market is not running.")
    
    def report_issue(self):
        raise Exception("Already under maintenance.")
    
    def finish_maintenance(self):
        print("Maintenance finished. Moving to free state.")
        self.stall.set_state(FreeState(self.stall))