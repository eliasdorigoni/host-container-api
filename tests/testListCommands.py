import io
import unittest
from pathlib import Path

from src.commands import ListActions
from src.core.Config import Config


class TestListCommands(unittest.TestCase):
    def test_list_receives_expected_data(self):
        config = Config()

        buffer = io.StringIO()
        ListActions.run(config, None, buffer)
        output = buffer.getvalue()

        self.assertTrue("Status" in output, "Status class name not in output")
        self.assertTrue("status" in output, "Status action name not in output")
        self.assertTrue("CurrentPath" in output, "CurrentPath class name not in output")
        self.assertTrue("current-path" in output, "CurrentPath action name not in output")
