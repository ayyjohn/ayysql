from subprocess import Popen, PIPE, STDOUT


def run_script(commands):
    with Popen(["python", "repl.py"], stdout=PIPE, stdin=PIPE, encoding="utf8") as repl:
        for command in commands:
            repl.stdin.write(command + "\n")

        repl.stdin.close()

        output = repl.stdout.read()
    return output.split("\n")


def test__insert__when_called__creates_an_entry():
    script = [
        "insert 1 alec alec@ayyjohn.com",
        "select",
        ".exit",
    ]
    result = run_script(script)

    assert result == [
        "ayysql> executed",
        "ayysql> (id: 1, username: alec, email: alec@ayyjohn.com)",
        "executed",
        "ayysql> ",
    ]


def test__insert__too_many_rows__returns_error():
    script = [f"insert {i} alec#{i} alec{i}@ayyjohn.com" for i in range(101)]
    script.append(".exit")

    result = run_script(script)

    assert result[-2] == "ayysql> error: table full"


def test__insert__with_max_length_username_or_email__works():
    max_length_username = "a" * 32
    max_length_email = "a" * 255
    script = [
        f"insert 1 {max_length_username} {max_length_email}",
        "select",
        ".exit",
    ]

    result = run_script(script)

    assert result == [
        "ayysql> executed",
        f"ayysql> (id: 1, username: {max_length_username}, email: {max_length_email})",
        "executed",
        "ayysql> ",
    ]


def test__insert__with_too_long_username_or_email__fails():
    too_long_username = "a" * 33
    too_long_email = "a" * 256
    script = insert_select_and_exit(1, too_long_username, too_long_email)

    result = run_script(script)

    assert result == [
        "error: a field is too long",
        "executed",
        "ayysql> ",
    ]


def insert_select_and_exit(id, username, email):
    return [
        f"insert {id} {username} {email}",
        "select",
        ".exit",
    ]
