from fastapi import FastAPI, status, Response

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/status", status_code=status.HTTP_200_OK)
def read_status(response: Response):
    from lib.HostContainerService import HostContainerService
    try:
        return HostContainerService("status").run_action()
    except FileNotFoundError as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "success": False,
            "error": str(e)
        }
    except BrokenPipeError as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "success": False,
            "message": "Broken pipe",
            "error": str(e)
        }


@app.get("/get-{action_name}", status_code=status.HTTP_200_OK)
def read_get_from_host(action_name: str, response: Response):
    from lib.HostContainerService import HostContainerService
    service = HostContainerService("get-" + action_name)
    if not service.is_existing_command:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "success": False,
            "message": "command not found: get-" + action_name,
        }

    try:
        return service.run_action()
    except FileNotFoundError as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "success": False,
            "error": str(e)
        }
    except BrokenPipeError as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "success": False,
            "message": "Broken pipe",
            "error": str(e)
        }
