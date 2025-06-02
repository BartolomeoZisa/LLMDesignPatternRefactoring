import pytest
from refactored.graphtraversal import DFSStrategy, BFSStrategy, GraphVisitor

@pytest.fixture
def graph():
    return {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }

def test_dfs_strategy(graph):
    visitor = GraphVisitor(DFSStrategy())
    result = visitor.visit(graph, 'A')
    assert result == ['A', 'B', 'D', 'E', 'F', 'C']

def test_bfs_strategy(graph):
    visitor = GraphVisitor(BFSStrategy())
    result = visitor.visit(graph, 'A')
    assert result == ['A', 'B', 'C', 'D', 'E', 'F']

def test_dfs_single_node():
    graph = {'X': []}
    visitor = GraphVisitor(DFSStrategy())
    result = visitor.visit(graph, 'X')
    assert result == ['X']

def test_bfs_single_node():
    graph = {'X': []}
    visitor = GraphVisitor(BFSStrategy())
    result = visitor.visit(graph, 'X')
    assert result == ['X']

def test_bfs_disconnected_graph():
    graph = {
        'A': ['B'],
        'B': [],
        'C': ['D'],
        'D': []
    }
    visitor = GraphVisitor(BFSStrategy())
    result = visitor.visit(graph, 'A')
    assert result == ['A', 'B']

def test_bfs_dfs_are_different():
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['E'],
        'D': [],
        'E': []
    }

    dfs_visitor = GraphVisitor(DFSStrategy())
    bfs_visitor = GraphVisitor(BFSStrategy())

    dfs_result = dfs_visitor.visit(graph, 'A')
    bfs_result = bfs_visitor.visit(graph, 'A')

    assert dfs_result == ['A', 'B', 'D', 'C', 'E']
    assert bfs_result == ['A', 'B', 'C', 'D', 'E']
    assert dfs_result != bfs_result  # Confirm they differ

def test_graph_visitor_strategy_switch():
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['E'],
        'D': [],
        'E': []
    }

    visitor = GraphVisitor(DFSStrategy())
    dfs_result = visitor.visit(graph, 'A')
    assert dfs_result == ['A', 'B', 'D', 'C', 'E']

    # Switch to BFS at runtime
    visitor.set_strategy(BFSStrategy())
    bfs_result = visitor.visit(graph, 'A')
    assert bfs_result == ['A', 'B', 'C', 'D', 'E']

    # Ensure that switching the strategy actually changes behavior
    assert dfs_result != bfs_result
