import sys
from enum import Enum

from typing import Text, Optional, Tuple

META_COMMAND_CHAR = "."


class MetaCommandResult(Enum):
    SUCCESS = 0
    UNRECOGNIZED_COMMAND = 1


class PrepareStatementResult(Enum):
    SUCCESS = 0
    SYNTAX_ERROR = 1
    UNRECOGNIZED_STATEMENT = 2


class StatementType(Enum):
    UNKNOWN = 0
    INSERT = 1
    SELECT = 2


def do_meta_command(user_input):
    # type (Text) -> Optional[MetaCommandResult]
    if user_input == ".exit":
        exit(0)
    else:
        return MetaCommandResult.UNRECOGNIZED_COMMAND


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


class Statement:
    def __init__(self, statement_type, row):
        # type: (StatementType, Row) -> Statement
        self.statement_type = statement_type
        self.row = row

    def __str__(self):
        return f"{self.statement_type.name} statement: {self.row}"


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


def run_repl():
    # type: () -> None
    while True:
        print("ayysql> ", end="")

        user_input = input().strip()

        if user_input.startswith(META_COMMAND_CHAR):
            meta_command_result = do_meta_command(user_input)
            if meta_command_result == MetaCommandResult.SUCCESS:
                continue
            elif meta_command_result == MetaCommandResult.UNRECOGNIZED_COMMAND:
                print(f"unrecognized command {user_input}")
                continue
        else:
            prepare_statement_result, statement = prepare_statement(user_input)
            if prepare_statement_result == PrepareStatementResult.UNRECOGNIZED_STATEMENT:
                print(f"Unrecognized keyword at start of '{user_input}'")
                continue

            execute_statement(statement)
            print("executed")


if __name__ == "__main__":
    run_repl()
