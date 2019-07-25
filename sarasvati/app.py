from logging import CRITICAL, DEBUG, basicConfig, getLogger

from yaml import safe_load as yaml_load
from .api.api import Sarasvati


basicConfig(level=DEBUG)
getLogger("urllib3.connectionpool").setLevel(CRITICAL)
getLogger("yapsy").setLevel(CRITICAL)

def run():
    print("Run sarasvati")
    
    # reading configuraion files
    with open("config.yml", "r") as ymlfile:
        cfg = yaml_load(ymlfile)

    # init packages repository
    packages_path = cfg["packages"]["path"]
    repositories_url = cfg["packages"]["repositories"]

    api = Sarasvati()
    app = api.plugins.get(category="Application")

    for c in api.plugins.find(category="Commands"):
        print(c)
        c.activate()

    app.activate()


    # m = PackagesManager(repositories_url, packages_path)
    # m.update()
    # m.add("hello-world")

if __name__ == "__main__":
    run()
