# encoding: utf-8
""" Stuff that doesn't fit in anywhere particular. """
from __future__ import print_function
import os
import sys

default_lexer_name = 'markdown'


def _get_highlighter(filename, lexer_name):
    u""" Get highlighter.

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
    no_highlight = lambda text: text

    lexer = None

    # Import the highlight tools
    try:
        from pygments import highlight
        from pygments.formatters import TerminalFormatter
        from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
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

    return lambda text: highlight(text, lexer, TerminalFormatter())


def colorize(sheet_content, filename=''):
    """ Colorizes cheatsheet content if so configured """
    do_colorize = os.environ.get('CHEATCOLORS', False)

    if not do_colorize:
        return sheet_content

    highlight = _get_highlighter(filename, do_colorize)
    return highlight(sheet_content)


def die(message):
    """ Prints a message to stderr and then terminates """
    stderr_warn(message)
    exit(1)


def edit(filename):
    u""" Launch editor with file. """
    import subprocess

    editor = os.environ.get('EDITOR')
    if not editor:
        raise Exception(
            u"Could not edit %r: No EDITOR environment variable set" %
            filename)

    try:
        subprocess.call([editor, filename])
    except OSError, e:
        raise Exception(
            u"Could not edit %r (editor: %r): %s" %
            (filename, editor, e))


def prompt_yes_or_no(question):
    """ Prompts the user with a yes-or-no question """
    # Support Python 2 and 3 input
    # Default to Python 2's input()
    get_input = raw_input

    # If this is Python 3, use input()
    if sys.version_info[:2] >= (3, 0):
        get_input = input

    print(question)
    return get_input('[y/n] ') == 'y'


def stderr_warn(message):
    """ Prints a message to stderr """
    print((message), file=sys.stderr)
