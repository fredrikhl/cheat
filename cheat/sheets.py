# encoding: utf-8
""" Module for looking up and fetching cheat sheets. """

from __future__ import unicode_literals, print_function

import os
import sys


def is_readable_dir(path):
    """ Return True if directory is readable. """
    return (bool(path) and os.path.isdir(path)
            and os.access(path, os.R_OK | os.X_OK))


class _SheetLookup(object):

    """ Class to deal with cheat sheet paths. """

    install_dir = os.path.join(sys.prefix, 'share', 'cheatsheets')
    """ Where cheat sheets gets installed to. """

    source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                              'cheatsheets')
    """ Location of cheat sheets in source dir. """

    @property
    def default_cheat_sheets(self):
        """ The default cheat sheets.

        Return the first existing, readable folder of:

          1. env[DEFAULT_CHEAT_DIR]
          2. install_dir
          3. source_dir

        :return str,None: Default cheatsheets path, if any.

        """
        for path in (os.environ.get('DEFAULT_CHEAT_DIR'),
                     self.install_dir,
                     self.source_dir):
            if is_readable_dir(path):
                return path
        return None

    @property
    def write_dir(self):
        """ Get a writable path for new cheat sheets.

        :return str,None:
            Returns the first writable path in paths(), or None if no writable
            path is found.
        """
        for p in reversed(self.sheet_paths):
            if p in (self.install_dir, self.source_dir):
                continue
            if os.access(p, os.W_OK):
                return p
        return None

    @property
    def cheat_sheets(self):
        """ A mapping of cheat sheet names to filename. """
        if not hasattr(self, '_cheat_sheets'):
            self._cheat_sheets = dict()

            for cheat_dir in self.sheet_paths:
                self._cheat_sheets.update(
                    dict(((os.path.splitext(cheat)[0],
                           os.path.join(cheat_dir, cheat))
                          for cheat in os.listdir(cheat_dir)
                          if not cheat.startswith('.'))))
        return self._cheat_sheets

    @property
    def sheet_paths(self):
        """ A list of search paths that exists and are readable.

        The list is ordered so that the last item is the first that should be
        considered when looking for cheat sheets. It contains the following
        directories, if they exist and are readable:

          1. default_cheat_sheets
          3. ~/.cheat/
          4. env[CHEATPATH] (colon-separated list)

        :return list:
            A list of readable paths that may contain cheat sheets.

        """
        if not hasattr(self, '_cheat_paths'):
            self._cheat_paths = filter(
                is_readable_dir,
                [self.default_cheat_sheets,
                 os.path.join(os.path.expanduser('~'), '.cheat'),
                 ] + os.environ.get('CHEATPATH', '').split(os.pathsep))
        return self._cheat_paths

    def exists(self, name):
        """ Check if the cheat sheet exists. """
        filename = self.get(name)
        if filename is None:
            return False
        return os.access(filename, os.R_OK)

    def is_writable(self, name):
        filename = self.get(name)
        if filename is None:
            return False
        if filename.startswith(self.install_dir):
            return False
        return os.access(filename, os.W_OK)

    def get(self, name):
        """ Return the path of the named cheat sheet.

        :param str name: The name of a cheat sheet.

        :return str,None:
            Returns the cheat sheet path, or None if the named cheat sheet
            doesn't exist.
        """
        return self.cheat_sheets.get(name, None)

    def search(self, term):
        """ Search all cheatsheets for a term.

        :param str term: The term to search for.

        :return dict:
            A dict that contains matches. Each match is a mapping from the name
            of a cheat sheet to a list of lines that contains the match.

        """
        for name in sorted(self.cheat_sheets.keys()):
            matches = []
            for line in open(self.cheat_sheets[name], 'r'):
                line = line.decode('utf-8', 'replace')
                if term in line:
                    matches.append(line.strip())
            if matches:
                yield name, matches


# TODO: Should probably replace sys.modules[name] with this:
#     sys.modules[__name__] = _SheetLookup()
Sheets = _SheetLookup()
