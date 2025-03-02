import errno
import os
import selectors
import time
from pathlib import Path

from src.core.Config import Config


def create_pipe_if_missing(pipe_path: Path):
    if not pipe_path.exists():
        os.makedirs(pipe_path.parent, exist_ok=True)
        os.mkfifo(pipe_path)


def read_from_pipe(pipe_path: Path, timeout_in_seconds: int = 0) -> str | None:
    """
    Returns the content of `pipe_path`. Blocks the execution until content is
    received unless `timeout_in_seconds` is greater than zero.

    :param pipe_path: Path to named pipe
    :param timeout_in_seconds: 0 to wait indefinitely for content, or any number
    :return: string or None if timeout is reached
    """
    if timeout_in_seconds == 0:
        with open(pipe_path, 'r') as f:
            return f.read().strip()

    sel = selectors.DefaultSelector()
    fd = os.open(pipe_path, os.O_RDONLY | os.O_NONBLOCK)
    with os.fdopen(fd, 'r') as infile:
        sel.register(infile, selectors.EVENT_READ)
        start_time = time.time()

        while time.time() - start_time < timeout_in_seconds:
            events = sel.select(timeout=0.2)  # Check every 200 ms
            if events:
                for key, _ in events:
                    data = key.fileobj.read()
                    if data:
                        return data.strip()

    return None


def write_to_pipe(message: str, pipe_path: Path, timeout_in_seconds: int = 3) -> None:
    """
    Sends a message to a named pipe, raising an exception on timeout.

    :param message: JSON-formatted content
    :param pipe_path: path to the fifo file
    :param timeout_in_seconds: raises an exception after seconds passed. Set to 0 to disable
    :return: None
    """

    if timeout_in_seconds == 0:
        with open(pipe_path, 'w') as f:
            f.write(message)
            f.flush()
        return

    start_time = time.time()
    while time.time() - start_time < timeout_in_seconds:
        try:
            fd = os.open(pipe_path, os.O_WRONLY | os.O_NONBLOCK)
            with os.fdopen(fd, 'w', buffering=1) as outfile:
                outfile.write(message)
                outfile.flush()
            return
        except OSError as e:
            if e.errno in (errno.EAGAIN, errno.EWOULDBLOCK, errno.ENXIO):
                time.sleep(0.2)
            else:
                raise e

    raise TimeoutError("Timeout reached")


def listen(pipe_path: Path) -> (str, str):
    content = read_from_pipe(pipe_path, 0)
    # TODO: handle more than one line
    parts = content.split(":")
    if len(parts) == 2:
        return parts

    raise RuntimeError("Malformed content: \"{}\"".format(content))


def get_input_pipe(config: Config) -> Path:
    """
    Returns the absolute path to the input named pipe
    """
    pipe: Path = config.get("input_pipe_filename")
    assert isinstance(pipe, str)

    root: Path = config.get("pipes_directory")
    assert isinstance(root, Path)

    return root.joinpath(pipe).absolute()


def get_test_pipe(config: Config) -> Path:
    """
    Returns the absolute path to the test named pipe
    """
    pipe: Path = config.get("test_pipe_filename")
    assert isinstance(pipe, str)

    root: Path = config.get("pipes_directory")
    assert isinstance(root, Path)

    return root.joinpath(pipe).absolute()


def get_pipe(pipe_name: str, config: Config, check_pipe_exists=False) -> Path:
    """
    Returns the absolute path to a named pipe, optionally checking if it exists
    """
    root: Path = config.get("pipes_directory")
    assert root is Path

    return Path(pipe_name).relative_to(root).absolute()
