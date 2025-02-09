#!/bin/bash

THIS_DIR=$( cd -- "$( /usr/bin/dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && /usr/bin/pwd )
INCOMING_COMMANDS_PIPE_PATH="$THIS_DIR""/../pipes/container_to_host.pipe"
HOST_COMMANDS_DIRECTORY="$THIS_DIR""/commands"
PIPES_PATH="$THIS_DIR""/pipes"

# Creates fifo file if it does not exist
create_fifo_if_not_exists() {
    [[ -p "$1" ]] || mkfifo "$1"
}

# Creates files in output path with the names in actions directory
create_pipes_from_script_names() {
    SCRIPTS=$( find -P "$HOST_COMMANDS_DIRECTORY" -type f -name "*.sh" -printf "%f\n" | cut -d"/" -f2 | sed 's/.sh//g' )
    while IFS=' ' read -ra NAME; do
        # shellcheck disable=SC2128
        create_fifo_if_not_exists "$PIPES_PATH""/""$NAME"".pipe"
    done <<< "$SCRIPTS"
}

# If incoming pipe has data, runs the command
check_incoming_pipe() {
  INPUT=$( cat "$INCOMING_COMMANDS_PIPE_PATH" )
  if [[ -z "$INPUT" ]]; then
      return
  fi

  if [[ $( echo "$INPUT" | wc -l ) -ne 1 ]]; then
      echo "ERROR: only one line expected"
      return
  fi

  if ! [[ "$INPUT" =~ ^[a-z0-9-_]$ ]]; then
    echo "ERROR: command must follow the pattern ^[a-z0-9-_]$"
    return
  fi

  COMMAND_PATH="$HOST_COMMANDS_DIRECTORY""/""$INPUT"".sh"
  if ! [ -f "$COMMAND_PATH" ]; then
    echo "ERROR: unknown action ""$INPUT"
    return
  fi

  # shellcheck source=/dev/null
  source "$COMMAND_PATH" > "$PIPES_PATH""/""$INPUT"".pipe"
}

create_pipes_from_script_names
create_fifo_if_not_exists "$INCOMING_COMMANDS_PIPE_PATH"

while true
do
  check_incoming_pipe
done
