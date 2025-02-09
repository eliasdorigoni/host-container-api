# Host Container API

This project provides a Docker container with an API to execute code on a host
machine using named pipes. A program must be running continuously in the host.

Linux only.

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

# Run

```shell
docker run --rm -p 8000:8000 -it $(docker build -q .)
```

```shell
python -m venv venv
. ./host-machine/host-pipe-handler.sh
```
