#!/usr/bin/env python
# encoding: utf-8
""" install cheat. """

from distutils.core import setup
import os


def get_requirements(filename):
    """ Read requirements from file. """
    with open(filename, 'r') as reqfile:
        for req_line in reqfile.readlines():
            req_line = req_line.strip()
            if req_line:
                yield req_line


setup(
    name='cheat',
    # version=get_version_number(),
    author='Chris Lane',
    author_email='chris@chris-allen-lane.com',
    license='GPL3',
    description=('cheat allows you to create and view interactive cheatsheets '
                 'on the command-line. It was designed to help remind *nix '
                 'system administrators of options for commands that they use '
                 'frequently, but not frequently enough to remember.'),
    url='https://github.com/chrisallenlane/cheat',
    use_scm_version=True,
    packages=['cheat', ],
    data_files=[
        ('etc/cheat/autocomplete', ['autocomplete/cheat.bash',
                                    'autocomplete/cheat.fish',
                                    'autocomplete/cheat.zsh']),
        ('share/cheatsheets', [os.path.join('cheatsheets', f) for f
                               in os.listdir('cheatsheets')]),
    ],
    scripts=['bin/cheat'],
    setup_requires=['setuptools_scm'],
    install_requires=list(get_requirements('requirements.txt')),
)
