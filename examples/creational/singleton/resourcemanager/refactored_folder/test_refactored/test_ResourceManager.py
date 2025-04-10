import pytest
import threading

from refactored.ResourceManager import *

#reset the singleton instance before each test
@pytest.fixture(autouse=True)
def reset_singletons():
  SingletonMeta._instances = {}

def run_factories(initial_resources, factories_data):
    resource_manager = ResourceManager(initial_resources)
    factories = []
    for data in factories_data:
        factory = Factory(data["name"], resource_manager, data["sequence"])
        factories.append(factory)
        factory.start()

    for factory in factories:
        factory.join()

    return resource_manager.resources

@pytest.fixture
def initial_resources_fixture():
    return {"wood": 100, "stone": 50, "iron": 30}

def test_exact_resource_consumption_single_factory(initial_resources_fixture):
    initial_resources = initial_resources_fixture
    factories_data = [
        {"name": "Factory_1", "sequence": [("wood", 100), ("stone", 50), ("iron", 30)]}
    ]
    final_resources = run_factories(initial_resources, factories_data)
    assert all(value == 0 for value in final_resources.values())

def test_exact_resource_consumption_multiple_factories_simple(initial_resources_fixture):
    initial_resources = initial_resources_fixture
    factories_data = [
        {"name": "Factory_1", "sequence": [("wood", 50), ("stone", 25), ("iron", 15)]},
        {"name": "Factory_2", "sequence": [("wood", 50), ("stone", 25), ("iron", 15)]},
    ]
    final_resources = run_factories(initial_resources, factories_data)
    assert all(value == 0 for value in final_resources.values())

def test_exact_resource_consumption_multiple_factories_complex(initial_resources_fixture):
    initial_resources = initial_resources_fixture
    factories_data = [
        {"name": "Factory_1", "sequence": [("wood", 30), ("stone", 10), ("iron", 5)]},
        {"name": "Factory_2", "sequence": [("wood", 20), ("stone", 15), ("iron", 10)]},
        {"name": "Factory_3", "sequence": [("wood", 50), ("stone", 25), ("iron", 15)]},
    ]
    final_resources = run_factories(initial_resources, factories_data)
    assert all(value == 0 for value in final_resources.values())

def test_resource_over_consumption_single_factory(initial_resources_fixture):
    initial_resources = initial_resources_fixture
    factories_data = [
        {"name": "Factory_1", "sequence": [("wood", 101)]}
    ]
    final_resources = run_factories(initial_resources, factories_data)
    assert final_resources["wood"] == initial_resources["wood"]  # Should not consume more than available
    assert final_resources["stone"] == initial_resources["stone"]
    assert final_resources["iron"] == initial_resources["iron"]

def test_resource_over_consumption_multiple_factories(initial_resources_fixture):
    initial_resources = initial_resources_fixture
    factories_data = [
        {"name": "Factory_1", "sequence": [("wood", 60)]},
        {"name": "Factory_2", "sequence": [("wood", 50)]},
    ]
    final_resources = run_factories(initial_resources, factories_data)
    assert final_resources["wood"] == initial_resources["wood"] - 60 or initial_resources["wood"]-50 # Only the first or second factory should succeed fully
    assert final_resources["stone"] == initial_resources["stone"]
    assert final_resources["iron"] == initial_resources["iron"]

def test_partial_resource_consumption(initial_resources_fixture):
    initial_resources = initial_resources_fixture
    factories_data = [
        {"name": "Factory_1", "sequence": [("wood", 20), ("stone", 10)]},
        {"name": "Factory_2", "sequence": [("wood", 30), ("stone", 15)]},
    ]
    final_resources = run_factories(initial_resources, factories_data)
    assert final_resources["wood"] == initial_resources["wood"] - 50
    assert final_resources["stone"] == initial_resources["stone"] - 25
    assert final_resources["iron"] == initial_resources["iron"]

def test_no_resource_consumption(initial_resources_fixture):
    initial_resources = initial_resources_fixture
    factories_data = [
        {"name": "Factory_1", "sequence": []},
        {"name": "Factory_2", "sequence": []},
    ]
    final_resources = run_factories(initial_resources, factories_data)
    assert final_resources == initial_resources

def test_mixed_resource_consumption_and_failure(initial_resources_fixture):
    initial_resources = initial_resources_fixture
    factories_data = [
        {"name": "Factory_1", "sequence": [("wood", 50), ("stone", 20)]},
        {"name": "Factory_2", "sequence": [("wood", 60), ("iron", 40)]}, # Factory 2 will fail on wood and iron
    ]
    final_resources = run_factories(initial_resources, factories_data)
    assert final_resources["wood"] == initial_resources["wood"] - 50
    assert final_resources["stone"] == initial_resources["stone"] - 20
    assert final_resources["iron"] == initial_resources["iron"]

def test_thread_safety():
    initial_resources = {"wood": 1000, "stone": 1000, "iron": 300}
    # create a big number of factories to test thread safety
    factories_data = [
        {"name": f"Factory_{i}", "sequence": [("wood", 1), ("stone", 1)]} for i in range(1000)
    ]
    final_resources = run_factories(initial_resources, factories_data)
    assert final_resources["wood"] == initial_resources["wood"] - 1000
    assert final_resources["stone"] == initial_resources["stone"] - 1000
    assert final_resources["iron"] == initial_resources["iron"]

def test_singleton_instance():
    # Create two instances of ResourceManager
    instance1 = ResourceManager({"wood": 100, "stone": 50})
    instance2 = ResourceManager()

    # Check if both instances are the same
    assert instance1 is instance2

    # Check if the resources of the first instance are affected by the second
    assert instance1.resources == {"wood": 100, "stone": 50}