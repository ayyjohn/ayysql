from enum import Enum
from struct import calcsize, pack_into, unpack_from
from typing import Optional

from pager import PAGE_SIZE
from row import ROW_FORMAT, ROW_SIZE, Row

# each node will correspond to one page.
# internal nodes will point to their children by storing the page
# number that stores the child. Pages are stored in the DB file
# one after another, and the Pager asks for a page number
# and gets back a pointer to the page cache.

# a node consists of a node type (int), is_root (int),
# and a parent pointer (long)
COMMON_NODE_FORMAT = "iil"
NODE_SIZE = calcsize(COMMON_NODE_FORMAT)
# leaf nodes have the same as internal nodes plus a number of cells (long)
LEAF_NODE_HEADER_FORMAT = COMMON_NODE_FORMAT + "l"
LEAF_NODE_HEADER_SIZE = calcsize(LEAF_NODE_HEADER_FORMAT)
# leaf node bodies have a long list of keys (long) and values (Rows)
LEAF_NODE_KEY_SIZE = 4  # size of uint32_t
LEAF_NODE_VALUE_SIZE = ROW_SIZE
LEAF_NODE_SPACE_FOR_CELLS = LEAF_NODE_KEY_SIZE + LEAF_NODE_VALUE_SIZE
LEAF_NODE_CELL_FORMAT = "l" + ROW_FORMAT
LEAF_NODE_CELL_SIZE = calcsize(LEAF_NODE_CELL_FORMAT)
LEAF_NODE_MAX_CELLS = LEAF_NODE_SPACE_FOR_CELLS // LEAF_NODE_CELL_SIZE
LEAF_NODE_BODY_FORMAT = LEAF_NODE_CELL_FORMAT * LEAF_NODE_MAX_CELLS
LEAF_NODE_FORMAT = LEAF_NODE_HEADER_FORMAT + LEAF_NODE_BODY_FORMAT

nodes = {}


class Node:
    def __init__(self, parent, num_cells, cells=None, is_root=False):
        self.node_type = NodeType.LEAF
        self.parent = parent
        self.is_root = is_root
        self.num_cells = num_cells
        self.cells = cells
        if cells is None:
            self.cells = []  # type: List[Tuple[int, Row]]

        nodes[id(self)] = self

    def serialize_into(self, page):
        # type: (bytearray, int) -> None
        pack_into(
            LEAF_NODE_HEADER_FORMAT,
            page,
            0,
            self.node_type.value,
            int(self.is_root),
            id(self.parent),
            self.num_cells,
        )
        offset = LEAF_NODE_HEADER_SIZE
        for key, row in self.cells:
            pack_into(
                LEAF_NODE_CELL_FORMAT, page, offset, key, row.serialize(),
            )
            offset += LEAF_NODE_CELL_SIZE

    @classmethod
    def deserialize_from(cls, page):
        node_type, is_root, parent_id, num_cells = unpack_from(LEAF_NODE_HEADER_FORMAT, page, 0)
        offset = LEAF_NODE_HEADER_SIZE
        cells = []
        for i in range(LEAF_NODE_MAX_CELLS):
            key, id, name, email = unpack_from(LEAF_NODE_CELL_FORMAT, page, offset)
            cells.append((key, Row(id, name, email)))
            offset += LEAF_NODE_CELL_SIZE
        return cls(
            node_type=NodeType(node_type),
            is_root=bool(is_root),
            parent=nodes[parent_id],
            num_cells=num_cells,
            cells=cells,
        )

    def key(self, cell_num):
        return self.cells[cell_num][0]

    def value(self, cell_num):
        return self.cells[cell_num][1]

    @classmethod
    def initialize_root_node(cls):
        return cls(parent=None, num_cells=0, cells=None, is_root=True,)


class NodeType(Enum):
    INTERNAL = 0
    LEAF = 1
