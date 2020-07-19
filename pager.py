import math
import os
from typing import List, Optional, Text

CREATE_IF_NOT_EXISTS = "wb+"


PAGE_SIZE = 4096  # bytes, 4kb is a common page size for most vm systems
Page = bytearray


class Pager:
    def __init__(self, filename, max_pages=100):
        # type: (Text, int) -> None
        try:
            self.db_file = open(filename, CREATE_IF_NOT_EXISTS)
            self.file_length = os.path.getsize(filename)
        except IOError:
            print(f"couldn't open {filename}")
            exit(0)
        self.pages = [None] * max_pages  # type: List[Optional[Page]]

    def get_page(self, page_num):
        # type: (int) -> Page
        # cache miss
        if self.pages[page_num] is None:
            print("cache miss")
            page = Page(PAGE_SIZE)
            print(page)
            # round up for partial pages
            num_pages_in_db = math.ceil(self.file_length / PAGE_SIZE)

            if page_num <= num_pages_in_db:
                self.db_file.seek(page_num * PAGE_SIZE, whence=1)
                print("reading from file")
                print(f"fetching page num {page_num}")
                page = Page(self.db_file.read(PAGE_SIZE))
                print(page)

            self.pages[page_num] = page
            print(f"page num {page_num} is now {page}")
            print(self.pages[page_num])
            return self.pages[page_num]
        else:
            print("cache hit")
            print(self.pages)
            return self.pages[page_num]

    def flush(self, page_num, size):
        if self.pages[page_num] is None:
            print("tried to flush a null page")
            exit(0)

        offset = self.db_file.seek(page_num * PAGE_SIZE)
        self.db_file.write(self.pages[page_num], size)

    @classmethod
    def open(cls, filename, max_pages):
        # type: (Text, int) -> Pager
        return cls(filename, max_pages=max_pages)
