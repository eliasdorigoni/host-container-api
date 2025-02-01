# Host Container API

This project provides a FastAPI implementation to be run inside Docker and
APIs to interact with named pipes. 

```yaml
# docker-compose.yaml
services:
  host-container-api:
    container_name: host-container-api
    command: [
      "/app/venv/bin/python", "-m", "fastapi", "run", "/app/main.py",
      "--host", "0.0.0.0",
      "--port", "8080"
    ]
    image: python:3.11
    restart: unless-stopped
    volumes:
      - ./:/app:
```
