import pytest
from refactored.traffic_light import TrafficLight, RedState, GreenState, YellowState


def test_initial_state_is_red():
    light = TrafficLight()
    assert isinstance(light.state, RedState)


def test_red_to_green_transition():
    light = TrafficLight()
    message = light.change()
    assert isinstance(light.state, GreenState)
    assert message == "Switching from RED to GREEN"


def test_green_to_yellow_transition():
    light = TrafficLight()
    light.set_state(GreenState())
    message = light.change()
    assert isinstance(light.state, YellowState)
    assert message == "Switching from GREEN to YELLOW"


def test_yellow_to_red_transition():
    light = TrafficLight()
    light.set_state(YellowState())
    message = light.change()
    assert isinstance(light.state, RedState)
    assert message == "Switching from YELLOW to RED"


def test_display_red():
    light = TrafficLight()
    message = light.show()
    assert message == "RED light - Stop!"


def test_display_green():
    light = TrafficLight()
    light.set_state(GreenState())
    message = light.show()
    assert message == "GREEN light - Go!"


def test_display_yellow():
    light = TrafficLight()
    light.set_state(YellowState())
    message = light.show()
    assert message == "YELLOW light - Caution!"


def test_full_cycle_messages_and_states():
    light = TrafficLight()
    messages = []
    expected_states = [GreenState, YellowState, RedState]
    expected_messages = [
        "Switching from RED to GREEN",
        "Switching from GREEN to YELLOW",
        "Switching from YELLOW to RED"
    ]

    for expected_state, expected_msg in zip(expected_states, expected_messages):
        msg = light.change()
        messages.append(msg)
        assert isinstance(light.state, expected_state)

    assert messages == expected_messages


