#!/bin/bash

COMMAND_DIR=$( cd -- "$( /usr/bin/dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && /usr/bin/pwd )
source "$COMMAND_DIR""/../.env"

CONTAINER_DATA=$( /usr/bin/docker compose -f "$HOMESERVER_DOCKERCOMPOSE_YAML_PATH" ps --format json )

# Each line in CONTAINER_DATA is a json object,
# so it needs to be converted to an array.
printf "["$( echo "$CONTAINER_DATA" | sed 's/$/,/' )"]" | sed 's/,]$/]/'
