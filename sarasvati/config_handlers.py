from sarasvati.api import Sarasvati
from sarasvati.config import ConfigManager


def subscribe_config_changes(api: Sarasvati):
    api.plugins.plugin_enable_flag_changed.subscribe(
        lambda name, enabled: _on_plugin_enable_flag_changed(name, enabled, api.config))


def _on_plugin_enable_flag_changed(name: str, enabled: bool, config: ConfigManager):
    # check plugins/disabled key is present
    if not config.plugins.disabled:
        config.plugins.disabled = []
    
    # update list
    if enabled:
        config.plugins.disabled.remove(name)
    else:
        config.plugins.disabled.append(name)

    config.save()
