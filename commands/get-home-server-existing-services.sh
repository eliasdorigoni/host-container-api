#!/bin/bash

COMMAND_DIR=$( cd -- "$( /usr/bin/dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && /usr/bin/pwd )
source "$COMMAND_DIR""/../.env"

/usr/bin/docker compose -f "$HOMESERVER_DOCKERCOMPOSE_YAML_PATH" config --format json
