import argparse


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python .",
        description="Listens to a named pipe and executes programs based on its content."
    )
    parser.add_argument(
        "action",
        type=str,
        help="Either 'listen', 'listen-once' or 'list-actions', or 'test-write' for testing.",
    )
    parser.add_argument(
        "--read-timeout",
        action="store",
        default=0,
        help="Stops reading if this amount of seconds have passed without receiving content. "
             "Default 0 is no timeout."
    )
    parser.add_argument(
        "--write-timeout",
        action="store",
        default=3,
        help="Stops sending content if this amount of seconds have passed and no program is listening. "
             "Default 3 seconds."
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose mode."
    )

    return parser.parse_args()
