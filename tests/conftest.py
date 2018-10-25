"""


Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/conftest.py                                                |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================



Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os.path

# 3rd-party
import pytest

# self
from PyPoE.poe.constants import VERSION, DISTRIBUTOR
from PyPoE.poe.path import PoEPath
from PyPoE.poe.file import dat
from PyPoE.poe.file.specification import load
from PyPoE.poe.file.ggpk import GGPKFile
from PyPoE.cli.exporter.core import setup_config
from PyPoE.cli.exporter import config

# =============================================================================
# Globals
# =============================================================================

__all__ = []
_argparse_versions = {
    'stable': VERSION.STABLE,
    'beta': VERSION.BETA,
    'alpha': VERSION.ALPHA,
}

run = True

# =============================================================================
# Classes
# =============================================================================

# =============================================================================
# Functions
# =============================================================================


def get_version(config):
    return _argparse_versions[config.getoption('--poe-version')]

# =============================================================================
# pytest generators
# =============================================================================


def pytest_addoption(parser):
    parser.addoption(
        '--poe-version',
        action="store",
        choices=list(_argparse_versions.keys()),
        default='stable',
        help='Target version of path of exile; different version will test '
             'against different specifications.'
    )


def pytest_generate_tests(metafunc):
    global run
    if run:
        dat.set_default_spec(version=get_version(metafunc.config))
        run = False
    if 'dat_file_name' in metafunc.fixturenames:
        file_names = [
            fn for fn in load(
                version=get_version(metafunc.config)
            )
        ]

        metafunc.parametrize('dat_file_name', file_names)
    elif 'unique_dat_file_name' in metafunc.fixturenames and \
            'unique_dat_field_name' in metafunc.fixturenames:
        tests = []
        for file_name, file_section in load(
                version=get_version(metafunc.config)).items():
            for field_name, field_section in file_section['fields'].items():
                if not field_section['unique']:
                    continue
                tests.append((file_name, field_name))

        metafunc.parametrize(
            ('unique_dat_file_name', 'unique_dat_field_name'),
            tests,
        )

# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(scope='session')
def poe_version(request):
    v = get_version(request.config)
    dat.set_default_spec(v)
    return v


@pytest.fixture(scope='session')
def poe_path(poe_version):
    paths = PoEPath(
        version=poe_version,
        distributor=DISTRIBUTOR.INTERNATIONAL
    ).get_installation_paths(only_existing=True)

    if paths:
        return paths[0]
    else:
        pytest.skip('Path of Exile installation not found.')


@pytest.fixture(scope='session')
def ggpkfile(poe_path):
    ggpk = GGPKFile()
    ggpk.read(os.path.join(poe_path, 'content.ggpk'))
    ggpk.directory_build()

    return ggpk


@pytest.fixture(scope='session')
def rr(ggpkfile):
    return dat.RelationalReader(
        path_or_ggpk=ggpkfile,
        read_options={
            # When we use this, speed > dat value features
            'use_dat_value': False
        },
        raise_error_on_missing_relation=False,
    )


@pytest.fixture(scope='session')
def cli_config():
    setup_config()
    config.set_option('language', 'English')
