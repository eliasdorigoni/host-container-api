import inspect
from pathlib import Path

import lib.Commands
from lib.FifoHandler import FifoHandler


class CommandService:
    pipes_path = Path(__file__).resolve().parent.parent.joinpath('pipes')

    def __init__(self, name: str):
        self.command = self.get_command_from_name(name)

    def exists(self):
        return self.command is not None

    # noinspection PyMethodMayBeStatic
    def get_command_from_name(self, name: str) -> type[lib.Commands.AbstractCommand] | None:
        for _, obj in inspect.getmembers(lib.Commands):
            if inspect.isclass(obj) and issubclass(obj, lib.Commands.AbstractCommand) and obj.name == name:
                return obj

        return None

    def request_execution(self):
        fh = FifoHandler(
            self.pipes_path.joinpath('container_to_host.pipe'),
            self.pipes_path.joinpath(str(self.command.name) + '.pipe')
        )
        return fh.transmit(str(self.command.name))
