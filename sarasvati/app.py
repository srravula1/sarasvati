from logging import CRITICAL, DEBUG, basicConfig, getLogger

from colorama import Fore, init

from sarasvati.api import Sarasvati

from .config_handlers import subscribe_config_changes

basicConfig(level=DEBUG)
getLogger("urllib3.connectionpool").setLevel(CRITICAL)
getLogger("PyQt5.uic.uiparser").setLevel(CRITICAL)
getLogger("PyQt5.uic.properties").setLevel(CRITICAL)
getLogger("yapsy").setLevel(CRITICAL)

# Fancy Sarasvati logo
LOGO = """
                                           __   __
.-----.---.-.----.---.-.-----.--.--.---.-.|  |_|__|
|__ --|  _  |   _|  _  |__ --|  |  |  _  ||   _|  |
|_____|___._|__| |___._|_____|\___/|___._||____|__|
"""


def run():
    """Runs Sarasvati application."""
    init(autoreset=True)
    print(Fore.GREEN + LOGO)

    try:
        api = Sarasvati()
        subscribe_config_changes(api)
        apps = api.plugins.find(category="Application")

        if not apps:
            raise Exception("No 'Application' plugin found")
        if len(apps) > 1:
            raise Exception("To many 'Application' plugins found")

        apps[0].activate()
    except Exception as ex:
        print(Fore.RED + f"Error: {ex}")


# Start as standalone application
if __name__ == "__main__":
    run()
