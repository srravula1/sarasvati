from logging import getLogger

from requests import get as requests_get

from sarasvati.packages import PackagesException
from sarasvati.packages.metadata.metadata import IMetadataLoader


class HttpMetadataLoader(IMetadataLoader):
    def __init__(self):
        self.__log = getLogger("packages")

    def load(self, url: str) -> str:
        self.__log.info("Fetching repository %s", url)
        return self.__fetch_metadata(url)

    @staticmethod
    def __fetch_metadata(url: str):
        response = None
        try:
            response = requests_get(url)
        except:
            raise PackagesException("Unable to load repository metadata")

        if not response.ok:
            raise PackagesException(
                f"Unable to fetch repository: {response.status_code} {response.reason}")

        return response.text
