"""Handle dependeny resolutions"""
import json


class DependencyGraph:

    def __init__(self, metadata, template_list):

        default_template = metadata["default"]

        # Initialise nodes from passed in template_list names
        nodes = {n: Node(n) for n in template_list}
        if default_template not in nodes:
            nodes[default_template] = Node(default_template)

        # Add in edges if dependencies are listed in the metadata
        for k, v in nodes.items():
            deps = metadata['dependencies'].get(k, None)
            if deps:
                for d in deps:
                    v.add_edge(nodes[d])

        self.nodes = nodes

    def get_dependencies(self, template_name):

        node = self.nodes[template_name]

        resolution_order = self._resolve(node)

        template_order = [n.name for n in resolution_order]

        return template_order

    def _resolve(self, node, resolved=None, seen=None):
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
                    raise Exception('Circular reference detected: %s -&gt; %s' %
                                    (node.name, edge.name))
                self._resolve(edge, resolved, seen)
        resolved.append(node)

        return resolved


class Node:
    """A simple class to represent a node in a graph"""

    def __init__(self, name):
        self.name = name
        self.edges = []

    def add_edge(self, node):
        self.edges.append(node)
