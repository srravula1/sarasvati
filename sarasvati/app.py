from logging import CRITICAL, DEBUG, basicConfig, getLogger

from sarasvati.api import Sarasvati
from sarasvati.plugins import CommandInfo

basicConfig(level=DEBUG)
getLogger("urllib3.connectionpool").setLevel(CRITICAL)
getLogger("yapsy").setLevel(CRITICAL)

def run():
    print("Sarasvati")
    api = Sarasvati()

    # register all the commands
    command_line = api.plugins.get(category="CommandLine")
    if command_line:
        for commands_plugin in api.plugins.find(category="Commands"):
            commands = commands_plugin.get_commands()
            for command in commands:
                if not isinstance(command, CommandInfo):
                    raise Exception("Command registration info should be an instance of the CommandInfo class.")
                command_line.register(command[0], command[1])

    app = api.plugins.get(category="Application")
    app.activate()

if __name__ == "__main__":
    run()
