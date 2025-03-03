[![Tests](https://github.com/eliasdorigoni/host-container-api/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/eliasdorigoni/host-container-api/actions/workflows/python-app.yml)

# Host Container API

Execute actions from requests received via [named pipes](https://en.wikipedia.org/wiki/Named_pipe).

This is a python script that is continually listening on a named pipe. When 
keywords are received, it runs actions (not raw commands) and sends
the response to another pipe in JSON format. 

Intended to be used in home servers requiring information like system temperature, 
free disk space, ram usage, etc, from a Docker container. Not intended to be 
used in production.

- ✅ Works on Linux. Tested on Ubuntu and MacOS.
- ❌ Does not work on Windows: named pipes require OS-specific code.


![Sequence diagram](resources/diagram.png "Sequence diagram")

# Installation

```shell
# Clone this repo and cd into it
git clone this-repo
cd this-repo

# Create a virtual environment
python3 -m venv venv

# Activate the virtual env
source venv/bin/activate

# Install required packages in virtual env
pip install -r requirements.txt

# Duplicate the config and customize to your needs
cp example.config.yaml config.yaml
```

To run the program:
```shell
source venv/bin/activate
python . listen

# Or use `python . -h` to see help
```

*TODO: add a script to ensure constant execution*

# Data format

Both **requests** and **responses** are written to `*.pipe` files inside the
directory established in `pipes_directory` in the configuration file (`config.yaml`). 

For **incoming requests**, all programs must write to the file configured in 
`input_pipe_filename` in the config file, following this format:

```txt
<pipe-name>:<action-name>
```

**pipe-name**
: Where the response should be sent. Will be created if it does not exist.

**action-name**
: Indicates which **action** should run. An action is a class extending
`AbstractCommand` that has a `name` property that can be used to be called upon.

---

All **responses** to requests are written to the file specified in the `pipe-name`
part of the request. The content will be a JSON-formatted object with 3 root items:

```text
{
  "success": bool
  "message": string
  "data": object
}
```

**success**
: true or false

**message**
: empty if `success` is true, otherwise will contain some description

**data**
: the command output

# Add custom commands
The `/custom-commands` folder is git-ignored, so classes can be added without
losing the ability to upgrade.

1. Create a python class inside the `/custom-commands` folder
2. Extend the `AbstractCommand` class
3. Implement the abstract method and property required
4. Optionally, run `python . list-actions` to see if the command is listed
5. Try the command using a pipe name and the `name` property 

Example 

`/custom-actions/Example.py`
```python
from src.models.BaseAction import BaseAction, ActionResponse


class Example(BaseAction):
    name = "example"

    def run(self) -> ActionResponse:
        return ActionResponse("this is the response")
```

Then run `python . listen-once` in a terminal, and in another run: 
```shell
echo "output.pipe:example" > pipes/input.pipe
cat pipes/output.pipe
```

It will display:
```json
{
  "success": true,
  "message": "",
  "data": "this is the response"
}
```
