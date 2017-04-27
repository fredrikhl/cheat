# encoding: utf-8
""" The cheatsheet package. """

def get_version():
    import pkg_resources as _pkg
    return _pkg.get_distribution("cheat").parsed_version._version


version = get_version()
