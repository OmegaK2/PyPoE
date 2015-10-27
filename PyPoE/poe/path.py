"""
Library init

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/path.py                                                |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Library Init

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
"""
# =============================================================================
# Imports
# =============================================================================

# Python
import sys
import os

try:
    import winreg
except ImportError:
    winreg = None

# self
from PyPoE.poe.constants import VERSION, DISTRIBUTOR

# =============================================================================
# Globals
# =============================================================================

__all__ = ['PoEPath']

# =============================================================================
# Classes
# =============================================================================

class PoEPathList(list):
    """
    Special list object to make managing list objects easier.

    Only PoEPathValue objects are appended by PoEPath, but it can be otherwise
    used just like a regular list.
    It addition it performs existence checks on the items added by default.
    """
    def __init__(self, only_existing=True):
        self._only_existing = True

    def append(self, path, version, distributor):
        if path is None:
            return

        # Will fix wrong slashes in registry
        path = os.path.realpath(path)

        if self._only_existing and not os.path.exists(path):
            return

        list.append(self, PoEPathValue(path, version, distributor))

class PoEPathValue(str):
    """
    :param path: Path to the base path of exile folder
    :type path: str
    :param version: Combination of PoEPath VERSION
    :type version: VERSION
    :param distributor: Combination of PoEPath DISTRIBUTOR values
    :type distributor: DISTRIBUTOR
    """
    def __new__(self, path, version, distributor):
        self.path = path
        self.version = version
        self.distributor = distributor

        return str.__new__(self, path)

class PoEPath(object):
    """
    Class for retrieving default paths related to path of exile.

    Note that most of the functions currently only work on Windows, as PoE is
    only officially available on windows.
    """

    def __init__(self, version=VERSION.DEFAULT, distributor=DISTRIBUTOR.DEFAULT):
        """
        Change the version or distributor if you only watch to search for
        specific installations.

        :param version: Combination of VERSION constants
        :type version: VERSION
        :param distributor: Combination of DISTRIBUTOR constants
        :type distributor: DISTRIBUTOR
        """
        self.version = version
        self.distributor = distributor

    def _get_winreg_path(self, regpath, regkey, user=True):
        if user:
            key = winreg.HKEY_CURRENT_USER
        else:
            key = winreg.HKEY_LOCAL_MACHINE

        try:
            obj = winreg.OpenKey(key, regpath)
            path = winreg.QueryValueEx(obj, regkey)[0]
            obj.Close()
        # missing key raises FileNotFoundError
        except FileNotFoundError:
            return None
        return path

    def get_installation_paths(self, only_existing=True):
        """
        Returns a PoEPathList instance containing PoEPathValues depending on
        the version and distributor values set on class construction.

        :param only_existing: If True, only existing directory will be returned.
        :type only_existing: bool
        :return: returns a PoEPathList containing PoEPathValues
        :rtype: PoEPathList
        """
        paths = PoEPathList(only_existing)

        # Currently PoE only runs on windows
        if sys.platform != 'win32':
            return paths

        # TODO: Possibly find a way to reduce this spaghetti like code
        if self.distributor & DISTRIBUTOR.GGG:
            for item in (
                ('Software\GrindingGearGames\Path of Exile', VERSION.STABLE),
                ('Software\GrindingGearGames\Path of Exile - The Awakening Closed Beta', VERSION.BETA),
            ):
                if self.version & item[1]:
                    basepath =  self._get_winreg_path(item[0], 'InstallLocation')
                    paths.append(basepath, item[1], DISTRIBUTOR.GGG)

        if self.distributor & DISTRIBUTOR.STEAM:
            basepath = self._get_winreg_path('Software\Valve\Steam', 'SteamPath')
            # Steam does have a beta, but it is installed into the same directory
            # AFAIK, there is no safe way to determine which is installed
            # unless we hook into steam
            if basepath and self.version ^ VERSION.ALL:
                # Steam Common folder
                basepath = os.path.join(basepath, 'SteamApps', 'common')
                # Seems to be both beta, and live folder
                basepath = os.path.join(basepath, 'Path of Exile')
                paths.append(basepath, VERSION.ALL, DISTRIBUTOR.STEAM)

        if self.distributor & DISTRIBUTOR.GARENA:
            if self.version & VERSION.STABLE:
                basepath = self._get_winreg_path(
                    'SOFTWARE\Wow6432Node\Garena\PoE',
                    'Path',
                    user=False
                )
                paths.append(basepath, VERSION.STABLE, DISTRIBUTOR.GARENA)


        return paths