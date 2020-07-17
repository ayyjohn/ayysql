import sys

from model import Table
from commands import (
    do_meta_command,
    execute_statement,
    prepare_statement,
    ExecuteStatementResult,
    MetaCommandResult,
    META_COMMAND_CHAR,
    PrepareStatementResult,
)

from constants import NAME, PROMPT, EXECUTED, ERROR
from commands import INSERT, SELECT, META_EXIT


def run_repl():
    # type: () -> None
    table = Table()
    while True:
        print(PROMPT, end=" ")

        user_input = input().strip()

        if user_input.startswith(META_COMMAND_CHAR):
            meta_command_result = do_meta_command(user_input)
            if meta_command_result == MetaCommandResult.SUCCESS:
                continue
            elif meta_command_result == MetaCommandResult.UNRECOGNIZED_COMMAND:
                print(f"unrecognized meta command {user_input}")
                continue
        else:
            prepare_statement_result, statement = prepare_statement(user_input)
            if prepare_statement_result == PrepareStatementResult.UNRECOGNIZED_STATEMENT:
                print(f"unrecognized keyword at start of '{user_input}'")
                continue
            elif prepare_statement_result == PrepareStatementResult.FIELD_TOO_LONG:
                print(f"{ERROR} a field is too long")
                continue

            execute_result = execute_statement(statement, table)

            if execute_result == ExecuteStatementResult.SUCCESS:
                print(EXECUTED)
            elif execute_result == ExecuteStatementResult.TABLE_FULL:
                print(f"{ERROR} table full")


if __name__ == "__main__":
    run_repl()
