from fastapi import FastAPI, status, Response
from lib.HostContainerService import HostContainerService

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/commands/{action_name}", status_code=status.HTTP_200_OK)
def read_get_from_host(action_name: str, response: Response):
    service = HostContainerService(action_name)
    if not service.is_existing_command:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "success": False,
            "message": "Command not found: " + action_name,
        }

    try:
        return {
            "success": True,
            "data": service.run_action()
        }
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
