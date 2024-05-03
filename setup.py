#!/usr/bin/env python
# encoding: utf-8
import os
import setuptools

if __name__ == '__main__':
    setuptools.setup(
        data_files=[
            ('etc/cheat/autocomplete', ['autocomplete/cheat.bash',
                                        'autocomplete/cheat.fish',
                                        'autocomplete/cheat.zsh']),
            ('share/cheatsheets', [os.path.join('cheatsheets', f) for f
                                   in os.listdir('cheatsheets')]),
        ],
        scripts=['bin/cheat'],
    )
