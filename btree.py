from enum import Enum


class Node:
    def __init__(self, node_type):
        self.node_type = node_type


class NodeType(Enum):
    INTERNAL = 0
    LEAF = 1
