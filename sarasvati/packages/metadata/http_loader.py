from logging import getLogger
from typing import List

from requests import get as requests_get

from sarasvati.packages import PackagesException
from sarasvati.packages.metadata.metadata import IMetadataLoader


class HttpMetadataLoader(IMetadataLoader):
    def __init__(self, url: str):
        self.__url = url
        self.__log = getLogger("packages")

    def load(self) -> str:
        self.__log.info("Fetching repository %s", self.__url)
        return self.__fetch_metadata(self.__url)

    @staticmethod
    def __fetch_metadata(url: str):
        response = None
        try:
            response = requests_get(url)
        except:
            raise PackagesException("Unable to load repository metadata")
        
        if not response.ok:
            raise PackagesException(f"Unable to fetch repository: {response.status_code} {response.reason}")
        
        return response.text
