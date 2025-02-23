import os
import selectors
from pathlib import Path
import select


def create_pipe_if_missing(pipe_path: Path):
    if not pipe_path.exists():
        os.makedirs(pipe_path.parent)
        os.mkfifo(pipe_path)


def send(message: str, pipe_path: Path, timeout_in_seconds: int = 3) -> None:
    """
    Sends a message to a named pipe, optionally raising an exception on timeout.
    :param message: JSON-formatted content
    :param pipe_path: path to the fifo file
    :param timeout_in_seconds: raises an exception after seconds passed. Set to 0 to disable
    :return: None
    """
    fd = os.open(pipe_path, os.O_WRONLY)

    if timeout_in_seconds > 0:
        ready, _, _ = select.select([], [fd], [], timeout_in_seconds)
        if not ready:
            os.close(fd)
            raise TimeoutError("Timeout reached sending data")

    with open(fd, 'w', buffering=1) as fh:
        fh.write(message)
        fh.flush()


def receive(pipe_path: Path, timeout_in_seconds: int = 1) -> str:
    """
    Receives a message from a pipe
    :param pipe_path: Path to pipe
    :param timeout_in_seconds: raises an exception after seconds passed. Set to 0 to disable
    :return: text received from pipe
    """
    with open(pipe_path, 'r') as fifo:
        sel = selectors.DefaultSelector()
        sel.register(fifo, selectors.EVENT_READ)

        if timeout_in_seconds > 0:
            events = sel.select(timeout_in_seconds)
            if not events:
                raise TimeoutError("Timeout reached receiving data")

        for key, _ in sel.select():
            # noinspection PyUnresolvedReferences
            data = key.fileobj.read().strip()
            if data:
                return data

    raise RuntimeError


def listen(fifo_path: Path) -> (str,str):
    content = receive(fifo_path, 0)
    # TODO: handle more than one line
    parts = content.split(":")
    if len(parts) == 2:
        return parts

    raise RuntimeError("Malformed content: \"{}\"".format(content))
