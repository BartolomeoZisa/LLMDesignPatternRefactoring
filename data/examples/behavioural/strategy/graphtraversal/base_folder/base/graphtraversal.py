from collections import deque

class GraphVisitor:
    def __init__(self, strategy="dfs"):
        self.set_strategy(strategy)

    def set_strategy(self, strategy_name):
        if strategy_name not in ("dfs", "bfs"):
            raise ValueError(f"Unknown strategy '{strategy_name}'. Use 'dfs' or 'bfs'.")
        self.strategy = strategy_name

    def visit(self, graph, start_node):
        if start_node not in graph or not graph:
            # If the start node is not in the graph or the graph is empty, return an empty list
            return []

        if self.strategy == "dfs":
            return self._dfs(graph, start_node)
        elif self.strategy == "bfs":
            return self._bfs(graph, start_node)

    def _dfs(self, graph, start_node):
        visited = []
        stack = [start_node]

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.append(node)
                stack.extend(reversed(graph.get(node, [])))
        return visited

    def _bfs(self, graph, start_node):
        visited = []
        queue = deque([start_node])

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.append(node)
                queue.extend(graph.get(node, []))
        return visited


