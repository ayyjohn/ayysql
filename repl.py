import sys
from enum import Enum

META_COMMAND_CHAR = "."


class MetaCommandResult(Enum):
    SUCCESS = 0
    UNRECOGNIZED_COMMAND = 1


class PrepareStatementResult(Enum):
    SUCCESS = 0
    UNRECOGNIZED_STATEMENT = 1


class StatementType(Enum):
    INSERT = 0
    SELECT = 1


def do_meta_command(user_input):
    if user_input == ".exit":
        exit(0)
    else:
        return MetaCommandResult.UNRECOGNIZED_COMMAND


class Statement:
    def __init__(self, statement_type):
        self.statement_type = statement_type


def prepare_statement(user_input):
    if user_input.startswith("insert"):
        return PrepareStatementResult.SUCCESS, Statement(StatementType.INSERT)
    elif user_input.startswith("select"):
        return PrepareStatementResult.SUCCESS, Statement(StatementType.SELECT)
    else:
        return PrepareStatementResult.UNRECOGNIZED_STATEMENT, None


def execute_statement(statement):
    if statement.statement_type == StatementType.INSERT:
        print("doing an insert")
    elif statement.statement_type == StatementType.SELECT:
        print("doing a select")


if __name__ == "__main__":
    # initialize repl
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

