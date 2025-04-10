from queue import Queue, PriorityQueue
from abc import ABC, abstractmethod

# --- Unified Data Structure Interface and Wrappers ---

class DSWrapper(ABC):
    def __init__(self):
        self.visited = set()
        self.result = []
    
    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def empty(self):
        pass
    
    @abstractmethod
    def process_node(self, node, adj_list):
        pass

    def get_result(self):
        return self.result

class BFSWrapper(DSWrapper):
    def __init__(self, start):
        super().__init__()
        self.ds = Queue()
        self.ds.put(start)
    
    def add(self, item):
        self.ds.put(item)
    
    def remove(self):
        return self.ds.get()
    
    def empty(self):
        return self.ds.empty()
    
    def process_node(self, node, adj_list):
        if node in self.visited:
            return
        self.visited.add(node)
        self.result.append(node)
        for neighbor, _ in adj_list.get(node, []):
            if neighbor not in self.visited:
                self.add(neighbor)

class DFSWrapper(DSWrapper):
    def __init__(self, start):
        super().__init__()
        self.ds = [start]
    
    def add(self, item):
        self.ds.append(item)
    
    def remove(self):
        return self.ds.pop()
    
    def empty(self):
        return len(self.ds) == 0
    
    def process_node(self, node, adj_list):
        if node in self.visited:
            return
        self.visited.add(node)
        self.result.append(node)
        for neighbor, _ in adj_list.get(node, []):
            if neighbor not in self.visited:
                self.add(neighbor)

class DijkstraWrapper(DSWrapper):
    def __init__(self, adj_list, start):
        super().__init__()
        self.ds = PriorityQueue()
        self.distances = {node: float('inf') for node in adj_list}
        self.distances[start] = 0
        self.ds.put((0, start))
    
    def add(self, item):
        self.ds.put(item)
    
    def remove(self):
        return self.ds.get()
    
    def empty(self):
        return self.ds.empty()
    
    def process_node(self, node, adj_list):
        cost, node = node
        if node in self.visited:
            return
        self.visited.add(node)
        self.result.append(node)
        for neighbor, weight in adj_list.get(node, []):
            new_cost = cost + weight
            if new_cost < self.distances[neighbor]:
                self.distances[neighbor] = new_cost
                self.add((new_cost, neighbor))
    
    def get_result(self):
        return self.distances

# --- Abstract Factory ---

class TraversalFactory(ABC):
    @abstractmethod
    def create(self, adj_list, start):
        pass

class BFSFactory(TraversalFactory):
    def create(self, adj_list, start):
        return BFSWrapper(start)

class DFSFactory(TraversalFactory):
    def create(self, adj_list, start):
        return DFSWrapper(start)

class DijkstraFactory(TraversalFactory):
    def create(self, adj_list, start):
        return DijkstraWrapper(adj_list, start)

# --- Graph Implementation with Traversal Method --- 

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

    def traverse(self, start, traversal_factory: TraversalFactory):
        # Using the factory passed as an argument to create the appropriate wrapper
        container = traversal_factory.create(self.adj_list, start)
        
        while not container.empty():
            node = container.remove()
            container.process_node(node, self.adj_list)
        
        return container.get_result()



