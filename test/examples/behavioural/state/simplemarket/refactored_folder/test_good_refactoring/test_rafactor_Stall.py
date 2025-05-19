import pytest
from refactored.Stall import *

class BrokenState(StallState):
    def assign(self):
        raise Exception("Cannot assign. Stall is broken.")
    
    def end_market(self):
        raise Exception("Cannot end market. Stall is broken.")
    
    def report_issue(self):
        print("Broken stall reported. Moving to free maintenance.")
        self.stall.set_state(FreeMaintenanceState(self.stall))
    
    def finish_maintenance(self):
        raise Exception("Cannot finish maintenance directly from broken state.")

@pytest.fixture
def stall_in_broken_state():
    stall = Stall()
    stall.set_state(BrokenState(stall))  # Directly inject BrokenState
    return stall

def test_broken_state_report_issue_moves_to_free_maintenance(stall_in_broken_state):
    stall_in_broken_state.report_issue()
    assert isinstance(stall_in_broken_state.state, FreeMaintenanceState)

def test_broken_state_assign_raises_exception(stall_in_broken_state):
    with pytest.raises(Exception, match="Cannot assign. Stall is broken."):
        stall_in_broken_state.assign()

def test_broken_state_end_market_raises_exception(stall_in_broken_state):
    with pytest.raises(Exception, match="Cannot end market. Stall is broken."):
        stall_in_broken_state.end_market()

def test_broken_state_finish_maintenance_raises_exception(stall_in_broken_state):
    with pytest.raises(Exception, match="Cannot finish maintenance directly from broken state."):
        stall_in_broken_state.finish_maintenance()

