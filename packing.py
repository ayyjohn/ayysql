from struct import calcsize, pack_into, unpack_from
from typing import Text, Tuple, Union

from constants import NULL, UTF8

# to pack/unpack a row, we need to know the types
# currently a row consists of an id (int), and two strings of length 32 and 255
ROW_FORMAT = "i32s255s"
ROW_SIZE = calcsize(ROW_FORMAT)


def serialize_row(row, page, offset):
    # type: (Row, bytearray, int) -> None
    return pack_into(ROW_FORMAT, page, offset, row.id, b(row.username), b(row.email))


def b(s):
    # type: (Text) -> bytes
    return bytes(s, UTF8)


def deserialize_row(page, offset):
    # type: (bytearray, int) -> Tuple[int, Text, Text]
    id, name, email = unpack_from(ROW_FORMAT, page, offset)
    name = name.decode(UTF8).rstrip(NULL)
    email = email.decode(UTF8).rstrip(NULL)
    return (id, name, email)
