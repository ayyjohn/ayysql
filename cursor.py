from typing import Tuple

from btree import Node
from pager import ROWS_PER_PAGE, Page
from row import ROW_SIZE, Row
from table import Table


class Cursor:
    def __init__(self, table, page_num, is_at_end_of_table):
        # type: (Table, int, bool) -> None
        self.table = table
        self.page_num = table.root_page_num
        self.cell_num = 0
        root_node_page = table.pager.get_page(table.root_page_num)
        root_node = Node.deserialize_from(root_node_page)
        num_cells = root_node.num_cells
        self.is_at_end_of_table = num_cells == 0

    def location(self):
        # type: () -> Tuple[Page, int]
        page_num = self.page_num
        page = self.table.pager.get_page(page_num)
        return Node.deserialize_from(page).value(self.cell_num)

    def advance(self):
        page_num = self.page_num
        page = self.table.pager.get_page(page_num)
        node = Node.deserialize_from(page)
        self.cell_num += 1
        if self.cell_num >= node.num_cells:
            self.is_at_end_of_table = True

    def insert_leaf_node(self, key, row):
        current_page = self.table.pager.get_page(self.page_num)
        current_node = Node.deserialize_from(current_page)
        num_cells = current_node.num_cells
        if num_cells >= LEAF_NODE_MAX_CELLS:
            # node is full
            raise NotImplementedError("need to implement splitting leaf nodes")
            exit(0)
        
        

    def insert_row(self, row):
        # type: (Row) -> None
        page, offset = self.location()
        row.serialize_into(page, offset)
        self.table.num_rows += 1

    @classmethod
    def table_start(cls, table):
        # type: (Table) -> Cursor
        page_num = table.root_page_num
        cell_num = 0
        root_node_page = table.pager.get_page(table.root_page_num)
        root_node = Node.deserialize_from(root_node_page)
        num_cells = root_node.num_cells
        is_at_end_of_table = num_cells == 0

        return cls(table, cell_num, is_at_end_of_table)

    @classmethod
    def table_end(cls, table):
        # type: (Table) -> Cursor
        page_num = table.root_page_num
        root_node_page = table.pager.get_page(table.root_page_num)
        root_node = Node.deserialize_from(root_node_page)
        num_cells = root_node.num_cells
        is_at_end_of_table = True

        return cls(table, num_cells, is_at_end_of_table)
