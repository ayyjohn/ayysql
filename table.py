from typing import List, Optional, Tuple

from row import PAGE_SIZE, ROW_SIZE, ROWS_PER_PAGE, Page, Row


class Table:
    MAX_PAGES = 100
    MAX_ROWS = ROWS_PER_PAGE * MAX_PAGES

    def __init__(self):
        # type: () -> None
        self.num_rows = 0
        self.pages = [None] * Table.MAX_PAGES  # type: List[Optional[Page]]

    def get_rows(self):
        # type: () -> List[Row]
        rows = []
        for row_num in range(self.num_rows):
            page, offset = self.row_slot(row_num)
            rows.append(Row.deserialize_from(page, offset))
        return rows

    # todo rename this?
    def row_slot(self, row_num):
        # type: (int) -> Tuple[Page, int]
        page_num = row_num // ROWS_PER_PAGE
        page = self.pages[page_num]

        if page is None:
            page = self.pages[page_num] = Page(PAGE_SIZE)

        row_offset = row_num % ROWS_PER_PAGE
        byte_offset = row_offset * ROW_SIZE
        return (page, byte_offset)

    def insert_row(self, row):
        # type: (Row) -> None
        page, offset = self.row_slot(self.num_rows)
        row.serialize_into(page, offset)
        self.num_rows += 1
