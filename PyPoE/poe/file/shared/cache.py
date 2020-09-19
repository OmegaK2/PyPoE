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
import os
from typing import Union, List, Dict, Any

# 3rd-party

# self
from PyPoE.shared.mixins import ReprMixin
from PyPoE.poe.file.ggpk import GGPKFile
from PyPoE.poe.file.bundle import Bundle, Index, PATH_TYPES

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
    '_ggpk' : GGPKFile

    '_path' : str

    'is_unpacked' : bool

    'files' : dict[str, AbstractFileReadOnly]
        Dictionary of loaded file instances and their related path
    """

    FILE_TYPE = None

    def __init__(self,
                 path_or_ggpk: Union[str, GGPKFile] = None,
                 files: List[str] = None,
                 files_shortcut: bool = True,
                 instance_options: Dict[str, Any] = None,
                 read_options: Dict[str, Any] = None,
                 load_index: Union[bool, Index] = True,
                 bundle_cache: Union[bool, Index] = False):
        """
        Parameters
        ----------
        path_or_ggpk : str | GGPKFile
            The root path (i.e. relative to content.ggpk) where the files are
            stored or a :class:`PyPoE.poe.file.ggpk.GGPKFile` instance
        files : Iterable
            Iterable of files that will be loaded right away
        files_shortcut : bool
            Whether to use the shortcut function, i.e. self.__getitem__
        instance_options : dict[str, object]
            options to pass to the file's __init__ method
        read_options : dict[str, object]
            options to pass to the file instance's read method


        Raises
        ------
        TypeError
            if path_or_ggpk not specified or invalid type
        ValueError
            if a :class:`PyPoE.poe.file.ggpk.GGPKFile` was passed, but it was
            not parsed
        """
        if isinstance(path_or_ggpk, GGPKFile):
            if not path_or_ggpk.is_parsed:
                raise ValueError('The GGPK File must be parsed.')
            self._ggpk = path_or_ggpk
            self._path = None
        elif isinstance(path_or_ggpk, str):
            self._ggpk = None
            self._path = path_or_ggpk
        else:
            raise TypeError(
                'path_or_ggpk must be a valid directory or GGPKFile'
            )

        if isinstance(load_index, bool):
            if load_index:
                self.index = Index()
                if self._path:
                    self.index.read(os.path.join(
                        self._path, Index.PATH)
                    )
                else:
                    self.index.read(
                        self._ggpk[Index.PATH].record.extract()
                    )
            else:
                self.index = None
        elif isinstance(load_index, Index):
            self.index = load_index
        else:
            raise TypeError('load_index must be a bool or Index instance')

        if isinstance(bundle_cache, bool):
            if bundle_cache:
                self.bundle_cache = self.index
        elif isinstance(bundle_cache, Index):
            self.bundle_cache = bundle_cache
        else:
            raise TypeError('bundle_cache must be a bool or Index instance')

        self.instance_options = {} if instance_options is None else \
            instance_options
        self.read_options = {} if read_options is None else read_options

        self.files = {}

        read_func = self.__getitem__ if files_shortcut else self.get_file

        if files is not None:
            for file in files:
                read_func(file)

    def __getitem__(self, item):
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

    def _get_file_instance_args(self, file_name, *args, **kwargs):
        """
        Returns a dictionary of keyword arguments to pass to the file's
        __init__ method upon initial reading.

        Parameters
        ----------
        file_name :  str
            Name of the file


        Returns
        -------
        dict[str, object]
            Dictionary of keyword arguments
        """
        options = dict(self.instance_options)
        return options

    def _get_read_args(self, file_name : str, *args, **kwargs) -> Dict[str, Any]:
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
        is_bundle = False
        if self._ggpk:
            try:
                options['file_path_or_raw'] = \
                    self._ggpk[file_name].record.extract()
            except FileNotFoundError:
                is_bundle = True
        elif self._path:
            target = os.path.join(self._path, file_name)
            if os.path.exists(target):
                options['file_path_or_raw'] = target
            else:
                is_bundle = True

        if is_bundle:
            file_record = self.index.get_file_record(file_name)
            bundle_record = file_record.bundle

            if bundle_record.contents is None:
                if self._ggpk:
                    file_path_or_raw = \
                        self._ggpk[bundle_record.ggpk_path].record.extract()
                elif self._path:
                    file_path_or_raw = os.path.join(
                        self._path, bundle_record.ggpk_path
                    )

                bundle_record.read(file_path_or_raw)

            options['file_path_or_raw'] = file_record.get_file()

        return options

    def _create_instance(self, file_name, *args, **kwargs):
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

    def get_file(self, file_name, *args, **kwargs):
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

    @property
    def path_or_ggpk(self):
        """
        The path or :class:`PyPoE.poe.file.ggpk.GGPKFile` instance the cache
        was created with
        """
        return self._path or self._ggpk
