from src.commands import ListActions, Listen, ListenOnce, TestWrite
from src.core.Config import Config
from src.core.ProgramArguments import get_arguments


def main():
    config = Config()
    args = get_arguments()

    match args.action:
        case "listen-once":
            return ListenOnce.run(config, args)
        case "list-actions":
            return ListActions.run(config)
        case "listen":
            return Listen.run(config, args)
        case "test-write":
            return TestWrite.run(config)
        case _:
            return 1


if __name__ == '__main__':
    main()
