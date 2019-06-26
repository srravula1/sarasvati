from yaml import safe_load as yaml_load
from sarasvati.core.repository import PackagesRepository

def run():
    print("Run sarasvati")
    
    # reading configuraion files
    with open("config.yml", "r") as ymlfile:
        cfg = yaml_load(ymlfile)

    # init packages repository
    packages_path = cfg["plugins"]["path"]
    repositories_url = cfg["plugins"]["repositories"]
    r = PackagesRepository(
        path=packages_path,
        urls=repositories_url)
    
    r.update()
    r.fetch("hello-world")

if __name__ == "__main__":
    run()
