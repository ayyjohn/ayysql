from enum import Enum
from typing import Text, Optional, Tuple
from model import Row, Table


META_COMMAND_CHAR = "."


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
    UNRECOGNIZED_STATEMENT = 2


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


def do_meta_command(user_input):
    # type (Text) -> Optional[MetaCommandResult]
    if user_input == ".exit":
        exit(0)
    else:
        return MetaCommandResult.UNRECOGNIZED_COMMAND


def prepare_statement(user_input):
    # type: (Text) -> Tuple[PrepareStatementResult, Statement]
    if user_input.startswith("insert"):
        try:
            _, id, username, email = user_input.split(" ")
            insert_statement = Statement(StatementType.INSERT, Row(int(id), username, email))
        except ValueError:
            return PrepareStatementResult.SYNTAX_ERROR, Statement(StatementType.UNKNOWN)
        else:
            return PrepareStatementResult.SUCCESS, insert_statement
    elif user_input.startswith("select"):
        return PrepareStatementResult.SUCCESS, Statement(StatementType.SELECT)
    else:
        return PrepareStatementResult.UNRECOGNIZED_STATEMENT, Statement(StatementType.UNKNOWN)


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
    if not row:
        return ExecuteStatementResult.INVALID_STATEMENT

    if table.num_rows >= Table.MAX_ROWS:
        return ExecuteStatementResult.TABLE_FULL

    table.add_row(row)
    return ExecuteStatementResult.SUCCESS


def execute_select(statement, table):
    # type: (Statement, Table) -> ExecuteStatementResult
    for row in table.get_rows():
        print(row)
    return ExecuteStatementResult.SUCCESS
