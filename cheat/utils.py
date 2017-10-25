# encoding: utf-8
""" Stuff that doesn't fit in anywhere particular. """
from __future__ import unicode_literals, print_function

import os
from collections import OrderedDict

try:
    from pygments import highlight
    from pygments.filters import get_filter_by_name
    from pygments.formatters import (TerminalFormatter,
                                     Terminal256Formatter)
    # from pygments.formatters.other import TerminalTrueColorFormatter
    # from pygments.formatters.other import RawTokenFormatter
    from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
    from pygments.styles import get_style_by_name

    COLORS = True
except ImportError:
    COLORS = False


default_lexer_name = 'markdown'
default_style_name = 'default'


def no_highlight(text):
    """ Return text unmodified. """
    return text


def parse_filters_setting(filters_setting):
    """ Parse a filter map string.

    :param str filters_setting:
        Serialized map of filters to use for given lexers. Format:
        "<lexer_name>=<filter_name>:..."

    :return OrderedDict:
        Returns an unserialized mapping of the filters_setting.
    """
    filters = OrderedDict()
    for filter_setting in (filters_setting or '').split(os.pathsep):
        lexer_name, _, filter_name = filter_setting.partition('=')
        filter_list = filters.setdefault(lexer_name, list())
        if filter_name not in filter_list:
            filter_list.append(filter_name)
    return filters


def parse_styles_setting(styles_setting):
    """ Parse a styles list string.

    :param str styles_setting:
        Serialized list of styles to use, ordered by preference.
        Format: "<style_name>:..."

    :return list:
        Returns a list of style names.
    """
    seen = set()
    seen_add = seen.add
    return [style_name for style_name in styles_setting.split(os.pathsep)
            if not (style_name in seen or seen_add(style_name))]


def _get_highlighter(filename, lexer_name=None, styles=None, filters=None):
    """ Get highlighter.

    Creates a highlighter for, if available. The highlighter will use the first
    available lexer from:
      1. filename
      2. lexer_name
      3. default_lexer_name

    :param string filename: A filename to fetch highlighter for.
    :param string name: A fallback lexer name to use for highlighting.
    :param list styles: A list of preferred styles, in order
    :param dict filters: A mapping from lexer names to a list of filters

    :return callable:
        A function that takes one parameter, the string to highlight.

    """
    # Import the highlight tools
    if not COLORS:
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
            lexer = None

    if lexer is None:
        return no_highlight

    formatter = TerminalFormatter()

    for style in (styles or []):
        try:
            formatter = Terminal256Formatter(style=get_style_by_name(style))
            break
        except:
            continue

    for filter_name in filters.get(lexer.name, list()):
        try:
            lexer.add_filter(get_filter_by_name(filter_name))
        except:
            pass

    return lambda text: highlight(text, lexer, formatter)


def colorize(sheet_content, filename=''):
    """ Colorizes cheatsheet content if so configured """
    do_colorize = os.environ.get('CHEATCOLORS', False)
    styles = os.environ.get('CHEATSTYLE', None)
    filters = os.environ.get('CHEATFILTERS', None)

    if not do_colorize:
        return sheet_content

    highlight = _get_highlighter(filename,
                                 lexer_name=do_colorize,
                                 styles=parse_styles_setting(styles),
                                 filters=parse_filters_setting(filters))
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
