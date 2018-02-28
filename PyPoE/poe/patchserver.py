"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/patchserver.py                                         |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Utility functions and classes for connecting to the PoE patch server and
downloading files from it.


Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

Public API
-------------------------------------------------------------------------------

.. autoclass:: Patch

Internal API
-------------------------------------------------------------------------------
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import socket
import struct
import io
import os
from urllib import request

# 3rd-party

# self

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================


class Patch(object):
    """
    Class that handles connecting to the patching server and downloading files
    from the patching server.

    Attributes
    ----------
    patch_url : str
        Base patch url for the current PoE version. This does not point to a
        specific, load-balanced server
    patch_cdn_url : str
        Load-balanced patching url including port for the current PoE version.
    """

    _SERVER = 'pathofexile.com'
    _PORT = 12995
    _PROTO = b'\x01\x05'

    def __init__(self, master_server=_SERVER, master_port=_PORT):
        """
        Automatically fetches patching urls on class creation.

        .. note::

            Parameter shouldn't be required to be changed; if the servers change
            please create a pull request/issue on Github.

        Parameters
        ----------
        master_server : str
            Domain or IP address of the master patching server
        master_port : int
            Port to use when connecting to the master patching server
        """
        self._master_server = (master_server, master_port)
        self.update_patch_urls()

    def update_patch_urls(self):
        """
        Updates the patch urls from the master server.
        """
        with socket.socket(proto=socket.IPPROTO_TCP) as sock:
            sock.connect(self._master_server)
            sock.send(Patch._PROTO)
            data = io.BytesIO(sock.recv(1024))

            unknown = struct.unpack('<B', data.read(1))[0]

            data.seek(34)
            url_length = struct.unpack('<B', data.read(1))[0]
            self.patch_url = data.read(url_length*2).decode('utf-16')

            data.seek(2, io.SEEK_CUR)
            self.patch_cdn_url = data.read(999).decode('utf-16')

            sock.close()

    def download(self, file_path, dst_dir=None, dst_file=None):
        """
        Downloads the file at the specified path from the patching server.

        Any intermediate directories for the write paths will be automatically
        created.

        Parameters
        ----------
        file_path : str
            path of the file relative to the content.ggpk root directory
        dst_dir : str
            Write the file to the specified directory.

            The target directory is seen as the root directory, thus the
            file will be written according to it's ``file_path``

            Mutually exclusive with the ``dst_file`` argument.
        dst_file : str
            Write the file to the specified location.

            Unlike dst_dir this will ignore any naming conventions from
            ``file_path``, so for example ``Data/Mods.dat`` could be written to
            ``C:/HelloWorld.txt``

            Mutually exclusive with the ``'dst_dir`` argument.

        Raises
        ------
        ValueError
            if neither dst_dir or dst_file is set
        ValueError
            if the HTTP status code is not 200 (and it wasn't raised by urllib)
        """
        if dst_dir:
            write_path = os.path.join(dst_dir, file_path)
        elif dst_file:
            write_path = dst_file
        else:
            raise ValueError('Either dst_dir or dst_file must be set')

        # Make any intermediate dirs to avoid errors
        os.makedirs(os.path.split(write_path)[0], exist_ok=True)

        # As per manual, writing should automatically find the optimal buffer
        with open(write_path, mode='wb') as f:
            f.write(self.download_raw(file_path))

    def download_raw(self, file_path):
        """
        Downloads the raw bytes.

        Parameters
        ----------
        file_path : str
            path of the file relative to the content.ggpk root directory

        Returns
        -------
        bytes
            the raw contents of the file in bytes

        Raises
        ------
        ValueError
            if the HTTP status code is not 200 (and it wasn't raised by urllib)
        """
        with request.urlopen(
            url="%s%s" % (self.patch_cdn_url, file_path),
        ) as robj:
            if robj.getcode() != 200:
                raise ValueError('HTTP response code: %s' % robj.getcode())
            return robj.read()

    @property
    def version(self):
        """
        Retrieves the game version from the url.

        Returns
        -------
        str
            The gama version in x.x.x.x format.

            The first 3 digits match the public known versions, the last is
            internal scheme for the a/b/c patches and hotfixes.
        """
        return self.patch_url.strip('/').rsplit('/', maxsplit=1)[-1]

# =============================================================================
# Functions
# =============================================================================