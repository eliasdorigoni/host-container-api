import os
import selectors
from pathlib import Path

import select


# noinspection PyMethodMayBeStatic
class FifoHandler:
    def __init__(self, send_pipe_path: Path, receive_pipe_path: Path):
        if not Path(send_pipe_path).is_fifo():
            raise FileNotFoundError("FIFO file missing: {}".format(send_pipe_path.name))

        if not Path(receive_pipe_path).is_fifo():
            raise FileNotFoundError("FIFO file not found: {}".format(receive_pipe_path))

        self.send_pipe_path = send_pipe_path
        self.receive_pipe_path = receive_pipe_path

    def transmit(self, message: str, send_timeout: int = 1, receive_timeout: int = 3) -> str:
        try:
            # TODO: Lock process and continue, or wait until lock is removed
            self.__send(message, self.send_pipe_path, send_timeout)
            return self.__receive(self.receive_pipe_path, receive_timeout)
        except BaseException as e:
            raise e
        finally:
            # TODO: Remove lock
            pass

    def __send(self, message: str, fifo_path: Path, timeout_in_seconds: int) -> None:
        fd = os.open(fifo_path, os.O_WRONLY | os.O_NONBLOCK)
        ready, _, _ = select.select([], [fd], [], timeout_in_seconds)

        if not ready:
            os.close(fd)
            raise TimeoutError("Timeout reached sending data")

        with open(fd, 'w', buffering=1) as fh:
            fh.write(message)
            fh.flush()

    def __receive(self, fifo_path: Path, timeout_in_seconds: int) -> str:
        with open(fifo_path, 'r') as fifo:
            sel = selectors.DefaultSelector()
            sel.register(fifo, selectors.EVENT_READ)
            events = sel.select(timeout_in_seconds)
            if not events:
                raise TimeoutError("Timeout reached receiving data")

            for key, _ in sel.select():
                # noinspection PyUnresolvedReferences
                data = key.fileobj.read().strip()
                if data:
                    return data

        raise RuntimeError
