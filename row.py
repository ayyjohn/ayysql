import sys
from struct import calcsize, pack, pack_into, unpack, unpack_from
from typing import List, Optional, Text, Tuple, Union

from constants import NULL, UTF8

# to pack/unpack a row, we need to know the types
# currently a row consists of an id (int), and two strings of length 32 and 255
ROW_FORMAT = "i32s255s"
# 291 according to testing
ROW_SIZE = calcsize(ROW_FORMAT)


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
        self.username = username
        self.email = email

    def __str__(self):
        # type: () -> Text
        return f"(id: {self.id}, username: {self.username}, email: {self.email})"

    def serialize_into(self, page, offset):
        # type: (bytearray, int) -> None
        pack_into(ROW_FORMAT, page, offset, self.id, b(self.username), b(self.email))

    @classmethod
    def deserialize_from(cls, page, offset):
        # type: (bytearray, int) -> Row
        id, name, email = unpack_from(ROW_FORMAT, page, offset)
        name = name.decode(UTF8).rstrip(NULL)
        email = email.decode(UTF8).rstrip(NULL)
        return cls(id, name, email)


def b(s):
    # type: (Text) -> bytes
    return bytes(s, UTF8)
