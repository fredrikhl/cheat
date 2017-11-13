# encoding: utf-8
""" The cheatsheet package. """
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution('cheat').version
except DistributionNotFound:
    __version__ = None
