import json


class ResponseFormatter:
    def __init__(self, content=None):
        self.content = content

    def as_success(self, optional_message: str = None):
        return json.dumps({
            "success": True,
            "message": optional_message,
            "data": self.content,
        })

    def as_error(self, optional_message: str = None):
        return json.dumps({
            "success": False,
            "message": optional_message,
            "data": self.content,
        })
