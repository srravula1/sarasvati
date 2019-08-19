from logging import CRITICAL, DEBUG, basicConfig, getLogger

from colorama import Fore, init

from sarasvati.api import Sarasvati
from sarasvati.plugins import CommandInfo

basicConfig(level=DEBUG)
getLogger("urllib3.connectionpool").setLevel(CRITICAL)
getLogger("PyQt5.uic.uiparser").setLevel(CRITICAL)
getLogger("PyQt5.uic.properties").setLevel(CRITICAL)
getLogger("yapsy").setLevel(CRITICAL)

LOGO = """
                                           __   __ 
.-----.---.-.----.---.-.-----.--.--.---.-.|  |_|__|
|__ --|  _  |   _|  _  |__ --|  |  |  _  ||   _|  |
|_____|___._|__| |___._|_____|\___/|___._||____|__|  
"""

def run():
    init(autoreset=True)
    print(Fore.GREEN + LOGO)
    
    api = Sarasvati()
    app = api.plugins.get(category="Application")
    api.before_start.notify()
    app.activate()

if __name__ == "__main__":
    run()
