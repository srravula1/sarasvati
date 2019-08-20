from io import BytesIO
from logging import getLogger
from os.path import join
from urllib.request import urlopen
from zipfile import ZipFile

from sarasvati.packages.exceptions import PackagesException
from sarasvati.packages.package import Package


class PackageFetcher:
    def __init__(self, fetch_to: str):
        self.__fetch_to = fetch_to
        self.__log = getLogger("packages")

    def fetch(self, package: Package):
        try:
            self.__log.info("Fetching package %s", package.key)
            resp = urlopen(package.url)
            zipfile = ZipFile(BytesIO(resp.read()))
            zipfile.extractall(join(self.__fetch_to, package.key))
        except Exception as ex:
           raise PackagesException(ex)
