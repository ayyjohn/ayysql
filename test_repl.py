from subprocess import Popen, PIPE, STDOUT


def run_script(commands):
    with Popen(["python", "repl.py"], stdout=PIPE, stdin=PIPE, encoding="utf8") as repl:
        for command in commands:
            repl.stdin.write(command + "\n")

        repl.stdin.close()

        output = repl.stdout.read()
    return output.split("\n")


def test__insert__when_called__creates_an_entry():
    result = run_script(["insert 1 alec alec@ayyjohn.com", "select", ".exit",])
    assert result == [
        "ayysql> executed",
        "ayysql> (id: 1, username: alec, email: alec@ayyjohn.com)",
        "executed",
        "ayysql> ",
    ]
