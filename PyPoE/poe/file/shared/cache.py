"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/shared/cache.py                                   |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

All file caches classes will inherit :class:`AbstractFileCache`.

.. warning::
    None of the abstract classes found here should be instantiated directly.

See also:

* :mod:`PyPoE.poe.file.shared`
* :mod:`PyPoE.poe.file.shared.keyvalues`


Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

.. autoclass:: AbstractFileCache
    :private-members:
"""

# =============================================================================
# Imports
# =============================================================================

# Python
from typing import Union, List, Dict, Any

# 3rd-party

# self
from PyPoE.shared.mixins import ReprMixin
from PyPoE.poe.file.shared import AbstractFileReadOnly
from PyPoE.poe.file.file_system import FileSystem

# =============================================================================
# Globals
# =============================================================================

__all__ = ['AbstractFileCache']

# =============================================================================
# Classes
# =============================================================================


class AbstractFileCache(ReprMixin):
    """
    Attributes
    ----------

    'is_unpacked' : bool

    'files' : dict[str, AbstractFileReadOnly]
        Dictionary of loaded file instances and their related path
    """

    FILE_TYPE = None

    def __init__(self,
                 path_or_file_system: Union[str, FileSystem] = None,
                 files: List[str] = None,
                 files_shortcut: bool = True,
                 instance_options: Dict[str, Any] = None,
                 read_options: Dict[str, Any] = None):
        """
        Parameters
        ----------
        path_or_file_system
            The root path (i.e. relative to content.ggpk) where the files are
            stored or a :class:`PyPoE.poe.file.ggpk.GGPKFile` instance
        files
            Iterable of files that will be loaded right away
        files_shortcut
            Whether to use the shortcut function, i.e. self.__getitem__
        instance_options
            options to pass to the file's __init__ method
        read_options
            options to pass to the file instance's read method


        Raises
        ------
        TypeError
            if path_or_ggpk not specified or invalid type
        ValueError
            if a :class:`PyPoE.poe.file.ggpk.GGPKFile` was passed, but it was
            not parsed
        """

        if isinstance(path_or_file_system, FileSystem):
            self.file_system: FileSystem = path_or_file_system
        else:
            self.file_system: FileSystem = FileSystem(root_path=path_or_file_system)

        self.instance_options: Dict[str, Any] = {} if \
            instance_options is None else instance_options
        self.read_options: Dict[str, Any] = {} if \
            read_options is None else read_options

        self.files: Dict[str, AbstractFileReadOnly] = {}

        read_func = self.__getitem__ if files_shortcut else self.get_file

        if files is not None:
            for file in files:
                read_func(file)

    def __getitem__(self, item: str) -> Any:
        """
        Shortcut.

        Equivalent:

        * AbstractFileCache[item] <==> AbstractFileCache.read_file(item)

        Parameters
        ----------
        item : str
            item to retrieve

        Returns
        -------
        AbstractFileReadOnly
            instance
        """
        return self.get_file(item)

    def _get_file_instance_args(self,
                                file_name: str,
                                *args,
                                **kwargs) -> Dict[str, Any]:
        """
        Returns a dictionary of keyword arguments to pass to the file's
        __init__ method upon initial reading.

        Parameters
        ----------
        file_name
            Name of the file


        Returns
        -------
        dict[str, object]
            Dictionary of keyword arguments
        """
        options = dict(self.instance_options)
        return options

    def _get_read_args(self,
                       file_name: str,
                       *args,
                       **kwargs) -> Dict[str, Any]:
        """
        Returns a dictionary of keyword arguments to pass to the file's
        read method upon initial reading.

        In particular it sets file_path_or_raw based on how the cache was
        instantiated.

        Parameters
        ----------
        file_name :  str
            Name of the file


        Returns
        -------
        dict[str, object]
            Dictionary of keyword arguments
        """
        options = dict(self.read_options)
        options['file_path_or_raw'] = self.file_system.get_file(file_name)

        return options

    def _create_instance(self,
                         file_name: str,
                         *args,
                         **kwargs) -> Any:
        """
        Creates a new instance for the given file name

        Parameters
        ----------
        file_name :  str
            Name to the file to pass on


        Returns
        -------

            File instance
        """
        f = self.FILE_TYPE(
            **self._get_file_instance_args(file_name=file_name, *args, **kwargs)
        )
        f.read(**self._get_read_args(file_name=file_name, *args, **kwargs))
        return f

    def get_file(self,
                 file_name: str,
                 *args,
                 **kwargs) -> AbstractFileReadOnly:
        """
        Returns the the specified file from the cache.

        If the file does not exist, read it from the path specified on cache
        creation, add it to the cache and then return it.

        Parameters
        ----------
        file_name :  str
            File to retrieve


        Returns
        -------
        AbstractFileReadOnly
            read file instance
        """
        if file_name not in self.files:
            f = self._create_instance(file_name=file_name)
            self.files[file_name] = f
        else:
            f = self.files[file_name]

        return f
