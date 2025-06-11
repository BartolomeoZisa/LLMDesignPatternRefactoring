import os
import matplotlib.pyplot as plt
import networkx as nx
import data.tools.modules.graphutils as graphutils



def visualize_registered_patterns(checker):
    combined = nx.DiGraph()
    pos = {}
    offset_x = 0
    
    for pattern_name, pattern_cls in checker.subgraph_classes.items():
        # Build pattern graph
        G = pattern_cls().build()
        
        # Relabel nodes to avoid clashes and keep pattern name as prefix
        mapping = {n: f"{pattern_name}:{n}" for n in G.nodes()}
        H = nx.relabel_nodes(G, mapping)
        
        # Add to combined graph
        combined = nx.compose(combined, H)
        
        # Generate positions for nodes in this pattern's subgraph using a layout
        # Then offset x-coordinates to separate subgraphs horizontally
        pos_sub = nx.spring_layout(H, seed=42)
        # Shift all x coords by offset_x
        pos_sub = {node: (x + offset_x, y) for node, (x, y) in pos_sub.items()}
        pos.update(pos_sub)
        
        # Increase offset for next subgraph (adjust spacing as needed)
        offset_x += 3.0
    
    # Draw combined graph
    plt.figure(figsize=(12, 6))
    nx.draw(combined, pos, with_labels=True, node_size=1000, node_color='lightblue', arrowsize=20, font_size=9)
    plt.title("Registered Subgraph Patterns Visualization")
    plt.show()

# Usage:
checker = graphutils.SubgraphChecker()
visualize_registered_patterns(checker)
