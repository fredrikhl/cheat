from cheat.utils import *
import os
import sys


def default_path():
    """ Get the location of the default cheat sheets. """
    for p in (os.environ.get('DEFAULT_CHEAT_DIR', ''),
              os.path.join(sys.prefix, 'share', 'cheatsheets')):
        if os.path.isdir(p):
            return [p, ]
    return list()


def user_path():
    """ Get the location of the users cheat sheets. """
    for p in (os.path.join(os.path.expanduser('~'), '.cheat'), ):
        if os.path.isdir(p):
            return [p, ]
    return list()


def cheat_paths():
    """ Get locations of additional cheat sheets. """
    # merge the CHEATPATH paths into the sheet_paths
    paths = []
    for p in os.environ.get('CHEATPATH', '').split(os.pathsep):
        if os.path.isdir(p):
            paths.append(p)
    return paths


def get():
    """ Assembles a dictionary of cheatsheets as name => file-path """
    cheats = {}

    # otherwise, scan the filesystem
    for cheat_dir in reversed(paths()):
        cheats.update(
            dict([
                (cheat, os.path.join(cheat_dir, cheat))
                for cheat in os.listdir(cheat_dir)
                if not cheat.startswith('.')
                and not cheat.startswith('__')
            ])
        )

    return cheats


def paths():
    """ Assembles a list of directories containing cheatsheets """
    sheet_paths = []
    sheet_paths.extend(default_path())
    sheet_paths.extend(user_path())
    sheet_paths.extend(cheat_paths())

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
