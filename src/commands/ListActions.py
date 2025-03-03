import argparse

from src.core.ActionService import ActionService
from src.core.Config import Config


def run(config: Config, custom_output=None) -> int:
    actions = ActionService(config).get_available_actions()
    print("Available actions:", file=custom_output)
    for item in actions:
        print('  - "{}" ({})'.format(
            item["action_name"],
            item["class_name"],
        ), file=custom_output)

    return 0
