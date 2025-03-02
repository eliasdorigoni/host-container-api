import argparse

from src.commands import Listen
from src.core.Config import Config


def run(config: Config, args: argparse.Namespace) -> int:
    return Listen.run(config, args, True)
