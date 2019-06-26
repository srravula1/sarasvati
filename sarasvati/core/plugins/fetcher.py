from os.path import join
from tempfile import NamedTemporaryFile
from zipfile import BadZipFile, LargeZipFile, ZipFile, is_zipfile

from requests import HTTPError
from requests import get as requests_get

from .exception import PluginsException
from .meta import PluginMeta


class PluginFetcher():
    """Fetches and extracts plugin using specified url."""

    def __init__(self, path: str):
        """
        Initializes new instance of the PluginFetcher class.
        
        Arguments:
            path {str} -- Path to extract plugins.
        """
        self.__path = path

    def fetch(self, meta: PluginMeta):
        with requests_get(meta.url, stream=True) as stream, NamedTemporaryFile() as file:
            self.__download(stream, file)
            self.__extract(file.name, join(self.__path, meta.key))

    @staticmethod
    def __download(stream, file):
        try:
            stream.raise_for_status()
            for chunk in stream.iter_content(chunk_size=8192): 
                file.write(chunk)
            file.flush()
        except HTTPError as ex:
            msg = ex.args[0]
            raise PluginsException(f"Unable to download file. {msg}")

    @staticmethod
    def __extract(path: str, extract_to: str):
        # check zip file
        if not is_zipfile(path):
            raise PluginsException("Not a zip file.")

        # extract zip file
        try:
            with ZipFile(path, "r") as zip:
                zip.extractall(extract_to)
        except FileNotFoundError as ex:
            raise PluginsException("Unable to extract plugin file. File not found.")
        except BadZipFile as ex:
            raise PluginsException("Unable to extract plugin file. Bad zip file.")
        except LargeZipFile as ex:
            raise PluginsException("Unable to extract plugin file. Zip file is too large.")
