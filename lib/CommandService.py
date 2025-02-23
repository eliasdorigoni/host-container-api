import importlib
import inspect
import os
from importlib.util import spec_from_file_location
from pathlib import Path

from lib.Configuration import Configuration
import lib.AbstractCommand


class CommandService:
    pipes_path = Path(__file__).resolve().parent.parent.joinpath('pipes')

    def __init__(self, config: Configuration):
        self.config = config
        self.commands = {}
        self.load_commands()

    def execute(self, command_name: str):
        if command_name not in self.commands:
            raise NotImplementedError("Command not found")

        return self.commands[command_name]().run()

    def load_commands(self) -> None:
        src_path = self.config.root_path.joinpath('lib')
        self.commands = self.commands | self.get_classes_from_file(src_path, 'Commands.py')

        src_path = self.config.root_path.joinpath('custom')
        if src_path.exists():
            for filename in os.listdir(src_path):
                self.commands = self.commands | self.get_classes_from_file(src_path, filename)

    # noinspection PyMethodMayBeStatic
    def get_classes_from_file(self, source_path, filename) -> dict:
        classes = {}
        if not filename.endswith(".py") or filename == "__init__.py":
            return classes

        module_name = filename[:-3]
        module_path = os.path.join(source_path, filename)

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_name and issubclass(obj, lib.AbstractCommand.AbstractCommand):
                classes[obj.name] = obj
        return classes

    def get_available_commands(self) -> list[dict]:
        _list = []

        for name, obj in self.commands.items():
            _list.append({
                "command_name": name,
                "class_name": obj.__name__,
            })

        return _list
