"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/path.py                                                |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Utilities for retrieving Path of Exile related paths.

Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

.. autoclass:: PoEPath
    :special-members: __init__
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
    def __new__(self, path, version, distributor):
        """

        Parameters
        ----------
        path : str
            Path to the base path of exile folder
        version : VERSION
            Combination of PoEPath VERSION
        distributor : DISTRIBUTOR
            Combination of PoEPath DISTRIBUTOR values
        """
        self.path = path
        self.version = version
        self.distributor = distributor

        return str.__new__(self, path)


class PoEPath:
    """
    Class for retrieving default paths related to path of exile.

    .. warning::
        Currently this only works on the Windows platform, as there is no
        official Path of Exile client on Linux.
    """

    def __init__(self, version=VERSION.DEFAULT, distributor=DISTRIBUTOR.DEFAULT):
        """
        Change the version or distributor if you only watch to search for
        specific installations.

        Parameters
        ----------
        version : VERSION
            Combination of :class:`PyPoE.poe.constants.VERSION` constants
        distributor : DISTRIBUTOR
            Combination of :class:`PyPoE.poe.constants.DISTRIBUTOR` constants
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

        Parameters
        ----------
        only_existing : bool
            If True, only existing directory will be returned.

        Returns
        -------
        list
            returns a PoEPathList containing PoEPathValues
        """
        paths = PoEPathList(only_existing)

        # Currently PoE only runs on windows
        if sys.platform != 'win32':
            return paths

        # TODO: Possibly find a way to reduce this spaghetti like code
        if self.distributor & DISTRIBUTOR.GGG:
            for item in (
                (r'Software\GrindingGearGames\Path of Exile', VERSION.STABLE),
                (r'Software\GrindingGearGames\Path of Exile - beta', VERSION.BETA),
                (r'Software\GrindingGearGames\Path of Exile - Alpha',
                 VERSION.ALPHA)
            ):
                if self.version & item[1]:
                    basepath =  self._get_winreg_path(item[0], 'InstallLocation')
                    paths.append(basepath, item[1], DISTRIBUTOR.GGG)

        if self.distributor & DISTRIBUTOR.STEAM:
            basepath = self._get_winreg_path(r'Software\Valve\Steam',
                                             'SteamPath')
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
                    r'SOFTWARE\Wow6432Node\Garena\PoE',
                    'Path',
                    user=False
                )
                paths.append(basepath, VERSION.STABLE, DISTRIBUTOR.GARENA)


        return paths