from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import AnyStr


class BaseAction(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def run(self) -> ActionResponse:
        raise NotImplementedError


class ActionResponse:
    def __init__(self, data: AnyStr, is_success: bool = True, message: str = ""):
        self.data = str(data)
        self.is_success = is_success
        self.message = message

    def to_string(self):
        return json.dumps({
            "success": self.is_success,
            "message": self.message,
            "data": self.data,
        })
