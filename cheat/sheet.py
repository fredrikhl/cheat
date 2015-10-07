# encoding: utf-8
""" Module for creating, editing and reading cheat sheets. """
from cheat.sheets import Sheets
import os
import shutil


class CheatSheet(object):
    u""" Cheat sheet abstraction. """

    def __init__(self, sheet_name):
        u""" Sheet object. """
        self._name = sheet_name

    @property
    def name(self):
        u""" The cheat sheet name. """
        return self._name

    @property
    def filename(self):
        u""" The filename of this cheat sheet. """
        if not getattr(self, '_filename', None):
            self._filename = Sheets.cheat_sheets.get(self.name)
        return self._filename

    @filename.setter
    def filename(self, new_filename):
        u""" Sets the filename for this cheat sheet.

        We need to update the filename of a cheat sheet when we create a new
        sheet or make a writable copy of a sheet.

        """
        self._filename = new_filename

    @property
    def exists(self):
        u""" Checks if this cheat sheet exists. """
        return Sheets.exists(self.name)

    @property
    def writable(self):
        u""" Checks if the file for this cheat sheet is writable. """
        return Sheets.is_writable(self.name)

    @property
    def contents(self):
        u""" The contents of this cheat sheet. """
        if not self.exists:
            return None
        with open(self.filename, 'r') as cheatfile:
            return cheatfile.read()

    def create(self, ext='md'):
        u""" Creates a file for this cheat sheet. """
        if self.exists:
            raise Exception("Sheet already exists")
        if Sheets.write_dir is None:
            raise Exception("No writable path configured")
        if ext:
            new_sheet = os.path.extsep.join((self.name, ext))
        else:
            new_sheet = self.name
        self.filename = os.path.join(Sheets.write_dir, new_sheet)
        touch(self.filename)

    def copy(self):
        u""" Creates a copy of this cheat sheet. """
        if not self.exists:
            raise Exception("Sheet doesn't exist")
        if Sheets.write_dir is None:
            raise Exception("No writable path configured")
        new_sheet = os.path.join(Sheets.write_dir,
                                 os.path.basename(self.filename))
        shutil.copy(self.filename, new_sheet)
        self.filename = new_sheet


def touch(filename):
    u""" Touch a file. """
    with open(filename, 'a'):
        os.utime(filename, None)


def get_editable(name):
    u""" Get the filename of an editable cheat sheet. """
    sheet = CheatSheet(name)
    try:
        if not sheet.exists:
            sheet.create()
        elif not sheet.writable:
            sheet.copy()
    except Exception, e:
        raise Exception(
            u"Could not edit %r (file: %r): %s" %
            (sheet.name, sheet.filename, e))
    return sheet.filename
