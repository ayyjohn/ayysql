from enum import Enum

from model import Row


META_COMMAND_CHAR = "."


class MetaCommandResult(Enum):
    SUCCESS = 0
    UNRECOGNIZED_COMMAND = 1

class ExecuteStatementResult(Enum):
    EXECUTE_SUCCESS = 0
    EXECUTE_TABLE_FULL = 1

class PrepareStatementResult(Enum):
    SUCCESS = 0
    SYNTAX_ERROR = 1
    UNRECOGNIZED_STATEMENT = 2


class StatementType(Enum):
    UNKNOWN = 0
    INSERT = 1
    SELECT = 2


class Statement:
    def __init__(self, statement_type, row):
        # type: (StatementType, Row) -> Statement
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
            return PrepareStatementResult.SYNTAX_ERROR, StatementType(StatementType.UNKNOWN)
        else:
            return PrepareStatementResult.SUCCESS, insert_statement
    elif user_input.startswith("select"):
        return PrepareStatementResult.SUCCESS, Statement(StatementType.SELECT)
    else:
        return PrepareStatementResult.UNRECOGNIZED_STATEMENT, Statement(StatementType.UNKNOWN)


def execute_statement(statement):
    # type: (Statement) -> None
    if statement.statement_type == StatementType.INSERT:
        print("doing an insert")
    elif statement.statement_type == StatementType.SELECT:
        print("doing a select")
    else:
        print("unrecognized statement type")

