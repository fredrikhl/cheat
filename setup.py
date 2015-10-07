from distutils.core import setup
import os


def get_version_number():
    u""" Get the version number from the cheat package. """
    local = dict()
    initfile = os.path.join(os.path.dirname(__file__), 'cheat', '__init__.py')
    execfile(initfile, local)
    if 'version' in local:
        return '%d.%d.%d' % local['version']
    raise Exception("No version in %r" % initfile)


setup(
    name='cheat',
    version=get_version_number(),
    author='Chris Lane',
    author_email='chris@chris-allen-lane.com',
    license='GPL3',
    description=('cheat allows you to create and view interactive cheatsheets '
                 'on the command-line. It was designed to help remind *nix '
                 'system administrators of options for commands that they use '
                 'frequently, but not frequently enough to remember.'),
    url='https://github.com/chrisallenlane/cheat',
    packages=[
        'cheat',
    ],
    data_files=[
        ('etc/cheat/autocomplete', ['autocomplete/cheat.bash',
                                    'autocomplete/cheat.fish',
                                    'autocomplete/cheat.zsh']),
        ('share/cheatsheets', [os.path.join('cheatsheets', f) for f
                               in os.listdir('cheatsheets')]),
    ],
    scripts=['bin/cheat'],
    install_requires=[
        'pygments >= 1.6.0',
        'pygments-markdown-lexer == 0.1.0.dev39', ]
)
