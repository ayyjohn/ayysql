class Row:
    MAX_USERNAME_LENGTH = 32
    MAX_EMAIL_LENGTH = 255

    def __init__(
        self,
        id,  # type: int
        username,  # type: Text
        email,  # type: Text
    ):
        self.id = id
        # todo validate length against maxes
        self.username = username
        self.email = email

    def __str__(self):
        return f"Row(id: {self.id}, username: {self.username}, email: {self.email})"


class Table:
    def __init__(self):
        self.num_rows = 0
        self.pages = []
