import inspect

import pystatikman.config.defaultconfig

config_list = inspect.getmembers(defaultconfig, inspect.isclass)
definedconfigs = dict(config_list)