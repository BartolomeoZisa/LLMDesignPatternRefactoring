from abc import ABC, abstractmethod
from collections import deque


class GraphTraversalStrategy(ABC):
    @abstractmethod
    def traverse(self, graph, start_node):
        pass

class DFSStrategy(GraphTraversalStrategy):
    def traverse(self, graph, start_node):
        visited = set()
        result = []

        def dfs(node):
            if node not in visited:
                visited.add(node)
                result.append(node)
                for neighbor in graph.get(node, []):
                    dfs(neighbor)

        dfs(start_node)
        return result

class BFSStrategy(GraphTraversalStrategy):
    def traverse(self, graph, start_node):
        visited = set()
        queue = deque([start_node])
        result = []

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                result.append(node)
                queue.extend(graph.get(node, []))

        return result
    
class GraphVisitor:
    def __init__(self, strategy: GraphTraversalStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: GraphTraversalStrategy):
        self.strategy = strategy

    def visit(self, graph, start_node):
        if not graph or start_node not in graph:
            return []
        return self.strategy.traverse(graph, start_node)

        