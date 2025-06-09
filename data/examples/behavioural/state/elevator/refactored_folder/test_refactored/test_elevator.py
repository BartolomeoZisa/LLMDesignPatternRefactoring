import pytest
from refactored.elevator import (
    Elevator,
    IdleDownState,
    IdleUpState,
    MovingUpwardsState,
    MovingDownwardsState,
    DoorsOpeningUpState,
    DoorsOpeningDownState,
    DoorsClosingUpState,
    DoorsClosingDownState,
    InvalidStateTransitionError,
)

# ---------- Valid Transitions ----------

def test_idle_down_to_moving_upwards():
    elevator = Elevator()
    elevator.call("up")
    assert isinstance(elevator.state, MovingUpwardsState)

def test_idle_down_to_doors_opening_down():
    elevator = Elevator()
    elevator.call("down")
    assert isinstance(elevator.state, DoorsOpeningDownState)

def test_moving_upwards_to_doors_opening_up():
    elevator = Elevator()
    elevator.call("up")  # Moves to MovingUpwards
    elevator.sensor_arrival_triggered()
    assert isinstance(elevator.state, DoorsOpeningUpState)

def test_moving_downwards_to_doors_opening_down():
    elevator = Elevator()
    elevator.set_state(IdleUpState(elevator))
    elevator.call("down")
    elevator.sensor_arrival_triggered()
    assert isinstance(elevator.state, DoorsOpeningDownState)

def test_doors_opening_up_to_closing_up():
    elevator = Elevator()
    elevator.set_state(DoorsOpeningUpState(elevator))
    elevator.sensor_doors_opened()
    assert isinstance(elevator.state, DoorsClosingUpState)

def test_doors_opening_down_to_closing_down():
    elevator = Elevator()
    elevator.set_state(DoorsOpeningDownState(elevator))
    elevator.sensor_doors_opened()
    assert isinstance(elevator.state, DoorsClosingDownState)

def test_doors_closing_up_to_idle_up():
    elevator = Elevator()
    elevator.set_state(DoorsClosingUpState(elevator))
    elevator.sensor_door_closed()
    assert isinstance(elevator.state, IdleUpState)

def test_doors_closing_down_to_idle_down():
    elevator = Elevator()
    elevator.set_state(DoorsClosingDownState(elevator))
    elevator.sensor_door_closed()
    assert isinstance(elevator.state, IdleDownState)

# ---------- Invalid Transitions ----------

def test_invalid_call_from_moving_upwards():
    elevator = Elevator()
    elevator.call("up")  # MovingUpwards
    with pytest.raises(InvalidStateTransitionError):
        elevator.call("down")

def test_invalid_notify_arrived_from_idle_down():
    elevator = Elevator()
    with pytest.raises(InvalidStateTransitionError):
        elevator.sensor_arrival_triggered()

def test_invalid_notify_doors_opened_from_idle_up():
    elevator = Elevator()
    elevator.set_state(IdleUpState(elevator))
    with pytest.raises(InvalidStateTransitionError):
        elevator.sensor_doors_opened()

def test_invalid_notify_door_closed_from_moving_down():
    elevator = Elevator()
    elevator.set_state(MovingDownwardsState(elevator))
    with pytest.raises(InvalidStateTransitionError):
        elevator.sensor_door_closed()


