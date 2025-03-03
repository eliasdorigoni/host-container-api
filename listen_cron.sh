#!/bin/bash
#make sure a process is always running.

THIS_DIR=$( cd -- "$( /usr/bin/dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && /usr/bin/pwd )

if pgrep -f "host-container-api" > /dev/null; then
  exit
else
  source "$THIS_DIR""/venv/bin/activate"
  python "$THIS_DIR" listen > /dev/null 2>&1 &
fi
