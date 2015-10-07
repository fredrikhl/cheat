cheat
=====
`cheat` allows you to create and view interactive cheatsheets on the
command-line. It was designed to help remind \*nix system administrators of
options for commands that they use frequently, but not frequently enough to
remember.

`cheat` depends only on `python` and `pip`.

Original
--------
This version is a fork from
[chrisallenlane/cheat](https://github.com/chrisallenlane/cheat).

The fork was originally intended to change the output coloring to highlight
markdown, but ended up as a major rewrite for no good reason.

The last version from [chrisallenlane](https://github.com/chrisallenlane/) can
be fetched from PyPI:
[![Latest Version](https://pypip.in/version/cheat/badge.png)](https://pypi.python.org/pypi/cheat/)

Installing
----------

    pip install git+https://github.com/fredrikhl/cheat.git#egg=cheat

Usage
-----

    usage: cheat [-h] [-l] [-d] [-v] [-e CHEATSHEET | -s KEYWORD | CHEATSHEET]

    positional arguments:
      CHEATSHEET            Show the cheat sheet named 'CHEATSHEET'.

    optional arguments:
      -h, --help            show this help message and exit
      -l, --list            List existing cheat sheets and exit.
      -d, --directories     List cheat sheet directories and exit.
      -v, --version         Print version and exit.
      -e CHEATSHEET, --edit CHEATSHEET
                            Edit a cheat sheet CHEATSHEET.
      -s KEYWORD, --search KEYWORD
                            Search cheat sheets for KEYWORD.

Configure
---------
The following environment variables affect how `cheat` works:

CHEATCOLORS
~~~~~~~~~~~
Setting the `CHEATCOLORS` environment variable enables syntax highlighting of cheat sheets.

If a cheat sheet has a file extension, that extension will be used to select
langauge for syntax highlighting.

If no syntax highlighter can be found for the cheat sheet (e.g. no file
extension), the default syntax highlighter will be used. If `CHEATCOLORS` is
set to a valid language, that language will be used as default.

Example:

    # Use 'bash' syntax highlighting
    export CHEATCOLORS="bash"

    # Enable syntax highlighting without specifying a default language (will
    # assume 'markdown')
    export CHEATCOLORS=1


DEFAULT\_CHEAT\_DIR
~~~~~~~~~~~~~~~~~~~
Override the default location for installed cheat sheets.

If this environment variable is set to a non-existing location, the default
cheat sheets will be disabled. Otherwise, this environment variable can be used
to set the location of the cheat sheets if some alternate install has been
done.

Example:

    # Disable default cheat sheets
    export DEFAULT_CHEAT_DIR=""

    # Change location fo default cheat sheets
    export DEFAULT_CHEAT_DIR="/path/to/my/cheatsheets"

CHEATPATH
~~~~~~~~~
Extra locations for cheat sheets.

Multiple colon-separated paths can be given.

Cheat sheets found on the `CHEATPATH` will override cheat sheets found in
`~/.cheat` and the default cheat sheets (`DEFAULT_CHEAT_DIR`).

Example:

    # Add two cheat paths
    export CHEATPATH="/my/first/set:/my/second/set"

    # Note: /my/second/set will override /my/first/set in the example. If
    # both directories have a cheat sheet for `foo`, the version found in
    # /my/second/set is used by cheat.

EDITOR
~~~~~~
`cheat` depends on an editor being set in your shell when editing cheat sheets.

Example:

    export EDITOR=vim


Editing cheat sheets
--------------------
If the cheat sheet that is being edited exists only in the default cheat dir,
or if you don't have write access to the cheat sheet, a copy will be made in
the first writeable search path for `cheat`.
