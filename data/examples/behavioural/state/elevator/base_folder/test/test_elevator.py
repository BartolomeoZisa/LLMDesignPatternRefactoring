import pytest
from base.elevator import *

def test_idle_to_moving_and_opening_doors():
    elevator = Elevator(floors=5)
    response = elevator.call(3)
    assert "Elevator called to floor 3" in response
    move_response = elevator.move(3)
    assert "Arrived at floor 3" in move_response
    door_response = elevator.open_doors()
    assert "Doors opening at floor 3" in door_response
    assert elevator.current_floor == 3

def test_opening_doors_to_open_state():
    elevator = Elevator(floors=5)
    elevator.call(2)
    elevator.move(2)
    response = elevator.open_doors()
    assert "Doors opening at floor 2" in response

def test_doors_open_to_closing():
    elevator = Elevator(floors=5)
    elevator.call(1)
    elevator.move(1)
    elevator.open_doors()
    response = elevator.close_doors()
    assert "Closing doors." in response

def test_doors_closing_to_opening():
    elevator = Elevator(floors=5)
    elevator.call(1)
    elevator.move(1)
    elevator.open_doors()
    elevator.close_doors()
    response = elevator.open_doors()
    assert "Re-opening doors." in response

def test_call_same_floor_opens_doors():
    elevator = Elevator(floors=5)
    elevator.current_floor = 2
    response = elevator.call(2)
    assert "Already on floor." in response

def test_invalid_floor_low():
    elevator = Elevator(floors=5)
    with pytest.raises(ElevatorError, match="Invalid floor."):
        elevator.call(-1)

def test_invalid_floor_high():
    elevator = Elevator(floors=5)
    with pytest.raises(ElevatorError, match="Invalid floor."):
        elevator.call(10)

def test_call_while_moving():
    elevator = Elevator(floors=5)
    elevator.call(4)
    elevator.move(4)
    elevator.open_doors()
    elevator.close_doors()
    elevator.close_doors()
    elevator.call(3)
    with pytest.raises(ElevatorError, match="Elevator is moving, please wait."):
        elevator.call(2)

def test_open_doors_while_moving():
    elevator = Elevator(floors=5)
    elevator.call(4)
    with pytest.raises(ElevatorError, match="Cannot open doors while moving."):
        elevator.open_doors()

def test_move_while_doors_open():
    elevator = Elevator(floors=5)
    elevator.call(3)
    elevator.move(3)
    elevator.open_doors()
    with pytest.raises(ElevatorError, match="Cannot move, doors are open."):
        elevator.move(3)

def test_call_while_doors_open():
    elevator = Elevator(floors=5)
    elevator.call(2)
    elevator.move(2)
    elevator.open_doors()
    with pytest.raises(ElevatorError, match="Doors are open, please wait."):
        elevator.call(1)

def test_move_while_idle_error():
    elevator = Elevator(floors=5)
    with pytest.raises(ElevatorError, match="Elevator is idle, not moving."):
        elevator.move(5)

def test_doors_already_open():
    elevator = Elevator(floors=5)
    elevator.call(2)
    elevator.move(2)
    elevator.open_doors()
    with pytest.raises(ElevatorError, match="Doors are already open."):
        elevator.open_doors()

def test_close_while_opening():
    elevator = Elevator(floors=5)
    elevator.call(3)
    elevator.move(3)
    with pytest.raises(ElevatorError, match="Doors are opening, cannot close now."):
        elevator.close_doors()

def test_open_while_opening():
    elevator = Elevator(floors=5)
    elevator.call(3)
    elevator.move(3)
    response = elevator.open_doors()
    assert "Doors opening at floor" in response

def test_move_while_closing():
    elevator = Elevator(floors=5)
    elevator.call(2)
    elevator.move(2)
    elevator.open_doors()
    elevator.close_doors()
    with pytest.raises(ElevatorError, match="Cannot move, doors are closing."):
        elevator.move(2)

def test_idle_door_operations():
    elevator = Elevator(floors=5)
    with pytest.raises(ElevatorError, match="Elevator is idle, doors are closed."):
        elevator.open_doors()
    with pytest.raises(ElevatorError, match="Elevator is idle, doors are closed."):
        elevator.close_doors()

