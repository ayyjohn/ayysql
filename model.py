import sys
from struct import pack, unpack
from typing import List, Optional, Text, Tuple

from constants import UTF8
from packing import ROW_SIZE, deserialize_row, serialize_row

PAGE_SIZE = 4096  # bytes, 4kb is a common page size for most vm systems
ROWS_PER_PAGE = PAGE_SIZE // ROW_SIZE


class Row:
    MAX_USERNAME_LENGTH = 32
    MAX_EMAIL_LENGTH = 255

    def __init__(
        self,
        id,  # type: int
        username,  # type: Text
        email,  # type: Text
    ):
        # type: (...) -> None
        self.id = id
        # todo validate length against maxes
        self.username = username
        self.email = email

    def __str__(self):
        return f"(id: {self.id}, username: {self.username}, email: {self.email})"


class Table:
    MAX_PAGES = 100
    MAX_ROWS = ROWS_PER_PAGE * MAX_PAGES

    def __init__(self):
        # type: () -> None
        self.num_rows = 0
        self.pages = [None] * Table.MAX_PAGES

    def get_rows(self):
        # type: () -> List[Row]
        rows = []
        for row_num in range(self.num_rows):
            page, offset = self.row_slot(row_num)
            id, name, email = deserialize_row(page, offset)
            rows.append(Row(id, name, email))
        return rows

    # todo rename this?
    def row_slot(self, row_num):
        # type: (int) -> Tuple[bytearray, int]
        page_num = row_num // ROWS_PER_PAGE
        page = self.pages[page_num]

        if page == None:
            page = self.pages[page_num] = bytearray(PAGE_SIZE)

        row_offset = row_num % ROWS_PER_PAGE
        byte_offset = row_offset * ROW_SIZE
        return (page, byte_offset)

    def insert_row(self, row):
        # type: (Row) -> None
        page, offset = self.row_slot(self.num_rows)
        serialize_row(row, page, offset)
        self.num_rows += 1
