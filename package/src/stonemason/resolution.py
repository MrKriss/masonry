"""Handle dependeny resolutions"""
import json


class Node:
    """A simple class to represent a node in a graph"""
    def __init__(self, name):
        self.name = name
        self.edges = []

    def add_edge(self, node):
        self.edges.append(node)


def create_dependency_graph(filename, node_list):
    """ Return a dictionary of Node instances representing the Dependency Graph """

    meta_data = json.load(open(filename))

    # Initialise nodes from passed in node_list names
    nodes = {n: Node(n) for n in node_list}

    # Add in edges if dependencies are listed in the meta_data
    for k, v in nodes.items():
        deps = meta_data['dependencies'].get(k, None)
        if deps:
            for d in deps:
                v.add_edge(nodes[d])

    return nodes


def resolve(node, resolved=None, seen=None):
    """Graph dependency resolution algorithm 

    Parameters
    ----------
    node: Node
        The node instance for which dependencies should be resolved

    Referenes
    ---------

        Source code obtained form the following paper. 

    .. https://www.electricmonk.nl/docs/dependency_resolving_algorithm/dependency_resolving_algorithm.html
        
    """
    if resolved is None:
        resolved = []
    if seen is None:
        seen = []

    seen.append(node)
    for edge in node.edges:
        if edge not in resolved:
            if edge in seen:
                raise Exception('Circular reference detected: %s -&gt; %s' % (node.name, edge.name))
            resolve(edge, resolved, seen)
    resolved.append(node)

    return resolved
