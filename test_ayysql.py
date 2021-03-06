from commands import INSERT, META_EXIT, SELECT
from subprocess import PIPE, STDOUT, Popen, run
from typing import Callable, List, Text

import pytest  # type: ignore
from constants import EXECUTED, PROMPT, UTF8

STATEMENT_WITH_NULL_RETURN_EXECUTED = f"{PROMPT} {EXECUTED}"
INSERT_STATEMENT_EXECUTED = STATEMENT_WITH_NULL_RETURN_EXECUTED
PRINTED_PROMPT = f"{PROMPT} "


def setup_function(function):
    # type: (Callable) -> None
    run(["rm", "-rf", "ayydb.db"])


def run_script(commands):
    # type: (List[Text]) -> List[Text]
    with Popen(["./ayysql", "ayydb.db"], stdout=PIPE, stdin=PIPE, encoding=UTF8) as repl:
        for command in commands:
            repl.stdin.write(command + "\n")  # type: ignore

        repl.stdin.close()  # type: ignore

        output = repl.stdout.read()  # type: ignore
    return output.split("\n")


def test__startup__when_wrong_number_of_args__fails():
    # type: () -> None
    with Popen(["./ayysql"], stdout=PIPE, encoding=UTF8) as repl:
        output = repl.stdout.read()  # type: ignore
    assert output == "must provide db file name and nothing else\n"

    with Popen(["./ayysql", "ayydb.db", "weird_extra_arg"], stdout=PIPE, encoding=UTF8) as repl:
        output = repl.stdout.read()  # type: ignore
    assert output == "must provide db file name and nothing else\n"


def test__insert__when_called__creates_an_entry():
    # type: () -> None
    script = insert_select_and_exit("1", "alec", "alec@ayyjohn.com")
    result = run_script(script)

    assert result == [
        INSERT_STATEMENT_EXECUTED,
        f"{PROMPT} (id: 1, username: alec, email: alec@ayyjohn.com)",
        EXECUTED,
        PRINTED_PROMPT,
    ]


def test__insert__too_many_rows__returns_error():
    script = [f"insert {i} alec#{i} alec{i}@ayyjohn.com" for i in range(1401)]
    script.append(".exit")

    result = run_script(script)

    assert result[-2] == f"{PROMPT} error: table full"


def test__insert__with_max_length_username_or_email__works():
    # type: () -> None
    max_length_username = "a" * 32
    max_length_email = "a" * 255
    script = insert_select_and_exit("1", max_length_username, max_length_email)

    result = run_script(script)

    assert result == [
        INSERT_STATEMENT_EXECUTED,
        f"{PROMPT} (id: 1, username: {max_length_username}, email: {max_length_email})",
        EXECUTED,
        PRINTED_PROMPT,
    ]


def test__insert__with_too_long_username_or_email__fails():
    # type: () -> None
    too_long_username = "a" * 33
    too_long_email = "a" * 256
    script = insert_select_and_exit("1", too_long_username, too_long_email)

    result = run_script(script)

    assert result == [
        f"{PROMPT} error: a field is too long",
        STATEMENT_WITH_NULL_RETURN_EXECUTED,
        PRINTED_PROMPT,
    ]


def test__insert__with_non_int_id__fails():
    # type: () -> None
    script = insert_select_and_exit("INVALID_ID", "alec", "alec@ayyjohn.com")

    result = run_script(script)

    assert result == [
        f"{PROMPT} error: the given ID is invalid",
        STATEMENT_WITH_NULL_RETURN_EXECUTED,
        PRINTED_PROMPT,
    ]


def test__insert__persists_data_between_runs():
    # type: () -> None
    first_script = insert_select_and_exit("1", "alec", "alec@ayyjohn.com")

    run_script(first_script)

    second_script = select_and_exit()
    result = run_script(second_script)

    assert result == [
        f"{PROMPT} (id: 1, username: alec, email: alec@ayyjohn.com)",
        EXECUTED,
        PRINTED_PROMPT,
    ]


def insert_select_and_exit(id, username, email):
    # type: (Text, Text, Text) -> List[Text]
    return [
        f"insert {id} {username} {email}",
        SELECT,
        META_EXIT,
    ]


def select_and_exit():
    # type: () -> List[Text]
    return [SELECT, META_EXIT]
