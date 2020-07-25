from typing import Tuple

from pager import ROWS_PER_PAGE, Page
from row import ROW_SIZE, Row
from table import Table


class Cursor:
    def __init__(self, table, row_num, end_of_table):
        # type: (Table, int, bool) -> None
        self.table = table
        self.row_num = row_num
        self.end_of_table = end_of_table

    def cursor_value(self):
        # type: () -> Tuple[Page, int]
        page_num = self.row_num // ROWS_PER_PAGE
        page = self.table.pager.get_page(page_num)

        row_offset = self.row_num % ROWS_PER_PAGE
        byte_offset = row_offset * ROW_SIZE

        return (page, byte_offset)

    def advance(self):
        self.row_num += 1
        if self.row_num >= self.table.num_rows:
            self.end_of_table = True

    def insert_row(self, row):
        # type: (Row) -> None
        page, offset = self.cursor_value()
        row.serialize_into(page, offset)
        self.table.num_rows += 1

    @classmethod
    def table_start(cls, table):
        # type: (Table) -> Cursor
        end_of_table = table.num_rows == 0
        return cls(table, 0, end_of_table)

    @classmethod
    def table_end(cls, table):
        # type: (Table) -> Cursor
        return cls(table, table.num_rows, True)