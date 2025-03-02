import argparse

from src.core.ActionService import ActionService
from src.core.Config import Config


def run(config: Config, args: argparse.Namespace | None, custom_output=None) -> int:
    commands = ActionService(config).get_available_commands()
    print("Available commands:", file=custom_output)
    for item in commands:
        print("  - \"{command_name}\" ({class_name})".format(
            command_name=item["command_name"],
            class_name=item["class_name"],
        ), file=custom_output)

    return 0
