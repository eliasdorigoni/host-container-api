from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/get-{action_name}")
def read_get_from_host(action_name: str):
    from lib.HostContainerService import HostContainerService
    service = HostContainerService("get-" + action_name)
    if not service.is_existing_command:
        return {
            "error": "command not found",
            "command-name": "get-" + action_name,
        }

    return service.run_action()
