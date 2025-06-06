import pytest

# Assume elevator code is imported or present here:
from base.elevator import Elevator, InvalidStateTransitionError

@pytest.fixture
def elevator():
    return Elevator()

def test_idle_down_to_moving_up(elevator):
    elevator.call_to_up()
    assert elevator.state.__class__.__name__ == "MovingUpwardsState"

def test_moving_up_to_doors_opening(elevator):
    elevator.call_to_up()
    elevator.sensor_arrival_triggered()
    assert elevator.state.__class__.__name__ == "DoorsOpeningState"

def test_doors_opening_to_doors_closing(elevator):
    elevator.call_to_up()
    elevator.sensor_arrival_triggered()
    elevator.sensor_doors_opened()
    assert elevator.state.__class__.__name__ == "DoorsClosingState"

def test_doors_closing_to_idle_up(elevator):
    elevator.call_to_up()
    elevator.sensor_arrival_triggered()
    elevator.sensor_doors_opened()
    elevator.sensor_door_closed_up()
    assert elevator.state.__class__.__name__ == "IdleUpState"

def test_idle_up_to_moving_down(elevator):
    elevator.call_to_up()
    elevator.sensor_arrival_triggered()
    elevator.sensor_doors_opened()
    elevator.sensor_door_closed_up()

    elevator.call_to_down()
    assert elevator.state.__class__.__name__ == "MovingDownwardsState"

def test_moving_down_to_doors_opening(elevator):
    elevator.call_to_up()
    elevator.sensor_arrival_triggered()
    elevator.sensor_doors_opened()
    elevator.sensor_door_closed_up()

    elevator.call_to_down()
    elevator.sensor_arrival_triggered()
    assert elevator.state.__class__.__name__ == "DoorsOpeningState"

def test_doors_closing_to_idle_down(elevator):
    elevator.call_to_up()
    elevator.sensor_arrival_triggered()
    elevator.sensor_doors_opened()
    elevator.sensor_door_closed_up()

    elevator.call_to_down()
    elevator.sensor_arrival_triggered()
    elevator.sensor_doors_opened()
    elevator.sensor_door_closed_down()
    assert elevator.state.__class__.__name__ == "IdleDownState"

def test_invalid_call_to_down_in_idle_down(elevator):
    with pytest.raises(InvalidStateTransitionError):
        elevator.call_to_down()

def test_invalid_call_to_up_in_moving_upwards(elevator):
    elevator.call_to_up()
    with pytest.raises(InvalidStateTransitionError):
        elevator.call_to_up()

def test_invalid_notify_doors_opened_in_idle_down(elevator):
    with pytest.raises(InvalidStateTransitionError):
        elevator.sensor_doors_opened()

def test_invalid_notify_door_closed_down_in_idle_up(elevator):
    elevator.call_to_up()
    elevator.sensor_arrival_triggered()
    elevator.sensor_doors_opened()
    elevator.sensor_door_closed_up()
    with pytest.raises(InvalidStateTransitionError):
        elevator.sensor_door_closed_down()

