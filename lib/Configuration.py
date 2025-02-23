from functools import reduce
from pathlib import Path

import yaml


class Configuration:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.content = None
        with open(root_path.joinpath("config.yaml"), 'r') as stream:
            self.content = yaml.load(stream, Loader=yaml.CLoader)

    def get(self, key_name: str, default_value=None):
        def search_key(_dict, _key):
            if _key in _dict:
                return _dict[_key]
            return None

        value = reduce(search_key, key_name.split("."), self.content)
        return value if value is not None else default_value
