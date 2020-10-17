import math
from typing import List, Optional, Text, Tuple

from btree import Node, nodes
from pager import PAGE_SIZE, ROWS_PER_PAGE, Page, Pager
from row import ROW_SIZE, Row


class Table:
    MAX_PAGES = 100
    MAX_ROWS = ROWS_PER_PAGE * MAX_PAGES

    def __init__(self, filename):
        # type: (Text) -> None
        self.filename = filename
        self.pager = Pager.open(filename, max_pages=Table.MAX_PAGES)
        self.root_page_num = 0

        if self.pager.num_pages == 0:
            # new db file
            root_node_page = self.pager.get_page(0)
            root_node = Node.initialize_root_node()
            nodes[id(root_node)] = root_node

    def close(self):
        # type: () -> None
        self.write_full_pages_to_disk()
        self.pager.shutdown()

    def write_full_pages_to_disk(self):
        # type: () -> None
        num_full_pages = self.num_rows // ROWS_PER_PAGE
        for page_num in range(self.pager.num_pages):
            if not self.pager.has_page_cached(page_num):
                continue

            self.pager.flush_page_to_disk(page_num)

    @classmethod
    def open(cls, filename):
        return cls(filename)
