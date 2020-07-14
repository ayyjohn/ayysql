import sys
from typing import Text, Optional, Tuple

from model import Row
from commands import (
    do_meta_command,
    execute_statement,
    prepare_statement,
    MetaCommandResult,
    META_COMMAND_CHAR,
    PrepareStatementResult,
)


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
