#!/bin/bash

THIS_DIR=$( cd -- "$( /usr/bin/dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && /usr/bin/pwd )
CONTAINER_TO_HOST_PIPE="$THIS_DIR""/pipes/container_to_host.pipe"
HOST_COMMANDS_PATH="$THIS_DIR""/host-commands"
PIPES_PATH="$THIS_DIR""/pipes"

# Creates fifo file if it does not exist
create_fifo_if_not_exists() {
    [[ -p "$1" ]] || mkfifo "$1"
}

# Creates files in output path with the names in actions directory
create_pipes_from_script_names() {
    SCRIPTS=$( find -P "$HOST_COMMANDS_PATH" -type f -name "*.sh" -printf "%f\n" | cut -d"/" -f2 | sed 's/.sh//g' )

    echo $SCRIPTS

    while IFS=' ' read -ra NAME; do
        create_fifo_if_not_exists "$PIPES_PATH""/""$NAME"".pipe"
    done <<< "$SCRIPTS"
}

# If incoming pipe has data, runs the command
check_incoming_pipe() {
  INPUT=$( cat "$CONTAINER_TO_HOST_PIPE" )
  if [[ -z "$INPUT" ]]; then
      return
  fi

  if [[ $( echo "$INPUT" | wc -l ) -ne 1 ]]; then
      echo "ERROR: only one line expected"
      return
  fi

  if [ "$INPUT" == "get-date" ] \
    || [ "$INPUT" == "status" ] \
    || [ "$INPUT" == "get-home-server-existing-services" ] \
    || [ "$INPUT" == "get-home-server-running-containers" ] \
    || [ "$INPUT" == "get-proxymanager-hosts" ]; then
    source "$HOST_COMMANDS_PATH""/""$INPUT"".sh" > "$PIPES_PATH""/""$INPUT"".pipe"
    return
  fi

  print "ERROR: unknown action ""$INPUT"
}


create_pipes_from_script_names
create_fifo_if_not_exists "$CONTAINER_TO_HOST_PIPE"

while true
do
  check_incoming_pipe
done
