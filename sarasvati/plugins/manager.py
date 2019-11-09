from yapsy.FilteredPluginManager import FilteredPluginManager
from yapsy.PluginManager import PluginManager as YapsyPluginManager

from sarasvati.core.event import Event


class PluginsManager:
    __EXTENSION = "plugin"
    __CORE_PLUGINS_PATH = "packages"

    def __init__(self, path: str = "plugins", categories: dict = None, api: "Sarasvati" = None):
        """
        Initializes new instance of the PluginsManager class.
        """
        self.__api = api
        self.__paths = [self.__CORE_PLUGINS_PATH, path]
        self.__categories = categories or {}
        self.__disabled = []
        self.__plugin_enable_flag_changed = Event()

        # Configure plugin manager
        self.__manager = FilteredPluginManager(YapsyPluginManager())
        self.__manager.getPluginLocator().setPluginInfoExtension(self.__EXTENSION)
        self.__manager.setPluginPlaces(self.__paths)
        self.__manager.setCategoriesFilter(self.__categories)
        self.__manager.isPluginOk = lambda x: x.name not in self.__disabled

    @property
    def plugin_enable_flag_changed(self):
        return self.__plugin_enable_flag_changed

    @property
    def all(self):
        result = []
        all_plugins = self.__manager.getAllPlugins()
        sorted_plugins = sorted(all_plugins, key=lambda x: x.name)
        for plugin in sorted_plugins:
            result.append(self.__convert(plugin))
        return result

    def disable_plugin(self, name: str):
        self.__disabled.append(name)
        self.__plugin_enable_flag_changed.notify(name, False)

    def enable_plugin(self, name: str):
        if name in self.__disabled:
            self.__disabled.remove(name)
            self.__plugin_enable_flag_changed.notify(name, True)

    def update(self):
        self.__manager.collectPlugins()

    def find(self, **kwargs):
        result = []
        for plugin in self.__manager.getPluginsOf(**kwargs):
            result.append(self.__convert(plugin))
        return result

    def get(self, **kwargs):
        plugins = self.find(**kwargs)
        count = len(plugins)
        if count == 1:
            return plugins[0]
        elif count == 0:
            raise Exception("No plugin found")
        elif count > 1:
            raise Exception("More than one plugin found")

    def __convert(self, obj):
        obj.plugin_object.info = PluginInfo(
            obj.name, obj.version, obj.path, obj.author, obj.is_activated)
        obj.plugin_object._api = self.__api
        obj.plugin_object._config = self.__api.config.plugins.get(obj.name)
        return obj.plugin_object


class PluginInfo:
    def __init__(self, name, version, path, author, is_activated, description=None):
        self.name = name
        self.version = version
        self.description = description
        self.path = path
        self.author = author
        self.is_activated = is_activated
