import pytest

import os
import imp
import inspect

from base_algorithm import Algorithm


def load_plugins(plugin_folder):
    plugins = {}
    cwd = os.path.abspath(os.path.curdir)
    plugin_folder = os.path.join(cwd, plugin_folder)
    folders = [x for x in os.listdir(plugin_folder)
               if os.path.isdir(os.path.join(plugin_folder, x))]
    for f in folders:
        path = os.path.join(plugin_folder, f)
        if "__init__.py" in os.listdir(path):
            module_info = imp.find_module("__init__", [path])
            plugins[f] = module_info
    return plugins


@pytest.fixture(params=load_plugins("plugins").items())
def algorithm(request):
    module_name, module_info = request.param
    module = imp.load_module("__init__", *module_info)
    is_algorithm = lambda x:\
        inspect.isclass(x)\
        and x is not Algorithm\
        and issubclass(x, Algorithm)
    module_members = inspect.getmembers(module, is_algorithm)
    assert len(module_members) == 1, "Looks like your algorithm {0} doesn't\
    contain a subclass of Algorithm.".format(module_name)
    return module_members[0][1]()
