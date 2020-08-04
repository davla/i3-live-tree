"""Serialize i3ipc.aio.Con

This module monkey-patches the i3ipc.aio.Con class to add custom serialization
to string
"""

from functools import partial
from itertools import chain

from i3ipc.aio import Con

FOCUSED_COLOR = '\033[91m'
RESET = '\033[0m'


def serialize_node(self: Con, indent_level=0) -> str:
    """Return the serialization of a single node"""
    content = self.name or self.layout
    text = f'{FOCUSED_COLOR}{content}{RESET}' if self.focused else content
    return " " * (indent_level * 2) + text


def serialize_tree(self: Con, indent_level=0):
    """Return depth-first serialization of the whole tree"""
    this_node = self.serialize_node(indent_level)

    serialize_children = partial(serialize_tree, indent_level=indent_level + 1)
    children = map(serialize_children, self.nodes)

    all_nodes = chain((this_node,), children)
    return '\n'.join(all_nodes)


Con.serialize_node = serialize_node
Con.__str__ = serialize_tree
