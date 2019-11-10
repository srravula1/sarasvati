import click

from sarasvati.config.manager import ConfigManager
from sarasvati.packages.manager import PackagesManager

config = ConfigManager("config.yml")
config.open()

# Packages manager
packages = PackagesManager(
    config.packages.repositories,
    config.packages.path)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--name", prompt="Package", help="Package to install")
def install(name: str):
    """Installs specified package."""
    packages.update()
    packages.add(name)


@cli.command()
@click.option("--name", prompt="Package", help="Package to remove")
def remove(name: str):
    """Installs specified package."""
    packages.remove(name)


@cli.command()
def bootstrap():
    packages.update()
    for package in packages.packages:
        packages.add(package.key)


if __name__ == '__main__':
    cli()
