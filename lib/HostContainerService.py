import os
from pathlib import Path

import select


class HostContainerService:
    pipes_path = Path(__file__).resolve().parent.parent.joinpath('pipes')
    commands_path = Path(__file__).resolve().parent.parent.joinpath('host-commands')

    def __init__(self, name: str):
        self.commands = self.get_available_commands()
        self.command_name = name
        self.is_existing_command = (name in self.commands)

    # noinspection PyMethodMayBeStatic
    def get_available_commands(self) -> list[str]:
        commands = []
        for _, _, files in os.walk(self.commands_path):
            commands = files

        return commands

    def run_action(self):
        out_fifo_path = self.pipes_path.joinpath('container_to_host.pipe')
        in_fifo_path = self.pipes_path.joinpath(self.command_name + '.pipe')
        timeout_in_seconds = 3

        if not os.path.exists(out_fifo_path):
            raise FileNotFoundError('Missing fifo file: ' + out_fifo_path.name)
        elif not os.path.exists(in_fifo_path):
            raise FileNotFoundError('Missing fifo file: ' + in_fifo_path.name)

        with open(out_fifo_path, 'w') as fh:
            fh.write(self.command_name)

        with open(in_fifo_path, 'r') as fh:
            while True:
                readable, writable, exceptional = select.select([fh], [], [fh], timeout_in_seconds)
                if not (readable or writable or exceptional):
                    raise BrokenPipeError("Timeout reached for command " + self.command_name)
                return fh.read()
