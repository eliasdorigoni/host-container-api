#!/bin/bash

COMMAND_DIR=$( cd -- "$( /usr/bin/dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && /usr/bin/pwd )
source "$COMMAND_DIR""/../.env"

TOKEN=$( curl -s -X POST \
    -H "Content-Type: application/json" \
    -d '{"identity": "'"$PROXYMANAGER_USER"'", "secret": "'"$PROXYMANAGER_SECRET"'"}' \
    "http://localhost:81/api/tokens" | jq ".token" | sed 's/"//g' )

curl -s -H "Authorization: Bearer ""$TOKEN" "http://localhost:81/api/nginx/proxy-hosts"
