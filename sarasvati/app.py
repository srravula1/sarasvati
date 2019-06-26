from yaml import safe_load as yaml_load
from sarasvati.core.plugins import PluginsRepository

def run():
    print("Run sarasvati")
    
    # reading configuraion files
    with open("config.yml", "r") as ymlfile:
        cfg = yaml_load(ymlfile)

    # init plugins repository
    plugins_path = cfg["plugins"]["path"]
    repositories_url = cfg["plugins"]["repositories"]
    r = PluginsRepository(
        path=plugins_path,
        urls=repositories_url)
    
    r.update()
    r.install("hello-world")

if __name__ == "__main__":
    run()
