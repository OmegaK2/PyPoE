"""
Path     PyPoE/poe/path.py
Name     Library init
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Library Init


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""
# =============================================================================
# Imports
# =============================================================================

import sys
import os

try:
    import winreg
except ImportError:
    winreg = None

# =============================================================================
# Globals
# =============================================================================

__all__ = ['PoePath']

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

        if self._only_existing and not os.path.exists(path):
            return

        list.append(self, PoEPathValue(path, version, distributor))

class PoEPathValue(str):
    """
    :param path: Path to the base path of exile folder
    :type path: str
    :param version: Combination of PoEPath VERSION_
    :type version: int
    :param distributor: Combination of PoEPath DISTRIBUTOR_ values
    :type distributor: int
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

    # TODO: Garena

    VERSION_STABLE = 1
    VERSION_BETA = 2

    VERSION_ALL = VERSION_STABLE | VERSION_BETA
    VERSION_DEFAULT = VERSION_STABLE
    
    VERSIONS = [VERSION_STABLE, VERSION_BETA]
    
    DISTRIBUTOR_GGG = 1
    DISTRIBUTOR_STEAM = 2

    DISTRIBUTOR_ALL = DISTRIBUTOR_GGG | DISTRIBUTOR_STEAM
    DISTRIBUTOR_DEFAULT = DISTRIBUTOR_ALL
    
    DISTRIBUTORS = [DISTRIBUTOR_GGG, DISTRIBUTOR_STEAM]

    def __init__(self, version=VERSION_DEFAULT, distributor=DISTRIBUTOR_DEFAULT):
        """
        Change the version or distributor if you only watch to search for
        specific installations.

        :param version: Combination of PoEPath VERSION_ constants
        :type version: int
        :param distributor: Combination of PoEPath DISTRIBUTOR_ constants
        :type version: int
        """
        self.version = version
        self.distributor = distributor

    def _get_winreg_path(self, regpath, regkey):
        try:
            obj = winreg.OpenKey(winreg.HKEY_CURRENT_USER, regpath)
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
        if self.distributor & PoEPath.DISTRIBUTOR_GGG:
            for item in (
                ('Software\GrindingGearGames\Path of Exile', PoEPath.VERSION_STABLE),
                ('Software\GrindingGearGames\Path of Exile - The Awakening Closed Beta', PoEPath.VERSION_BETA),
            ):
                if self.version & item[1]:
                    basepath =  self._get_winreg_path(item[0], 'InstallLocation')
                    paths.append(basepath, item[1], PoEPath.DISTRIBUTOR_GGG)


        if self.distributor & PoEPath.DISTRIBUTOR_STEAM:
            basepath = self._get_winreg_path('Software\Valve\Steam', 'SteamPath')
            # Steam does have a beta, but it is installed into the same directory
            # AFAIK, there is no safe way to determine which is installed
            # unless we hook into steam
            if basepath and self.version ^ PoEPath.VERSION_ALL:
                # Steam Common folder
                basepath = os.path.join(basepath, 'SteamApps', 'common')
                # Seems to be both beta, and live folder
                basepath = os.path.join(basepath, 'Path of Exile')
                paths.append(basepath, PoEPath.VERSION_ALL, PoEPath.DISTRIBUTOR_STEAM)

        return paths