# Host Container API

Run commands in the host machine from a Docker container.

This is a python script running on the host machine that is listening to a named pipe,
runs prepared commands and sends the response to another pipe. 

Intended to be used in home servers requiring host data.

![Sequence diagram](resources/diagram.png "Sequence diagram")

Do not install anywhere near production.

Tested on Debian. May run on MacOS.

# Installation

```shell
git clone <repo>
cd <repo>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To run the program, execute
```shell
cd <repo>
source venv/bin/activate
python listen.py
```

*TODO: add a script to ensure constant execution*

# Data format

For **incoming requests**, all Docker containers should write to the same named pipe
configured in `config.yaml` following this format:

```txt
<pipe-name>:<command-name>
```

pipe-name
: Where the response should be sent. Can be a fixed or random value.

command-name
: Indicates which **command** should run. A command (in this context)
is a class extending `AbstractCommand` that has a `name`
property that has to be used to execute said class.

---

All **responses** to requests are written to the same directory configured in
`config.yaml`, using the `pipe-name` received in the request as the pipe name.
The content will always be a JSON-formatted string with this format:

```json
{
  "success": bool,
  "message": string,
  "data": object
}
```

success
: true or false

message
: empty if `success` is true, otherwise will contain some description

data
: the command output

# How to add custom commands
The `commands` folder is git-ignored, so custom commands can be added without
losing the ability to upgrade.

1. Create a python class inside the `commands` folder
2. Extend the `AbstractCommand` class
3. Implement the abstract method and property required
4. Optionally, run `python list-commands.py` to see if the command is listed
5. Try the command using a pipe name and the `name` property 

Example 

`/commands/ExampleCommand.py`
```python
from lib.AbstractCommand import AbstractCommand

class ExampleCommand(AbstractCommand):
    name = "example-command"

    def run(self):
        return "this is the response"
```

Then run the `listen.py` file in one terminal, and in another run: 
```shell
echo "my-custom-pipe:example-command" > pipes/in.pipe
cat "my-custom-pipe"
```

It will display:
```json
{
  "success": true,
  "message": "",
  "data": "this is the response"
}
```
