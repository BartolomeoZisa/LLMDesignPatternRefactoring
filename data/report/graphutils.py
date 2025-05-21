import networkx as nx
from networkx.algorithms import isomorphism


graph_paths = {
    "uml_vector": "../results/behavioural/strategy/vector/llm/Vector_strategy_gpt-4o-mini-2024-07-18_20250520_225946/uml/classes_Vector.dot",
}

class GraphParser:
    @staticmethod
    def read_graph(path):
        """Load a single graph from a dot file."""
        return nx.nx_agraph.read_dot(path)

    @staticmethod
    def read_graphs_from_paths(path_dict):
        """
        Load multiple graphs from a dictionary of {name: path}.
        Returns dict {name: graph}.
        """
        graphs = {}
        for name, path in path_dict.items():
            graphs[name] = GraphParser.read_graph(path)
        return graphs


class SubgraphChecker:
    def __init__(self):
        self.subgraph_classes = {}

    def register(self, cls):
        name = cls.__name__
        self.subgraph_classes[name] = cls
        return cls

    def get_subgraph(self, name):
        if name not in self.subgraph_classes:
            raise ValueError(f"Subgraph '{name}' is not registered.")
        return self.subgraph_classes[name]().build()

    def check(self, graph, pattern_names):
        # graph: a single nx.Graph or nx.DiGraph
        # pattern_names: list or single string of pattern class names to check

        if isinstance(pattern_names, str):
            pattern_names = [pattern_names]

        results = {}
        for pattern_name in pattern_names:
            pattern_graph = self.get_subgraph(pattern_name)
            matcher = isomorphism.GraphMatcher(graph, pattern_graph)
            results[pattern_name] = matcher.subgraph_is_isomorphic()
        return results


checker = SubgraphChecker()

@checker.register
class Strategy:
    def build(self):
        G = nx.DiGraph()
        G.add_edge("Context", "Strategy")
        G.add_edge("ConcreteStrategy", "Strategy")
        return G

@checker.register
class FactoryMethod:
    def build(self):
        G = nx.DiGraph()
        G.add_edge("Creator", "Product")
        G.add_edge("ConcreteCreator", "Creator")
        G.add_edge("ConcreteProduct", "Product")
        return G

@checker.register
class Adapter:
    def build(self):
        G = nx.DiGraph()
        G.add_edge("Adapter", "Adaptee")
        G.add_edge("Adapter", "Target")
        return G

@checker.register
class State:
    def build(self):
        G = nx.DiGraph()
        G.add_edge("Context", "State")
        G.add_edge("ConcreteState", "State")
        return G

@checker.register
class Decorator:
    def build(self):
        G = nx.DiGraph()
        G.add_edge("Decorator", "Component")
        G.add_edge("ConcreteDecorator", "Decorator")
        return G

