import sys
from commands import (
    INSERT,
    META_COMMAND_CHAR,
    META_EXIT,
    SELECT,
    ExecuteStatementResult,
    MetaCommandResult,
    PrepareStatementResult,
    do_meta_command,
    execute_statement,
    prepare_statement,
)
from typing import Text

from constants import ERROR, EXECUTED, NAME, PROMPT
from table import Table


def run_repl(db_filename):
    # type: (Text) -> None
    table = Table.open(db_filename)
    while True:
        print(PROMPT, end=" ")

        user_input = input().strip()

        if user_input.startswith(META_COMMAND_CHAR):
            meta_command_result = do_meta_command(user_input, table)
            if meta_command_result == MetaCommandResult.SUCCESS:
                continue
            elif meta_command_result == MetaCommandResult.UNRECOGNIZED_COMMAND:
                print(f"unrecognized meta command {user_input}")
                continue
        else:
            statement, prepare_statement_result = prepare_statement(user_input)
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
