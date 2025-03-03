from src.models.BaseAction import BaseAction, ActionResponse


class Status(BaseAction):
    name = "status"

    def run(self) -> ActionResponse:
        return ActionResponse("ok")


class CurrentPath(BaseAction):
    name = "current-path"

    def run(self) -> ActionResponse:
        import os
        return ActionResponse(str(os.curdir))


class Timestamp(BaseAction):
    name = "timestamp"

    def run(self) -> ActionResponse:
        import time
        return ActionResponse(str(int(time.time())))
