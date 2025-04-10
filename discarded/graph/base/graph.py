from queue import Queue, PriorityQueue

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_edge(self, u, v, weight=1):
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        self.adj_list[u].append((v, weight))
        self.adj_list[v].append((u, weight))  # For an undirected graph

    # --- BFS Traversal ---
    def bfs(self, start):
        visited = set()
        result = []
        queue = Queue()
        queue.put(start)
        while not queue.empty():
            node = queue.get()
            if node not in visited:
                visited.add(node)
                result.append(node)
                for neighbor, _ in self.adj_list.get(node, []):
                    if neighbor not in visited:
                        queue.put(neighbor)
        return result

    # --- DFS Traversal ---
    def dfs(self, start):
        visited = set()
        result = []
        stack = [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                result.append(node)
                for neighbor, _ in self.adj_list.get(node, []):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return result

    # --- Dijkstra's Algorithm ---
    def dijkstra(self, start):
        distances = {node: float('inf') for node in self.adj_list}
        distances[start] = 0
        pq = PriorityQueue()
        pq.put((0, start))

        while not pq.empty():
            current_dist, node = pq.get()
            if current_dist > distances[node]:
                continue
            for neighbor, weight in self.adj_list.get(node, []):
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    pq.put((new_dist, neighbor))
        
        return distances

    # --- General Traversal Method ---
    def traverse(self, start, traversal_type):
        if traversal_type == "BFS":
            return self.bfs(start)
        elif traversal_type == "DFS":
            return self.dfs(start)
        elif traversal_type == "Dijkstra":
            return self.dijkstra(start)
        else:
            raise ValueError("Unknown traversal type")