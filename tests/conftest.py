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
from PyPoE.poe.file.dat import RelationalReader, load_spec
from PyPoE.poe.file.ggpk import GGPKFile

# =============================================================================
# Globals
# =============================================================================

__all__ = []
_argparse_versions = {
    'stable': VERSION.STABLE,
    'beta': VERSION.BETA,
    'alpha': VERSION.ALPHA,
}

# =============================================================================
# Classes
# =============================================================================

# =============================================================================
# Functions
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


@pytest.fixture(scope='session')
def poe_version(request):
    version = _argparse_versions[request.config.getoption('--poe-version')]
    load_spec(version=version)
    return version


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
    return RelationalReader(
        path_or_ggpk=ggpkfile,
        read_options={
            # When we use this, speed > dat value features
            'use_dat_value': False
        },
    )

