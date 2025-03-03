import argparse

from src.core.ActionService import ActionService
from src.core.Config import Config
from src.models.BaseAction import ActionResponse
from src.services.PipeService import get_input_pipe, create_pipe_if_missing, listen, write_to_pipe


def run(config: Config, args: argparse.Namespace, only_once: bool = False) -> int:
    in_pipe = get_input_pipe(config)
    action_service = ActionService(config)
    create_pipe_if_missing(in_pipe)

    while True:
        fifo_name, command_name = listen(in_pipe)
        # TODO: run the requested command in another process
        output_pipe_path = config.get("pipes_directory").joinpath(fifo_name)

        create_pipe_if_missing(output_pipe_path)

        # noinspection PyBroadException
        try:
            result = action_service.execute(command_name)
        except BaseException as e:
            result = ActionResponse(str(e), False, "Unexpected exception raised")

        write_to_pipe(result.to_string(), output_pipe_path, 10)

        if only_once:
            return 0
