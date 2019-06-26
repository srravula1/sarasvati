from yaml import safe_load as yaml_load
from sarasvati.core.repository import PackagesRepository
from logging import getLogger, basicConfig, DEBUG, CRITICAL

basicConfig(level=DEBUG)
getLogger("urllib3.connectionpool").setLevel(CRITICAL)

def run():
    print("Run sarasvati")
    
    # reading configuraion files
    with open("config.yml", "r") as ymlfile:
        cfg = yaml_load(ymlfile)

    # init packages repository
    packages_path = cfg["packages"]["path"]
    repositories_url = cfg["packages"]["repositories"]
    r = PackagesRepository(
        path=packages_path,
        urls=repositories_url)
    
    r.update()
    r.fetch("hello-world")

if __name__ == "__main__":
    run()
