import pytest
from alternative.Stall import *

# Fixture to set up a new Stall object for each test
@pytest.fixture
def stall():
    return Stall()

def test_free_to_assigned(stall):
    # Initially in FreeState
    stall.assign()
    assert isinstance(stall.state, AssignedState)

def test_free_to_maintenance(stall):
    # Initially in FreeState
    stall.report_issue()
    assert isinstance(stall.state, MaintenanceState)

def test_assigned_to_occupied(stall):
    # Transition from FreeState to AssignedState
    stall.assign()
    stall.start_market()
    assert isinstance(stall.state, OccupiedState)

def test_assigned_to_maintenance(stall):
    # Transition from FreeState to AssignedState
    stall.assign()
    stall.report_issue()
    assert isinstance(stall.state, MaintenanceState)

def test_occupied_to_free(stall):
    # Transition from FreeState to AssignedState to OccupiedState
    stall.assign()
    stall.start_market()
    stall.end_market()
    assert isinstance(stall.state, FreeState)

def test_occupied_to_maintenance(stall):
    # Transition from FreeState to AssignedState to OccupiedState
    stall.assign()
    stall.start_market()
    stall.report_issue()
    assert isinstance(stall.state, MaintenanceState)

def test_maintenance_to_free(stall):
    # Transition from FreeState to MaintenanceState
    stall.report_issue()
    stall.finish_maintenance()
    assert isinstance(stall.state, FreeState)

def test_assign_when_assigned(stall):
    # Initially in FreeState
    stall.assign()
    # Now in AssignedState, try assigning again
    stall.assign()
    assert isinstance(stall.state, AssignedState)  # Should remain in AssignedState

def test_assign_when_occupied(stall):
    # Transition from FreeState to AssignedState to OccupiedState
    stall.assign()
    stall.start_market()
    stall.assign()  # Try to assign while occupied
    assert isinstance(stall.state, OccupiedState)  # Should remain in OccupiedState

def test_start_market_when_free(stall):
    # Initially in FreeState
    stall.start_market()
    assert isinstance(stall.state, FreeState)  # Should remain in FreeState, cannot start market


def test_end_market_when_free(stall):
    # Initially in FreeState
    stall.end_market()
    assert isinstance(stall.state, FreeState)  # Should remain in FreeState, market isn't running

def test_end_market_when_maintenance(stall):
    # Transition from FreeState to MaintenanceState
    stall.report_issue()
    stall.end_market()
    assert isinstance(stall.state, MaintenanceState)  # Should remain in MaintenanceState, market isn't running

def test_report_issue_when_free(stall):
    # Initially in FreeState
    stall.report_issue()
    assert isinstance(stall.state, MaintenanceState)  # Should transition to MaintenanceState

def test_report_issue_when_assigned(stall):
    # Transition from FreeState to AssignedState
    stall.assign()
    stall.report_issue()
    assert isinstance(stall.state, MaintenanceState)  # Should transition to MaintenanceState

def test_finish_maintenance_when_free(stall):
    # Initially in FreeState
    stall.finish_maintenance()
    assert isinstance(stall.state, FreeState)  # Should remain in FreeState, no maintenance to finish

def test_finish_maintenance_when_assigned(stall):
    # Transition from FreeState to AssignedState
    stall.assign()
    stall.finish_maintenance()
    assert isinstance(stall.state, AssignedState)  # Should remain in AssignedState, no maintenance to finish

def test_finish_maintenance_when_occupied(stall):
    # Transition from FreeState to AssignedState to OccupiedState
    stall.assign()
    stall.start_market()
    stall.finish_maintenance()
    assert isinstance(stall.state, OccupiedState)  # Should remain in OccupiedState, no maintenance to finish

def test_finish_maintenance_when_maintenance(stall):
    # Transition from FreeState to MaintenanceState
    stall.report_issue()
    stall.finish_maintenance()
    assert isinstance(stall.state, FreeState)  # Should transition back to FreeState after finishing maintenance
