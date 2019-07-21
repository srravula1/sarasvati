from typing import List

from sarasvati.packages import PackageId, PackagesException
from sarasvati.packages.fetcher import PackageFetcher
from sarasvati.packages.repository import Repository


class PackagesManager:
    def __init__(self, urls: List[str], path: str):
        self.__repositories = list(map(lambda x: Repository(x), urls))
        self.__fetcher = PackageFetcher(path)

    def update(self):
        for repository in self.__repositories:
            repository.update()

    def add(self, packageId: PackageId):
        candidates = list(map(
            lambda r: r.find_package(packageId),
            self.__repositories))

        if len(candidates) > 1:
            raise PackagesException("Too many candidates to install")

        self.__fetcher.fetch(candidates[0])

    def remove(self, packageId: PackageId):
        pass

    def find(self, packageId: PackageId):
        pass
