from typing import Text, Optional, Tuple, List


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
    MAX_ROWS = 100

    def __init__(self):
        # type: () -> None
        self.num_rows = 0
        self.rows = []  # type: List[Row]

    def add_row(self, row):
        # type: (Row) -> None
        self.num_rows += 1
        self.rows.append(row)

    def get_rows(self):
        # type: () -> List[Row]
        return self.rows
