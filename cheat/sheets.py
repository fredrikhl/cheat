# encoding: utf-8
""" Module for looking up and fetching cheat sheets. """
import os
import sys


class _SheetLookup(object):

    u""" Class to deal with cheat sheet paths. """

    install_dir = os.path.join(sys.prefix, 'share', 'cheatsheets')
    u""" Where cheat sheets gets installed to. """

    @property
    def write_dir(self):
        """ Get a writable path for new cheat sheets.

        :return str,None:
            Returns the first writable path in paths(), or None if no writable
            path is found.
        """
        for p in reversed(self.sheet_paths):
            if p == self.install_dir:
                continue
            if os.access(p, os.W_OK):
                return p
        return None

    @property
    def cheat_sheets(self):
        u""" A mapping of cheat sheet names to filename. """
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
        u""" A list of search paths that exists and are readable.

        The list is ordered so that the last item is the first that should be
        considered when looking for cheat sheets. It contains the following
        directories, if they exist and are readable:

          1. <install prefix>/share/cheatsheets/
          2. env[DEFAULT_CHEAT_DIR]
          3. ~/.cheat/
          4. env[CHEATPATH] (colon-separated list)

        :return list:
            A list of readable paths that may contain cheat sheets.

        """
        if not hasattr(self, '__cheat_paths'):
            self.__cheat_paths = filter(
                lambda p: (p and os.path.isdir(p)
                           and os.access(p, os.R_OK | os.X_OK)),
                [self.install_dir,
                 os.environ.get('DEFAULT_CHEAT_DIR', None),
                 os.path.join(os.path.expanduser('~'), '.cheat'),
                 ] + os.environ.get('CHEATPATH', '').split(os.pathsep))
        return self.__cheat_paths

    def exists(self, name):
        u""" Check if the cheat sheet exists. """
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
        u""" Return the path of the named cheat sheet.

        :param str name: The name of a cheat sheet.

        :return str,None:
            Returns the cheat sheet path, or None if the named cheat sheet
            doesn't exist.
        """
        return self.cheat_sheets.get(name, None)

    def search(self, term):
        u""" Search all cheatsheets for a term.

        :param str term: The term to search for.

        :return dict:
            A dict that contains matches. Each match is a mapping from the name
            of a cheat sheet to a list of lines that contains the match.

        """
        for name in sorted(self.cheat_sheets.keys()):
            matches = []
            for line in open(self.cheat_sheets[name], 'r'):
                if term in line:
                    matches.append(line.strip())
            if matches:
                yield name, matches


Sheets = _SheetLookup()
