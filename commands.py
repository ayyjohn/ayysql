from enum import Enum
from typing import Optional, Text, Tuple

from cursor import Cursor
from row import Row
from table import Table

META_COMMAND_CHAR = "."
META_EXIT = f"{META_COMMAND_CHAR}exit"
INSERT = "insert"
SELECT = "select"


class MetaCommandResult(Enum):
    SUCCESS = 0
    UNRECOGNIZED_COMMAND = 1


class ExecuteStatementResult(Enum):
    SUCCESS = 0
    TABLE_FULL = 1
    INVALID_STATEMENT = 2


class PrepareStatementResult(Enum):
    SUCCESS = 0
    SYNTAX_ERROR = 1
    FIELD_TOO_LONG = 2
    UNRECOGNIZED_STATEMENT = 3


class StatementType(Enum):
    UNKNOWN = 0
    INSERT = 1
    SELECT = 2


class Statement:
    def __init__(self, statement_type, row=None):
        # type: (StatementType, Optional[Row]) -> None
        self.statement_type = statement_type
        self.row = row

    def __str__(self):
        return f"{self.statement_type.name} statement: {self.row}"


def do_meta_command(user_input, table):
    # type (Text, Table) -> Optional[MetaCommandResult]
    if user_input == META_EXIT:
        table.close()
        exit(0)
    else:
        return MetaCommandResult.UNRECOGNIZED_COMMAND


def prepare_statement(user_input):
    # type: (Text) -> Tuple[Statement, PrepareStatementResult]
    if user_input.startswith(INSERT):
        return prepare_insert(user_input)
    elif user_input.startswith(SELECT):
        return prepare_select(user_input)
    else:
        return (
            Statement(StatementType.UNKNOWN),
            PrepareStatementResult.UNRECOGNIZED_STATEMENT,
        )


def prepare_insert(user_input):
    # type: (Text) -> Tuple[Statement, PrepareStatementResult]
    try:
        _, id, username, email = user_input.split(" ")

        if not all([id, username, email]):
            return Statement(StatementType.UNKNOWN), PrepareStatementResult.SYNTAX_ERROR

        if len(username) > Row.MAX_USERNAME_LENGTH or len(email) > Row.MAX_EMAIL_LENGTH:
            return Statement(StatementType.UNKNOWN), PrepareStatementResult.FIELD_TOO_LONG

        row = Row(int(id), username, email)
    except ValueError:
        return Statement(StatementType.UNKNOWN), PrepareStatementResult.SYNTAX_ERROR
    else:
        insert_statement = Statement(StatementType.INSERT, row)
        return insert_statement, PrepareStatementResult.SUCCESS


def prepare_select(user_input):
    # type: (Text) -> Tuple[Statement, PrepareStatementResult]
    return Statement(StatementType.SELECT), PrepareStatementResult.SUCCESS


def execute_statement(statement, table):
    # type: (Statement, Table) -> ExecuteStatementResult
    if statement.statement_type == StatementType.INSERT:
        return execute_insert(statement.row, table)
    elif statement.statement_type == StatementType.SELECT:
        return execute_select(statement, table)
    else:
        return ExecuteStatementResult.INVALID_STATEMENT


def execute_insert(row, table):
    # type: (Optional[Row], Table) -> ExecuteStatementResult
    if row is None:
        return ExecuteStatementResult.INVALID_STATEMENT

    if table.num_rows >= Table.MAX_ROWS:
        return ExecuteStatementResult.TABLE_FULL

    cursor = Cursor.table_end(table)
    cursor.insert_row(row)

    return ExecuteStatementResult.SUCCESS


def execute_select(statement, table):
    # type: (Statement, Table) -> ExecuteStatementResult
    cursor = Cursor.table_start(table)

    while not cursor.end_of_table:
        page, offset = cursor.cursor_value()
        row = Row.deserialize_from(page, offset)
        print(row)
        cursor.advance()
    return ExecuteStatementResult.SUCCESS
