import importlib
import inspect
import os
from importlib.util import spec_from_file_location

from src.core.Config import Config
from src.models.BaseAction import BaseAction, ActionResponse


class ActionService:
    def __init__(self, config: Config):
        self.config = config
        self.actions = {}
        self.load_actions()

    def execute(self, name: str) -> ActionResponse:
        if name not in self.actions:
            raise NotImplementedError("Action not found")

        return self.actions[name]().run()

    def load_actions(self) -> None:
        src_path = self.config.root_path.joinpath('src')
        self.actions = self.get_classes_from_file(src_path, 'models/ExampleActions.py')

        src_path = self.config.root_path.joinpath('custom-actions')
        if src_path.exists():
            for filename in os.listdir(src_path):
                self.actions = self.actions | self.get_classes_from_file(src_path, filename)

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
            if obj.__module__ == module_name and issubclass(obj, BaseAction):
                classes[obj.name] = obj
        return classes

    def get_available_actions(self) -> list[dict]:
        _list = []

        for name, obj in self.actions.items():
            _list.append({
                "action_name": name,
                "class_name": obj.__name__,
            })

        return _list
