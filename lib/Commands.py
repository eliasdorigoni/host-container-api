from abc import ABC, abstractmethod


class AbstractCommand(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError


class Status(AbstractCommand):
    name = "status"

    def run(self):
        return "ok"


class Date(AbstractCommand):
    name = "date"

    def run(self):
        return "12345"
