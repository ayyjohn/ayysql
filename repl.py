import sys

if __name__ == "__main__":
    while True:
        print("ayysql> ", end="")
        user_input = input().strip()
        if user_input == ".exit":
            sys.exit(0)
        else:
            print(f"unrecognized command {user_input}")

