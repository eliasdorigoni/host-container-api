#!/bin/bash

THIS_DIR=$( cd -- "$( /usr/bin/dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && /usr/bin/pwd )
INCOMING_COMMANDS_PIPE_PATH="$THIS_DIR""/pipes/container_to_host.pipe"
PIPES_PATH="$THIS_DIR""/pipes"
PYTHON_EXEC_PATH="$THIS_DIR""/venv/bin/python"
SCRIPT_PATH="$THIS_DIR""/RunCommand.py"

# Creates fifo file if it does not exist
create_fifo_if_not_exists() {
    [[ -p "$1" ]] || mkfifo "$1"
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

  "$PYTHON_EXEC_PATH" "$SCRIPT_PATH" "$INPUT" > "$PIPES_PATH""/""$INPUT"".pipe"

  # shellcheck source=/dev/null
  # source "$HOST_COMMANDS_DIRECTORY""/""$INPUT"".sh" > "$PIPES_PATH""/""$INPUT"".pipe"
}

# create_pipes_from_script_names
create_fifo_if_not_exists "$INCOMING_COMMANDS_PIPE_PATH"
create_fifo_if_not_exists status

while true
do
  check_incoming_pipe
done
