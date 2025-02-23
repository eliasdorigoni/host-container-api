from pathlib import Path

from lib.CommandService import CommandService
from lib.Configuration import Configuration


def main():
    config = Configuration(Path(__file__).parent)
    commands = CommandService.get_available_commands(config)
    print("Available commands:")
    for item in commands:
        print("  - \"{command_name}\" ({class_name})".format(
            command_name=item["command_name"],
            class_name=item["class_name"],
        ))


if __name__ == '__main__':
    main()
