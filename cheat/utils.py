# encoding: utf-8
""" Stuff that doesn't fit in anywhere particular. """
from __future__ import unicode_literals, print_function

import os

default_lexer_name = 'markdown'
default_style_name = 'default'


def _get_highlighter(filename, lexer_name, style=None):
    """ Get highlighter.

    Creates a highlighter for, if available. The highlighter will use the first
    available lexer from:
      1. filename
      2. lexer_name
      3. default_lexer_name

    :param string filename: A filename to fetch highlighter for.
    :param string name: A fallback lexer name to use for highlighting.

    :return callable:
        A function that takes one parameter, the string to highlight.

    """
    # A function that just returns the text unmodified, if we're unable to do
    # highlighting:
    def no_highlight(text):
        return text

    # Import the highlight tools
    try:
        from pygments import highlight
        from pygments.formatters import (TerminalFormatter,
                                         Terminal256Formatter,
                                         TerminalTrueColorFormatter)
        from pygments.formatters.other import RawTokenFormatter
        from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
        from pygments.styles import get_style_by_name
    except ImportError:
        return no_highlight

    # Find available lexer object
    for method, value in ((get_lexer_for_filename, str(filename)),
                          (get_lexer_by_name, str(lexer_name)),
                          (get_lexer_by_name, default_lexer_name)):
        try:
            lexer = method(value)
            break
        except:
            # probably pygments.util.ClassNotFound
            continue

    if lexer is None:
        return no_highlight

    formatter = TerminalFormatter()

    if style:
        try:
            style = get_style_by_name(style)
        except:
            # Probably no such style
            style = get_style_by_name(default_style_name)
        formatter = TerminalTrueColorFormatter(style=style)

#   return lambda text: (
#       highlight(text, lexer, RawFormatter()) +
#       highlight(text, lexer, formatter))
    return lambda text: highlight(text, lexer, formatter)


def colorize(sheet_content, filename=''):
    """ Colorizes cheatsheet content if so configured """
    do_colorize = os.environ.get('CHEATCOLORS', False)
    style = os.environ.get('CHEATSTYLE', None)

    if not do_colorize:
        return sheet_content

    highlight = _get_highlighter(filename, do_colorize, style=style)
    return highlight(sheet_content)


def edit(filename):
    """ Launch editor with file. """
    import subprocess

    editor = os.environ.get('EDITOR')
    if not editor:
        raise Exception(
            "Could not edit %r: No EDITOR environment variable set" %
            filename)

    try:
        subprocess.call([editor, filename])
    except OSError, e:
        raise Exception(
            "Could not edit %r (editor: %r): %s" %
            (filename, editor, e))
