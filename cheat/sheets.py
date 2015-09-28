# encoding: utf-8
""" Module for looking up and fetching cheat sheets. """
from cheat.utils import die
import os
import sys


def get():
    """ Assembles a dictionary of cheatsheets as name => file-path """
    cheats = {}

    # otherwise, scan the filesystem
    for cheat_dir in paths():
        cheats.update(
            dict([
                (cheat, os.path.join(cheat_dir, cheat))
                for cheat in os.listdir(cheat_dir)
                if not cheat.startswith('.')
            ])
        )

    return cheats


def paths():
    """ Assembles a list of directories containing cheatsheets.

    Lookup order:

      1. <install prefix>/share/cheatsheets/
      2. env[DEFAULT_CHEAT_DIR]
      3. ~/.cheat/
      4. env[CHEATPATH] (colon-separated list)

    :return list:
        A list of existing paths that may contain cheat sheets.

    """
    sheet_paths = filter(
        lambda p: p and os.path.isdir(p),
        [os.path.join(sys.prefix, 'share', 'cheatsheets'),
         os.environ.get('DEFAULT_CHEAT_DIR', None),
         os.path.join(os.path.expanduser('~'), '.cheat'),
         ] + os.environ.get('CHEATPATH', '').split(os.pathsep))

    if not sheet_paths:
        die('The DEFAULT_CHEAT_DIR dir does not exist or the CHEATPATH is not set.')

    return sheet_paths


def list():
    """ Lists the available cheatsheets """
    sheet_list = ''
    pad_length = max([len(x) for x in get().keys()]) + 4
    for sheet in sorted(get().items()):
        sheet_list += sheet[0].ljust(pad_length) + sheet[1] + "\n"
    return sheet_list


def search(term):
    """ Searches all cheatsheets for the specified term """
    result = ''

    for cheatsheet in sorted(get().items()):
        match = ''
        for line in open(cheatsheet[1]):
            if term in line:
                match += '  ' + line

        if not match == '':
            result += cheatsheet[0] + ":\n" + match + "\n"

    return result
