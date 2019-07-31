from sarasvati.brain.brain import Brain


class BrainManager:
    """Manager of a brains."""

    def __init__(self, api):
        """Initializes new instance of the BrainManager class.
        
        Arguments:
            api {Sarasvati} -- Api
        """
        self.__api = api
        self.__active = None

    def open(self, path: str) -> Brain:
        """Opens new brain at specified path.
        
        Arguments:
            path {str} -- Path to the brain.
        
        Returns:
            Brain -- Brain.
        """
        self.__active = Brain(self.__api, path)
        return self.__active

    @property
    def active(self) -> Brain:
        """
        Returns active brain.
        
        Returns:
            Brain -- Brain.
        """
        return self.__active
