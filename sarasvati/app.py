from logging import CRITICAL, DEBUG, basicConfig, getLogger

from sarasvati.api import Sarasvati

basicConfig(level=DEBUG)
getLogger("urllib3.connectionpool").setLevel(CRITICAL)
getLogger("yapsy").setLevel(CRITICAL)

def run():
    print("Run sarasvati")
    api = Sarasvati()

    # register all the commands
    command_line = api.plugins.get(category="CommandLine")
    if command_line:
        for commands_plugin in api.plugins.find(category="Commands"):
            commands = commands_plugin.get_commands()
            for command in commands:
                command_line.register(command[0], command[1])

    app = api.plugins.get(category="Application")
    app.activate()

if __name__ == "__main__":
    run()
