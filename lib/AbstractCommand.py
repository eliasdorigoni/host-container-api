from abc import ABC, abstractmethod


class AbstractCommand(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError
