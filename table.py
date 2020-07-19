from typing import List, Optional, Text, Tuple

from pager import PAGE_SIZE, Page, Pager
from row import ROW_SIZE, ROWS_PER_PAGE, Row


class Table:
    MAX_PAGES = 100
    MAX_ROWS = ROWS_PER_PAGE * MAX_PAGES

    def __init__(self, filename):
        # type: (Text) -> None
        self.filename = filename
        self.pager = Pager.open(filename, max_pages=Table.MAX_PAGES)
        self.num_rows = self.pager.file_length // ROW_SIZE

    def get_rows(self):
        # type: () -> List[Row]
        rows = []
        for row_num in range(self.num_rows):
            page, offset = self.page_location(row_num)
            rows.append(Row.deserialize_from(page, offset))
        return rows

    # todo rename this?
    def page_location(self, row_num):
        # type: (int) -> Tuple[Page, int]
        page_num = row_num // ROWS_PER_PAGE
        print(f"fetching page_num {page_num}")
        page = self.pager.get_page(page_num)

        row_offset = row_num % ROWS_PER_PAGE
        byte_offset = row_offset * ROW_SIZE

        return (page, byte_offset)

    def insert_row(self, row):
        # type: (Row) -> None
        page, offset = self.page_location(self.num_rows)
        print("testing")
        print(page)
        print(offset)
        row.serialize_into(page, offset)
        self.num_rows += 1

    def close(self):
        # type: () -> None
        # write full pages
        num_full_pages = self.num_rows // ROWS_PER_PAGE
        for i in range(num_full_pages):
            if self.pager.pages[i] is None:
                continue

            self.pager.flush(i, PAGE_SIZE)
            self.pager.pages[i] = None

        num_leftover_rows = self.num_rows % ROWS_PER_PAGE
        if num_leftover_rows > 0:
            page_num = num_full_pages
            if self.pager.pages[page_num] is not None:
                self.pager.flush(page_num, num_leftover_rows * ROW_SIZE)
                self.pager.pages[page_num] = None

        self.pager.db_file.close()

        for i in range(Table.MAX_PAGES):
            self.pager.pages[i] = None

    @classmethod
    def open(cls, filename):
        return cls(filename)
