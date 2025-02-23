import os
from pathlib import Path

from lib.CommandService import CommandService
from lib.Configuration import Configuration
from lib import FifoHandler
from lib.ResponseFormatter import ResponseFormatter


def main():
    config = Configuration(Path(__file__).parent)
    in_pipe = config.get("pipes_directory").joinpath(config.get("input_pipe_filename"))
    cs = CommandService(config)
    FifoHandler.create_pipe_if_missing(in_pipe)
    while True:
        fifo_name, command_name = FifoHandler.listen(in_pipe)
        output_pipe_path = config.get("pipes_directory").joinpath(fifo_name)

        FifoHandler.create_pipe_if_missing(output_pipe_path)

        result = cs.execute(command_name)
        result = ResponseFormatter(result).as_success()

        FifoHandler.send(result, output_pipe_path, 10)


if __name__ == '__main__':
    main()
