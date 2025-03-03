import json
import os
import subprocess
import time
import unittest
from pathlib import Path

from src.core.Config import Config
from src.services import PipeService
from src.services.PipeService import get_input_pipe


class TestPipeService(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.test_pipe_path = PipeService.get_test_pipe(self.config)
        PipeService.create_pipe_if_missing(self.test_pipe_path)

    def tearDown(self):
        if self.test_pipe_path.exists():
            os.remove(self.test_pipe_path)

    def run_program_with(self, options: list[str]):
        project_path = Path(__file__).parent.parent
        executable = project_path.joinpath("venv/bin/python").absolute()
        command = [executable, project_path] + options

        import warnings
        with warnings.catch_warnings(action="ignore"):
            subprocess.Popen(command)

    def test_can_receive_content(self):
        content = str(int(time.time()))
        self.run_program_with(["test-write"])

        # If this step is stuck for more than 2 seconds, exit with CTRL+C.
        pipe_content = PipeService.read_from_pipe(self.test_pipe_path.absolute(), 2)
        self.assertEqual(content, pipe_content)

    def test_can_send_content(self):
        input_pipe = get_input_pipe(self.config)
        output_pipe_path = self.config.get("pipes_directory").joinpath("test-output.pipe")
        message = "test-output.pipe:timestamp"

        PipeService.create_pipe_if_missing(input_pipe)
        PipeService.create_pipe_if_missing(output_pipe_path)

        self.run_program_with(["listen-once", "--read-timeout=3"])

        PipeService.write_to_pipe(message, input_pipe, 3)
        content = PipeService.read_from_pipe(output_pipe_path, 3)

        timestamp = int(json.loads(content)["data"])
        delay_threshold = 2
        now = int(time.time())
        if now - timestamp > delay_threshold:
            self.fail("content has no valid timestamp ({}): {}".format(str(now), content))

