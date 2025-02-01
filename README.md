# Host Container API

This project provides a FastAPI implementation to be run inside Docker and
APIs to interact with named pipes. 

```yaml
# docker-compose.yaml
# assumes this is used as a submodule or nested
services:
  host-container-api:
    container_name: host-container-api
    build: ./host-container-api
    restart: unless-stopped
    volumes:
      - ./host-container-api/:/app:
```
