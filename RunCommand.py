import sys

from lib.CommandService import CommandService


def main(command_name: str):
    cs = CommandService(command_name)
    if not cs.exists():
        exit(1)
    print(cs.execute())


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("ERROR: expected one argument")
        exit(1)

    main(sys.argv[1])
