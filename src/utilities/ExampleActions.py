from src.models.BaseAction import BaseAction


class Status(BaseAction):
    name = "status"

    def run(self):
        return "ok"


class CurrentPath(BaseAction):
    name = "current-path"

    def run(self):
        import os
        return os.curdir


class Timestamp(BaseAction):
    name = "timestamp"

    def run(self):
        import time
        return str(int(time.time()))
