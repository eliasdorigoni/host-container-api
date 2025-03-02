import time

from src.core.Config import Config
from src.services.PipeService import write_to_pipe, get_test_pipe


def run(config: Config) -> int:
    config = Config()
    pipe_path = get_test_pipe(config)
    try:
        write_to_pipe(str(int(time.time())), pipe_path, 5)
        return 0
    except TimeoutError:
        return 1
