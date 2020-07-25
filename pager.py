import math
import os
from pathlib import Path
from typing import List, Optional, Text

from constants import BNULL
from row import ROW_SIZE

CREATE_IF_NOT_EXISTS = "rb+"

PAGE_SIZE = 4096  # bytes, 4kb is a common page size for most vm systems
ROWS_PER_PAGE = PAGE_SIZE // ROW_SIZE
Page = bytearray


class Pager:
    def __init__(self, filename, max_pages=100):
        # type: (Text, int) -> None
        try:
            Path(filename).touch(exist_ok=True)
            self.db_file = open(filename, CREATE_IF_NOT_EXISTS)
            self.file_length = os.stat(filename).st_size
        except IOError:
            print(f"couldn't open {filename}")
            exit(0)
        self.pages = [None] * max_pages  # type: List[Optional[Page]]

    def get_page(self, page_num):
        # type: (int) -> Page
        # cache miss
        if self.pages[page_num] is None:
            page = Page(PAGE_SIZE)

            # round up for partial pages
            num_pages_in_db = math.ceil(self.file_length / PAGE_SIZE)

            if page_num <= num_pages_in_db:
                self.db_file.seek(page_num * PAGE_SIZE)
                data = self.db_file.read(PAGE_SIZE)
                page[0 : len(data)] = data

            self.pages[page_num] = page
        return self.pages[page_num]  # type: ignore

    def flush(self, page_num, num_rows=ROWS_PER_PAGE):
        if self.pages[page_num] is None:
            print("tried to flush a null page")
            exit(0)

        self.db_file.seek(page_num * PAGE_SIZE)
        actual_data = self.pages[page_num][: num_rows * ROW_SIZE]
        self.db_file.write(actual_data)

    @classmethod
    def open(cls, filename, max_pages):
        # type: (Text, int) -> Pager
        return cls(filename, max_pages=max_pages)


if __name__ == "__main__":
    p = Pager.open("ayydb.db", 100)
    p.get_page(0)
