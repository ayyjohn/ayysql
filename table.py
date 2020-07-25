import math
from typing import List, Optional, Text, Tuple

from pager import PAGE_SIZE, ROWS_PER_PAGE, Page, Pager
from row import ROW_SIZE, Row


class Table:
    MAX_PAGES = 100
    MAX_ROWS = ROWS_PER_PAGE * MAX_PAGES

    def __init__(self, filename):
        # type: (Text) -> None
        self.filename = filename
        self.pager = Pager.open(filename, max_pages=Table.MAX_PAGES)
        self.num_rows = self.pager.file_length // ROW_SIZE

    def close(self):
        # type: () -> None
        self.write_full_pages_to_disk()
        self.write_partial_page_to_disk()
        self.pager.shutdown()

    def write_full_pages_to_disk(self):
        # write full pages
        num_full_pages = self.num_rows // ROWS_PER_PAGE
        for page_num in range(num_full_pages):
            if not self.pager.has_page_cached(page_num):
                continue

            self.pager.flush_page_to_disk(page_num)

    def write_partial_page_to_disk(self):
        # write partial final page if necessary
        num_leftover_rows = self.num_rows % ROWS_PER_PAGE
        if num_leftover_rows > 0:
            page_num = self.num_rows // ROWS_PER_PAGE
            if self.pager.has_page_cached(page_num):
                self.pager.flush_page_to_disk(page_num, num_leftover_rows)

    @classmethod
    def open(cls, filename):
        return cls(filename)
