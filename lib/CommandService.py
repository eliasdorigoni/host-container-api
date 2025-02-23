import importlib
import inspect
import os
from importlib.util import spec_from_file_location
from pathlib import Path

from lib.Configuration import Configuration
from lib.FifoHandler import FifoHandler
import lib.AbstractCommand
import custom


class CommandService:
    pipes_path = Path(__file__).resolve().parent.parent.joinpath('pipes')

    def __init__(self, name: str):
        self.command = self.get_command_from_name(name)

    def exists(self):
        return self.command is not None

    # noinspection PyMethodMayBeStatic
    def get_command_from_name(self, name: str) -> type[lib.AbstractCommand.AbstractCommand] | None:
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

    @staticmethod
    def get_classes_from_file(source_path, filename):
        classes = []
        if not filename.endswith(".py") or filename == "__init__.py":
            return classes

        module_name = filename[:-3]
        module_path = os.path.join(source_path, filename)

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_name and issubclass(obj, lib.AbstractCommand.AbstractCommand):
                classes.append({
                    "class_name": name,
                    "command_name": obj.name,
                })
        return classes

    @staticmethod
    def get_available_commands(config: Configuration):
        src_path = config.root_path.joinpath('lib')
        command_list = CommandService.get_classes_from_file(src_path, 'Commands.py')

        src_path = config.root_path.joinpath('custom')
        for filename in os.listdir(src_path):
            command_list = command_list + CommandService.get_classes_from_file(src_path, filename)

        return command_list
