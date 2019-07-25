from yapsy.FilteredPluginManager import FilteredPluginManager
from yapsy.PluginManager import PluginManager as YapsyPluginManager


class PluginsManager:
    __EXTENSION = "plugin"
    __CORE_PLUGINS_PATH = "packages"

    def __init__(self, path: str = "plugins", categories: dict = None, api: object = None):
        self.__paths = [self.__CORE_PLUGINS_PATH, path]
        self.__categories = categories or {}
        self.__api = api
        
        # Configure plugin manager
        self.__manager = FilteredPluginManager(YapsyPluginManager())
        self.__manager.getPluginLocator().setPluginInfoExtension(self.__EXTENSION)
        self.__manager.setPluginPlaces(self.__paths)
        self.__manager.setCategoriesFilter(self.__categories)

        # Collect plugins
        self.__collect_plugins()

    @property
    def all(self):
        result = []
        sorted_plugins = sorted(self.__manager.getAllPlugins(), key=lambda x: x.name)
        for plugin in sorted_plugins:
            result.append(self.__convert(plugin))
        return result

    def update(self):
        before = list(self.all)
        self.__collect_plugins()
        after = list(self.all)
        diff = set(after) - set(before)

        return list(diff)

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

    def __collect_plugins(self):
        self.__manager.collectPlugins()

#        for plugin in self.__manager.getAllPlugins():
#            self.__log.debug("Plugin: %s (v%s) by %s", plugin.name, plugin.version, plugin.author)

    def __convert(self, obj):
        obj.plugin_object.info = PluginInfo(obj.name, obj.version, obj.path, obj.author, obj.is_activated)
        obj.plugin_object._api = self.__api
        return obj.plugin_object


class PluginInfo:
    def __init__(self, name, version, path, author, is_activated, description=None):
        self.name = name
        self.version = version
        self.description = description
        self.path = path
        self.author = author
        self.is_activated = is_activated
