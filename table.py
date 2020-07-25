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
        # hack, in reality we shouldn't be stripping so much off the email
        # so this should just be floordiv
        # might actually work though, not sure
        self.num_rows = math.ceil(self.pager.file_length / ROW_SIZE)

    def close(self):
        # type: () -> None
        # write full pages
        num_full_pages = self.num_rows // ROWS_PER_PAGE
        for i in range(num_full_pages):
            if self.pager.pages[i] is None:
                continue

            self.pager.flush(i)
            self.pager.pages[i] = None

        # write partial final page if necessary
        num_leftover_rows = self.num_rows % ROWS_PER_PAGE
        if num_leftover_rows > 0:
            page_num = num_full_pages
            if self.pager.pages[page_num] is not None:
                self.pager.flush(page_num, num_leftover_rows)
                self.pager.pages[page_num] = None

        # clean up
        self.pager.db_file.close()
        for i in range(Table.MAX_PAGES):
            self.pager.pages[i] = None

    @classmethod
    def open(cls, filename):
        return cls(filename)
