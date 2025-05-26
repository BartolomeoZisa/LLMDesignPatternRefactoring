import networkx as nx
from networkx.algorithms import isomorphism
import matplotlib.pyplot as plt



graph_paths = {
    "uml_factory": "../results/creational/factory/monster/llm/monster_factorymethod_gpt-4o-mini-2024-07-18_20250521_180751/uml/classes_monster.dot",
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
    
    @staticmethod
    def convert_multidigraph_to_digraph(multi_digraph):
        G = nx.DiGraph()
        for u, v, data in multi_digraph.edges(data=True):
            G.add_edge(u, v, **data)
        return G



class SubgraphChecker:
    
    subgraph_classes = {}

    @classmethod
    def register(cls, pattern_cls):
        name = pattern_cls.__name__.lower()
        cls.subgraph_classes[name] = pattern_cls
        return pattern_cls

    @classmethod
    def get_subgraph(cls, name):
        if name not in cls.subgraph_classes:
            raise ValueError(f"Subgraph '{name}' is not registered.")
        return cls.subgraph_classes[name]().build()

    def check(self, graph, pattern_names):
        if isinstance(pattern_names, str):
            pattern_names = [pattern_names]

        results = {}
        for pattern_name in pattern_names:
            pattern_graph = self.get_subgraph(pattern_name)
            matcher = isomorphism.GraphMatcher(graph, pattern_graph)
            results[pattern_name] = matcher.subgraph_is_isomorphic()
        return results


class GraphVisualizer:
    def __init__(self, graph):
        """
        Initialize with a NetworkX graph (DiGraph, MultiDiGraph, etc.)
        """
        self.graph = graph

    def draw(self, title=None, node_color='lightblue', node_size=1500, font_size=12,
             edge_color='gray', arrows=True, save_path=None):
        """
        Visualize the graph.
        
        Args:
            title (str): Optional title for the plot.
            node_color (str or list): Color(s) of nodes.
            node_size (int): Size of nodes.
            font_size (int): Size of node labels.
            edge_color (str or list): Color(s) of edges.
            arrows (bool): Show arrows for directed graphs.
            save_path (str): If provided, save the plot to this path instead of showing.
        """
        plt.figure(figsize=(8, 6))

        # Use spring layout for nice spacing
        pos = nx.spring_layout(self.graph)

        nx.draw_networkx_nodes(self.graph, pos, node_color=node_color, node_size=node_size)
        nx.draw_networkx_edges(self.graph, pos, edge_color=edge_color, arrows=arrows)
        nx.draw_networkx_labels(self.graph, pos, font_size=font_size)

        if title:
            plt.title(title)
        plt.axis('off')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()




@SubgraphChecker.register
class Strategy:
    def build(self):
        G = nx.DiGraph()
        G.add_edge("Strategy", "Context")
        G.add_edge("ConcreteStrategy", "Strategy")
        return G

@SubgraphChecker.register
class FactoryMethod:
    def build(self):
        G = nx.DiGraph()
        G.add_edge("ConcreteCreator", "Creator")
        G.add_edge("ConcreteProduct", "Product")
        return G

@SubgraphChecker.register
class Adapter:
    def build(self):
        G = nx.DiGraph()
        G.add_edge("Adapter", "Target")
        G.add_edge("Adaptee", "Adapter")    
        return G

@SubgraphChecker.register
class State:
    def build(self):
        G = nx.DiGraph()
        #G.add_edge("Context", "State") is this always true?
        G.add_edge("ConcreteState", "State")
        G.add_edge("State", "Context") 
        return G

@SubgraphChecker.register
class Decorator:
    def build(self):
        G = nx.DiGraph()
        G.add_edge("Decorator", "Component")
        G.add_edge("ConcreteDecorator", "Decorator")
        G.add_edge("ConcreteComponent", "Component")
        G.add_edge("Component", "Decorator")
        return G



