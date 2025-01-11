# Plotting NetworkX as PyGraphViz
import networkx as nx
import matplotlib as mpl

from ecosystems.viz.color_utils import tabcmapper


def visualize_taxonomy(taxonomy: nx.MultiDiGraph, filename: str,):
    # Write a PNG file of the taxonomy to filename
    A = nx.nx_agraph.to_agraph(taxonomy)
    A.graph_attr.update(overlap='prism')  # Required to enable overlap_scaling
    A.graph_attr.update(overlap_scaling='3')  # Adjust this value as needed
    A.layout("twopi")

    A.draw(filename)
