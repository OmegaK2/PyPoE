"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

extras_require = {
    'dev': ['sphinx', 'pytest'],
    'cli': ['colorama', 'graphviz', 'tqdm', 'mwclient', 'mwparserfromhell', 'rapidfuzz'],
    'ui': ['pyside2==5.14.0'],
    'ui-extra': ['PyOpenGL'],
}

_full = {'full': set(), 'cli-full': set(), 'ui-full': set()}

for k, v in dict(extras_require).items():
    for item in v:
        _full['full'].add(item)
        if k.startswith('cli'):
            _full['cli-full'].add(item)
        if k.startswith('ui'):
            _full['ui-full'].add(item)

for k, v in _full.items():
    extras_require[k] = list(v)

setup(
    name='PyPoE',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0.0a0',

    description='Python Tools for Path of Exile',
    long_description="""""",

    # The project's main homepage.
    url='https://github.com/OmegaK2/PyPoE',

    # Author details
    author='[#OMEGA] - K2',
    author_email='omegak2@gmx.de',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only'
    ],

    # What does your project relate to?
    keywords='', # TODO

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['configobj', 'brotli', 'fnvhash', 'cffi'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require=extras_require,

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'PyPoE': ['_data/*'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.8/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],
    data_files=[
        #('', ['PyPoE/_data/*'])
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={ # TODO
        'console_scripts': [
            'pypoe_exporter=PyPoE.cli.exporter.core:main',
        ],
        'gui_scripts': [
            'pypoe_ui=PyPoE.ui:main',
        ],
    },
)
