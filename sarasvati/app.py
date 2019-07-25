from logging import CRITICAL, DEBUG, basicConfig, getLogger
from .api.api import Sarasvati


basicConfig(level=DEBUG)
getLogger("urllib3.connectionpool").setLevel(CRITICAL)
getLogger("yapsy").setLevel(CRITICAL)

def run():
    print("Run sarasvati")

    api = Sarasvati()
    app = api.plugins.get(category="Application")

    for c in api.plugins.find(category="Commands"):
        c.activate()

    app.activate()

if __name__ == "__main__":
    run()
