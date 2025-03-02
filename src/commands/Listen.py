import argparse

from src.core.ActionService import ActionService
from src.core.Config import Config
from src.services.PipeService import get_input_pipe, create_pipe_if_missing, listen, write_to_pipe
from src.utilities.ResponseFormatter import ResponseFormatter


def run(config: Config, args: argparse.Namespace, only_once: bool = False) -> int:
    in_pipe = get_input_pipe(config)
    action_service = ActionService(config)
    create_pipe_if_missing(in_pipe)

    while True:
        fifo_name, command_name = listen(in_pipe)
        # TODO: run the requested command in another process
        output_pipe_path = config.get("pipes_directory").joinpath(fifo_name)

        create_pipe_if_missing(output_pipe_path)

        result = action_service.execute(command_name)
        result = ResponseFormatter(result).as_success()

        write_to_pipe(result, output_pipe_path, 10)

        if only_once:
            return 0
