from logging import CRITICAL, DEBUG, basicConfig, getLogger

from yaml import safe_load as yaml_load

from sarasvati.packages import PackagesManager

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
    # r = Repository(repositories_url[0])
    # r.update()
    # package = r.get_package("hello-world")

    # f = PackageFetcher(packages_path)
    # f.fetch(package)

    # manager
    m = PackagesManager(repositories_url, packages_path)
    m.update()
    m.add("hello-world")
    m.remove("")
    # m.find("")

    # r.fetch("hello-world")

if __name__ == "__main__":
    run()
