from functools import reduce
from pathlib import Path

import yaml


class Config:
    def __init__(self):
        self.root_path = Path(__file__).parent.parent.parent.absolute()
        self.content = None
        with open(self.root_path.joinpath("config.yaml"), 'r') as stream:
            self.content = yaml.load(stream, Loader=yaml.CLoader)

        self.content["pipes_directory"] = self.__maybe_resolve_path(self.content["pipes_directory"])

    def __maybe_resolve_path(self, p: str) -> Path:
        p = Path(p)
        if p.is_absolute():
            return p

        return self.root_path.joinpath(p).resolve()

    def get(self, key_name: str, default_value=None):
        def search_key(_dict, _key):
            if _key in _dict:
                return _dict[_key]
            return None

        value = reduce(search_key, key_name.split("."), self.content)
        return value if value is not None else default_value
