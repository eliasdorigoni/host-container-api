from lib.AbstractCommand import AbstractCommand


class Status(AbstractCommand):
    name = "status"

    def run(self):
        return "ok"


class CurrentPath(AbstractCommand):
    name = "current-path"

    def run(self):
        import os
        return os.curdir
