import pytest
from refactored.Stall import *

# Test case for the initial FreeState
def test_initial_state():
    stall = Stall()
    assert isinstance(stall.state, FreeState)

# Test transition from FreeState -> OccupiedState on assign
def test_free_to_occupied_on_assign():
    stall = Stall()
    stall.assign()
    assert isinstance(stall.state, OccupiedState)

# Test transition from FreeState -> FreeMaintenanceState on report_issue
def test_free_to_free_maintenance_on_report_issue():
    stall = Stall()
    stall.report_issue()
    assert isinstance(stall.state, FreeMaintenanceState)

# Test transition from OccupiedState -> FreeState on end_market
def test_occupied_to_free_on_end_market():
    stall = Stall()
    stall.set_state(OccupiedState(stall))  # Moving to OccupiedState first
    stall.end_market()
    assert isinstance(stall.state, FreeState)

# Test transition from OccupiedState -> OccupiedMaintenanceState on report_issue
def test_occupied_to_occupied_maintenance_on_report_issue():
    stall = Stall()
    stall.set_state(OccupiedState(stall))  # Moving to OccupiedState first
    stall.report_issue()
    assert isinstance(stall.state, OccupiedMaintenanceState)

# Test transition from OccupiedMaintenanceState -> OccupiedState on finish_maintenance
def test_occupied_maintenance_to_occupied_on_finish_maintenance():
    stall = Stall()
    stall.set_state(OccupiedMaintenanceState(stall))  # Moving to OccupiedMaintenanceState first
    stall.finish_maintenance()
    assert isinstance(stall.state, OccupiedState)

# Test transition from OccupiedMaintenanceState -> FreeMaintenanceState on end_market
def test_occupied_maintenance_to_free_maintenance_on_end_market():
    stall = Stall()
    stall.set_state(OccupiedMaintenanceState(stall))  # Moving to OccupiedMaintenanceState first
    stall.end_market()
    assert isinstance(stall.state, FreeMaintenanceState)

# Test transition from FreeMaintenanceState -> FreeState on finish_maintenance
def test_free_maintenance_to_free_on_finish_maintenance():
    stall = Stall()
    stall.set_state(FreeMaintenanceState(stall))  # Moving to FreeMaintenanceState first
    stall.finish_maintenance()
    assert isinstance(stall.state, FreeState)

# Test invalid transition: FreeState -> end_market should raise Exception
def test_free_to_free_on_end_market():
    stall = Stall()
    with pytest.raises(Exception, match="Market is not running."):
        stall.end_market()
    assert isinstance(stall.state, FreeState)

# Test invalid transition: OccupiedState -> end_market should move to FreeState
def test_occupied_to_free_on_end_market():
    stall = Stall()
    stall.set_state(OccupiedState(stall))  # Moving to OccupiedState first
    stall.end_market()
    assert isinstance(stall.state, FreeState)

# Test invalid transition: OccupiedState -> finish_maintenance should raise Exception
def test_occupied_finish_maintenance_invalid():
    stall = Stall()
    stall.set_state(OccupiedState(stall))  # Moving to OccupiedState first
    with pytest.raises(Exception, match="Cannot finish maintenance in occupied state."):
        stall.finish_maintenance()
    assert isinstance(stall.state, OccupiedState)

# Test invalid transition: OccupiedMaintenanceState -> report_issue should raise Exception
def test_occupied_maintenance_report_issue_invalid():
    stall = Stall()
    stall.set_state(OccupiedMaintenanceState(stall))  # Moving to OccupiedMaintenanceState first
    with pytest.raises(Exception, match="Already under maintenance."):
        stall.report_issue()
    assert isinstance(stall.state, OccupiedMaintenanceState)

# Test invalid transition: FreeMaintenanceState -> report_issue should raise Exception
def test_free_maintenance_report_issue_invalid():
    stall = Stall()
    stall.set_state(FreeMaintenanceState(stall))  # Moving to FreeMaintenanceState first
    with pytest.raises(Exception, match="Already under maintenance."):
        stall.report_issue()
    assert isinstance(stall.state, FreeMaintenanceState)

# Test invalid transition: FreeState -> finish_maintenance should raise Exception
def test_free_finish_maintenance_invalid():
    stall = Stall()
    with pytest.raises(Exception, match="Already in a free state."):
        stall.finish_maintenance()
    assert isinstance(stall.state, FreeState)

# Test invalid transition: OccupiedState -> assign should raise Exception
def test_occupied_assign_invalid():
    stall = Stall()
    stall.set_state(OccupiedState(stall))
    with pytest.raises(Exception, match="Cannot assign while occupied."):
        stall.assign()
    assert isinstance(stall.state, OccupiedState)

# Test invalid transition: FreeMaintenanceState -> assign should raise Exception
def test_free_maintenance_assign_invalid():
    stall = Stall()
    stall.set_state(FreeMaintenanceState(stall))
    with pytest.raises(Exception, match="Cannot assign. Stall is under maintenance."):
        stall.assign()
    assert isinstance(stall.state, FreeMaintenanceState)


