import os
import selectors
from pathlib import Path


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
            [commands.append(os.path.splitext(f)[0]) for f in files]
        return commands

    def run_action(self):
        out_fifo_path = self.pipes_path.joinpath('container_to_host.pipe')
        in_fifo_path = self.pipes_path.joinpath(self.command_name + '.pipe')
        timeout_in_seconds = 3

        if not os.path.exists(out_fifo_path):
            raise FileNotFoundError('Missing fifo file: ' + out_fifo_path.name)
        elif not os.path.exists(in_fifo_path):
            raise FileNotFoundError('Missing fifo file: ' + in_fifo_path.name)

        # Send
        with open(out_fifo_path, 'w') as fh:
            fh.write(self.command_name)

        # Receive
        sel = selectors.DefaultSelector()
        with open(in_fifo_path, 'r') as fifo:
            sel.register(fifo, selectors.EVENT_READ)
            events = sel.select(timeout_in_seconds)
            if not events:
                raise TimeoutError("No data received within the timeout period.")

            for key, _ in sel.select():
                data = key.fileobj.read().strip()
                if data:
                    return data

        raise RuntimeError("No data received from named pipe.")
