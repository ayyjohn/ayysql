import math
import os
from pathlib import Path
from typing import List, Optional, Text

from constants import BNULL
from row import ROW_SIZE

READ_WRITE_BINARY = "rb+"

PAGE_SIZE = 4096  # bytes, 4kb is a common page size for most vm systems
ROWS_PER_PAGE = PAGE_SIZE // ROW_SIZE
Page = bytearray


class Pager:
    def __init__(self, filename, max_pages=100):
        # type: (Text, int) -> None
        create_db_file(filename)

        try:
            self.db_file = open(filename, READ_WRITE_BINARY)
        except IOError:
            print(f"couldn't open {filename}")
            exit(0)

        self.file_length = os.stat(filename).st_size
        self.pages = [None] * max_pages  # type: List[Optional[Page]]

    def shutdown(self):
        self.db_file.close()

    def get_page(self, page_num):
        # type: (int) -> Page
        page = self.try_to_fetch_page_from_cache(page_num)
        if page is None:
            page = self.get_page_from_disk(page_num)
            self.cache_page(page_num, page)
        return page

    def has_page_cached(self, page_num):
        return self.pages[page_num] is not None

    def try_to_fetch_page_from_cache(self, page_num):
        # type: (int) -> Optional[Page]
        return self.pages[page_num]

    def get_page_from_disk(self, page_num):
        # type: (int) -> Page
        page = Page(PAGE_SIZE)
        num_pages_in_db = math.ceil(self.file_length / PAGE_SIZE)

        if page_num <= num_pages_in_db:
            self.db_file.seek(page_num * PAGE_SIZE)
            data = self.db_file.read(PAGE_SIZE)
            page[0 : len(data)] = data
        return page

    def cache_page(self, page_num, page):
        # type: (int, Page) -> None
        self.pages[page_num] = page

    def purge_cached_page(self, page_num):
        # type: (int) -> None
        self.pages[page_num] = None

    def flush_page_to_disk(self, page_num, num_rows=ROWS_PER_PAGE):
        if not self.has_page_cached(page_num):
            print("tried to flush a null page")
            exit(0)

        self.db_file.seek(page_num * PAGE_SIZE)
        row_data = self.pages[page_num][: num_rows * ROW_SIZE]
        self.db_file.write(row_data)

    @classmethod
    def open(cls, filename, max_pages):
        # type: (Text, int) -> Pager
        return cls(filename, max_pages=max_pages)


def create_db_file(filename):
    Path(filename).touch(exist_ok=True)
