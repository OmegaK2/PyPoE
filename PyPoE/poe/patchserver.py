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
.. autoclass:: PatchFileList
.. autoclass:: DirectoryNodeExtended
.. autofunction:: node_check_hash
.. autofunction:: node_outdated_files

Internal API
-------------------------------------------------------------------------------

.. autofunction:: socket_fd_open
.. autofunction:: socket_fd_close
.. autoclass:: BaseRecordData
.. autoclass:: VirtualDirectoryRecord
.. autoclass:: VirtualFileRecord

"""

# =============================================================================
# Imports
# =============================================================================

# Python
import socket
import select
import struct
import io
import os
from urllib import request
from urllib.error import URLError
from collections import OrderedDict
from hashlib import sha256
from hmac import compare_digest

# 3rd-party

# self
from PyPoE.shared.mixins import ReprMixin
from PyPoE.poe.file.ggpk import DirectoryNode, DirectoryRecord, FileRecord
from PyPoE.shared.murmur2 import murmur2_32

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Functions
# =============================================================================

def socket_fd_open(socket_fd):
    """
    Create a TCP/IP socket object from a
    :meth:`socket.socket.detach` file descriptor.
    Uses :func:`socket.fromfd`.

    Parameters
    ---------
    socket_fd : fd
        File descriptor to build socket from.

    Returns
    ------
    socket : :mod:`socket`
    """

    # open new socket from fd
    sock = socket.fromfd(fd=socket_fd,
                         family=socket.AF_INET,
                         type=socket.SOCK_STREAM,
                         proto=socket.IPPROTO_TCP)
    return sock

def socket_fd_close(socket_fd):
    """
    Shutdown (FIN) and close a TCP/IP socket object from a
    :meth:`socket.socket.detach` file descriptor.

    Parameters
    ---------
    socket_fd : fd
        File descriptor for socket to close
    """

    sock = socket_fd_open(socket_fd)
    # fin the connection
    sock.shutdown(socket.SHUT_RDWR)
    # close the socket
    sock.close()

def node_check_hash(directory_node, folder_path=None, ggpk=None,
                    recurse=True, bufsize=2**20):
    """
    Compare expected hash against files on disk.

    Folder hash is sha256sum of concaterated items in folder.

    Accepts either a string folder path or a GGPKFile

    Example GGPK::

        from PyPoE.poe.file.ggpk import GGPKFile
        ggpk_file = '/mnt/poe/Path_of_Exile/Content.ggpk'
        ggpk = GGPKFile()
        ggpk.read(ggpk_file)
        ggpk.directory_build()

        from PyPoE.poe.patchserver import node_check_hash
        node_check_hash(ggpk['Data/Maps.dat'], ggpk=ggpk)

        test_node = 'Art/2DArt/Atlas'

        node = ggpk[test_node]

        # GGPK files match GGPK hashes?
        node_hashes = node_check_hash(node, ggpk=ggpk)

        if node_hashes[-1][2] is True:
          print('hashes match for {}'.format(node.get_path()))
        else:
          for child_node, child_hash, child_bool in node_hashes:
            if bool is False:
              print(child_node.record.name)
              print('{} file hash'.format(child_hash.hexdigest()))
              print('{:064x} expected hash'.format(child_node.record.hash))

        # up to date?
        import PyPoE.poe.patchserver
        patch = PyPoE.poe.patchserver.Patch()
        patch_file_list = PyPoE.poe.patchserver.PatchFileList(patch)
        cdir = ''
        for dir in test_node.split('/'):
          if len(cdir) > 0:
              cdir += '/'
          cdir += dir
          patch_file_list.update_filelist([cdir])

        from hmac import compare_digest
        node_patchserver_results = []
        for index, child in enumerate(node_hashes):
            node_path = child[0].get_path()
            node_patchserver = patch_file_list.directory[node_path]
            node_file_hash = child[1]
            hash_test = compare_digest(
                node_file_hash.hexdigest(),
                format(node_patchserver.record.hash, '064x'))

            node_patchserver_results.append(hash_test)

        if list(zip(node_hashes, node_patchserver_results))[-1][1] is True:
          print('hashes match patchserver for {}'.format(test_node))

    Example files::

        import os
        import PyPoE.poe.patchserver

        patch = PyPoE.poe.patchserver.Patch()
        patch_file_list = PyPoE.poe.patchserver.PatchFileList(patch)
        poe_dir = '/mnt/poe/Path_of_Exile'
        node_hash_list = PyPoE.poe.patchserver.node_check_hash(
          patch_file_list.directory, folder_path=poe_dir, recurse=False)
        for node, checksum, matched in node_hash_list:
          print('{} hashed okay?: {}'.format(
            node.record.name,
            matched))

    Parameters
    ---------
    directory_node : :class:`.PyPoE.poe.file.ggpk.DirectoryNode`
        The node to check that
        folder & files or GGPKFile contents match expected values.

    folder_path : str
        file system directory where files to check are located

    ggpk : :class:`.PyPoE.poe.file.ggpk.GGPKFile`
        GGPK file record

    recurse : bool
        If set, check folders

    bufsize : int
        The size of the buffer to use for computing each hash

    Returns
    ------
    :class:`list` [ :class:`tuple` ]
        :class:`.PyPoE.poe.file.ggpk.DirectoryNode` :
            The tested node

        :mod:`hashlib` :
            sha256sum for file or folder

        :class:`bool` :
            True if folder bytes hash == expected hash

    Raises
    -----
    ValueError
        One of either ggpk or folder_path must be given
    """

    if bool(folder_path) == bool(ggpk):
        raise ValueError('Must specify either folder_path or ggpk')

    node_hash = None
    hash_test = False
    self = directory_node

    if isinstance(self.record, FileRecord):
        if folder_path:
            file = os.path.join(folder_path, self.record.name)
            try:
                file_handle = open(file, 'rb')
            except FileNotFoundError:
                return [(self, node_hash, hash_test)]
        elif ggpk:
            file_handle = ggpk[self.get_path()].record.extract()

        if file_handle:
            file_hash = sha256()
            while True:
                # Hash max bufsize (1MB default) at a time
                buf = file_handle.read(bufsize)
                if not buf:
                    break
                file_hash.update(buf)

            node_hash = file_hash
            del file_hash

            hash_test = compare_digest(node_hash.hexdigest(),
                                       format(self.record.hash, '064x'))

            file_handle.close()
            del file_handle

        return [(self, node_hash, hash_test)]

    elif (isinstance(self.record, DirectoryRecord)
          or self.record is None):
        if folder_path:
            folder = ''
            if self.record is not None:
                folder = self.record.name
            folder_path = os.path.join(folder_path, folder)
            children = self.children
        elif ggpk:
            # PyPoE ggpk children are reversed
            children = self.children[::-1]

        child_hash_list = []
        hash_list = []
        missing_files = False
        # need the order of items in folder to generate hash
        for node in children:
            # if node is directory and do not want to recurse
            if not (isinstance(node.record, DirectoryRecord)
                    and not recurse):
                child_node_hash = node_check_hash(node,
                                                  folder_path=folder_path,
                                                  ggpk=ggpk,
                                                  recurse=recurse,
                                                  bufsize=bufsize)
                if child_node_hash[-1][1] is None:
                    missing_files = True
                # only calculate the folder hash from immediate
                # children hashes ... no grandchildren
                child_hash_list.append(child_node_hash[-1])
                # store all hash results to return
                hash_list += child_node_hash
        if missing_files is False and recurse:
            folder_hash_concat = b''.join(
                item[1].digest() for item in child_hash_list)
            node_hash = sha256(folder_hash_concat)
            hash_test = compare_digest(node_hash.hexdigest(),
                                       format(self.record.hash, '064x'))
        # put folder hash at end of list if recurse and not root
        if self.record is not None and recurse:
            return hash_list + [(self, node_hash, hash_test)]

        return hash_list

def node_outdated_files(patch_file_list, directory_node_path,
                        folder_path, recurse=False, bufsize=2**10):
    """
    Get expected hash based list of outdated files on disk
    for given directory node.

    Example::

        import PyPoE.poe.patchserver
        patch = PyPoE.poe.patchserver.Patch()
        patch_file_list = PyPoE.poe.patchserver.PatchFileList(patch)
        poe_dir = '/mnt/poe/Path_of_Exile'
        node = ''
        update_list = PyPoE.poe.patchserver.node_outdated_files(
            patch_file_list, node, poe_dir, recurse=False)
        print(update_list)

    Parameters
    ---------
    patch_file_list : :class:`.PatchFileList`
        The connection to a patch server

    directory_node_path : str
        The path name of the node
        :meth:`.PyPoE.poe.file.ggpk.DirectoryNode.get_path`
        to update folder & files for.

    folder_path : str
        file system directory where files to check are located

    recurse : bool
        If set, update all files in directories below directory_node_path

    bufsize : int
        The size of the buffer to use for computing each hash

    Returns
    ------
    dict
        :mod:`hashlib`:
            :class:`list`:
                :class:`PyPoE.poe.file.ggpk.DirectoryNode`
    """

    # get needed depth of directory node first
    try:
        directory_node = patch_file_list.directory[directory_node_path]
        # if directory and no child metadata
        if (isinstance(directory_node.record, DirectoryRecord)
                and not directory_node.children):
            raise FileNotFoundError('Just here to trigger the except')
    except FileNotFoundError:
        directory_paths = directory_node_path.split('/')
        cdir = ''
        for index, dir_name in enumerate(directory_paths):
            if cdir:
                cdir += '/'
            cdir += dir_name
            # do not know if node is file or folder
            # if file, second last node is final
            if (len(directory_paths) - index) < 1:
                directory_node = patch_file_list.directory[directory_node_path]
                if (directory_node.record is not None
                        and isinstance(directory_node.record, FileRecord)):
                    break
            patch_file_list.update_filelist([cdir])
    directory_node = patch_file_list.directory[directory_node_path]

    # walk metadata
    if recurse:
        directories = directory_node.directories
        end_directories = []
        while directories:
            child = directories.pop()
            # if child is directory
            if isinstance(child.record, DirectoryRecord):
                # if metadata is not present
                if not child.children:
                    patch_file_list.update_filelist([child.get_path()])
                directories = directories + child.directories
                if not child.directories:
                    end_directories.append(child)

    node_hash_list = node_check_hash(directory_node,
                                     folder_path=folder_path,
                                     recurse=recurse,
                                     bufsize=bufsize)

    download_list = {}
    for node, checksum, match in node_hash_list:
        # For files that did not match
        if isinstance(node.record, FileRecord) and not match:
            try:
                # expected hash as key,
                # so not downloading same file many times
                download_list[node.record.hash].append(node)
            except KeyError:
                download_list[node.record.hash] = [node]

    return download_list

def node_update_files(patch_file_list, directory_node_path,
                      folder_path, recurse=False, bufsize=2**10):
    """
    Update files and folders on disk for given node path.

    Example::

        import PyPoE.poe.patchserver
        patch = PyPoE.poe.patchserver.Patch()
        patch_file_list = PyPoE.poe.patchserver.PatchFileList(patch)
        poe_dir = '/tmp/pypoe/poe'
        node = 'Metadata/Items/Amulets'
        PyPoE.poe.patchserver.node_update_files(
          patch_file_list, node, poe_dir, recurse=False)
        node = 'Metadata/Items/Rings'
        PyPoE.poe.patchserver.node_update_files(
          patch_file_list, node, poe_dir, recurse=False)

    Parameters
    ---------
    patch_file_list : :class:`.PatchFileList`
        The connection to a patch server

    directory_node_path : str
        The path name of the node
        :meth:`.PyPoE.poe.file.ggpk.DirectoryNode.get_path`
        to update folder & files for.

    folder_path : str
        file system directory where files to check are located

    recurse : bool
        If set, update all files in directories below directory_node_path

    bufsize : int
        The size of the buffer to use for computing each hash
    """
    node_parent_split = directory_node_path.rsplit('/', 1)
    node_parent = directory_node_path.rsplit('/', 1)[0]
    if len(node_parent_split) == 1:
        node_parent = ''
    hash_path = os.path.join(folder_path,
                             node_parent)
    download_list = node_outdated_files(patch_file_list,
                                        directory_node_path,
                                        hash_path,
                                        recurse=recurse,
                                        bufsize=bufsize)

    from json import dump
    dump_dict = patch_file_list.directory.get_dict()
    dump_dict['version'] = patch_file_list.patch.version
    file_handle = open(os.path.join(folder_path,
                                    'poe_file_details.json'),
                       'w', encoding='utf-8')
    dump(dump_dict, file_handle)
    file_handle.close()

    dir_fd = os.open(folder_path, os.O_DIRECTORY)

    files_subdir = 'files'
    files_count = len(download_list.keys())
    download_index = 0
    for hash, nodes in download_list.items():
        pretty_hash = format(hash, '064x')
        dst_file = os.path.join(folder_path, files_subdir, pretty_hash)
        node_file_name = nodes[0].get_path()
        print("{} file downloads remaining".format(
            files_count - download_index))
        patch_file_list.patch.download(node_file_name,
                                       dst_file=dst_file)
        print("downloaded: {}".format(node_file_name))
        download_index += 1

        for node in nodes:
            link_src = dst_file
            node_path = node.get_path()
            link_dst = os.path.join(folder_path,
                                    node_path)
            link_parent = os.path.dirname(link_dst)
            os.makedirs(link_parent, exist_ok=True)
            link_source_rel = os.path.relpath(link_src, link_parent)
            try:
                old_source = os.path.realpath(link_dst)
                if old_source != link_src:
                    os.remove(old_source, dir_fd=dir_fd)
            except FileNotFoundError:
                pass

            try:
                os.remove(node_path, dir_fd=dir_fd)
            except FileNotFoundError:
                pass

            os.symlink(link_source_rel, node_path, dir_fd=dir_fd)

    os.close(dir_fd)

# =============================================================================
# Classes
# =============================================================================


class Patch:
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
    sock_fd : fd
        Socket file descriptor for connection to patch server
    """

    _SERVER_IPV4 = '172.65.204.172'
    _SERVER_IPV6 = '2606:4700:90:0:7976:9369:8e00:f737'
    _PORT = 12995
    # use patch proto 4
    _PROTO = b'\x01\x04'

    def __init__(self, master_server=_SERVER_IPV4, master_port=_PORT):
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

    def __del__(self):
        """
        Automatically close the patchserver connection and socket.
        """

        sock = socket_fd_open(self.sock_fd)
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            sock.close()
        except OSError:
            raise

    def update_patch_urls(self):
        """
        Updates the patch urls from the master server.

        Open a connection to the patchserver, get webroot details,
        detach from socket, and store socket file descriptor as :attr:`sock_fd`

        .. note::

            Recreate socket object later with: :func:`.socket_fd_open`

            When finished, destroy socket with: :func:`.socket_fd_close`.
            Equivalent is called in :meth:`.__del__`
        """
        with socket.socket(proto=socket.IPPROTO_TCP) as sock:
            sock.connect(self._master_server)
            sock.send(Patch._PROTO)
            data = io.BytesIO(sock.recv(1024))

            unknown = struct.unpack('B', data.read(1))[0]
            blank = struct.unpack('33s', data.read(33))[0]

            url_length = struct.unpack('B', data.read(1))[0]
            self.patch_url = data.read(url_length*2).decode('utf-16')

            blank = struct.unpack('B', data.read(1))[0]

            url2_length = struct.unpack('B', data.read(1))[0]
            self.patch_cdn_url = data.read(url2_length*2).decode('utf-16')

            # Close this later!
            self.sock_fd = sock.detach()

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
        hosts = [self.patch_url]
        for index, host in enumerate(hosts):
            try:
                with request.urlopen(
                    url="%s%s" % (host, file_path),
                ) as robj:
                    if robj.getcode() != 200:
                        raise ValueError('HTTP response code: %s' % robj.getcode())
                    return robj.read()
            except URLError as url_error:
                # try alternate patch url if connection refused
                if (not isinstance(url_error.reason, ConnectionRefusedError)
                    or not index < len(hosts)):
                    raise url_error

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

class PatchFileList:
    """
    Class that retrieves file details from the patch server.

    Example::

        import PyPoE.poe.patchserver
        patch = PyPoE.poe.patchserver.Patch()
        patch_file_list = PyPoE.poe.patchserver.PatchFileList(patch)
        patch_file_list.update_filelist(['Data'])

    .. note::

        Patch server protocol

        1. Open TCP 12995 us.login.pathofexile.com
        2. Client hello

           push 01 04:
               04 = patch proto 4

               05 = patch proto 5
        3. receive web root & backup web root
        4. Client request folder details

           push 03 00 folder_name_length folder_name_in_utf16_LittleEndian:
               Root: 0300 00

               Art: 0300 03 410072007400
        5. receive single-depth item list for queried folder

           proto 4 root example:
               2 byte header:
                   0400

               byte folder_name_length:
                   Root: 00

               folder_name_length bytes folder_name:
                   Root: null

               int list_length (number of items in folder):
                   00 00 00 17

               list_of_items:
                   For each item:
                       2 byte item type:
                           0000 file

                           0100 folder (in content.ggpk)

                       byte item_name_length

                       item_name_length bytes UTF-16 item name

                       int(BE) file size in bytes

                       32 byte sha256sum

           proto 5:
               not understood: different datatypes, Endianness,
               and some values are compressed or encoded.

               2 byte header:
                   0400

               n-byte unknown:
                   ?folder name length

                   ?folder name

                   ?list_length (number of items in folder):

               list_of_items:
                   For each item:
                       n-byte unknown:
                           ?item type

                           some missing int(BE) file size in bytes

                           some missing ?int(LE) item_name_length

                           some missing item_name_length-some_value bytes
                           partial UTF-16 item name

                       32 byte sha256sum

        6. client checks provided hashes / sizes against files,
           and Content.ggpk records for directories.

           * directory hashes are SHA-256
             of the concatenated SHA-256 hashes of the children.
           * if file checksum fails, queue failed file for download.
           * if directory checksum fails, get folder details for
             failed folder name (step 4) from patch server

    Attributes
    ---------
    patch : :class:`.Patch`
        Store patch server details.
    sock : :mod:`socket`
        Store socket, to use single connection for multiple queries.
    sock_timeout : float
        Socket timeout value in seconds, for :meth:`socket.socket.settimeout`.
    data : :class:`io.BytesIO`
        Store server_data from socket, for processing in multiple methods.
    directory : :class:`.DirectoryNodeExtended`
        Store patch file list data as :class:`PyPoE.poe.file.ggpk.DirectoryNode`
    """
    _PROTO_PRE = b'\x03\x00'
    _PROTO_HEADER2 = b'\x04\x00'

    def __init__(self, patch, socket_timeout=1.0):
        """
        Automatically fetch root file list on class creation.

        Parameters
        ----------
        patch : :class:`.Patch`
            A Patch object

        socket_timeout : float
            Socket timeout value in seconds, for :meth:`socket.socket.settimeout`.
        """
        # Want patch server details from Patch instance
        self.patch = patch
        # Want socket fd details from Patch instance
        self.sock = socket_fd_open(patch.sock_fd)
        self.sock_timeout = socket_timeout
        self.data = bytes

        self.directory = DirectoryNodeExtended(None, None, None)

        # Get the root filelist
        self.update_filelist([''])

    def __del__(self):
        """
        Detach socket on instance deletion
        """
        self.patch.sock_fd = self.sock.detach()

    def read(self, read_length):
        """
        Read length of data from :attr:`.data`.
        Get and save more data from :attr:`.sock` if length not met.

        Parameters
        ---------
        read_length : int
            Length of data to read

        Returns
        ------
        bytes
            Requested data

        Raises
        -----
        EOFError
            If the TCP stream returned by the patch server ends unexpectedly
        """
        # The amount of data to pull from socket each recv
        # Amount recv will be < network MTU
        bufsize = 2048
        # Need to be able to set data, which is used by other methods
        data_stream = self.data
        # Need details of socket
        sock = self.sock
        # Get the seek (cursor) position of data
        data_current = data_stream.tell()
        recv_attempts = 0
        while True:
            # no single value should be long enough to be broken
            # over more than 1 TCP packet
            if recv_attempts > 1:
                raise EOFError('Too many attempts to pull data'
                               + ' when expecting more data')
            # Attempt to read length asked for
            data_read = data_stream.read(read_length)
            recv_attempts += 1
            # If less data than expected
            if len(data_read) < read_length:
                # Check if there is more data waiting in the socket
                # And that data waiting is not an empty TCP packet
                sockets_ready = select.select([sock], [], [], 0)
                if (len(sockets_ready) < 1
                    or len(sock.recv(1, socket.MSG_PEEK)) < 1):
                    # If there is no more data, something is wrong
                    raise EOFError('Reached end of TCP stream'
                                   + ' when expecting more data')
                # Otherwise, create a new data stream with
                # all existing data + data pulled from socket
                data_stream.seek(0)
                data_all = data_stream.read() + sock.recv(bufsize)
                data_stream = io.BytesIO(data_all)
                data_stream.seek(data_current)
                # Set instance data, for access from other methods
                self.data = data_stream
            else:
                break
        return data_read

    def extract_varchar(self):
        """
        Helper function to extract variable length string from :attr:`.data`.
        String length is first byte of data.

        Returns
        -------
        str
            extracted variable length string
        """
        # First bytes tells length of string
        varchar_length = struct.unpack('B', self.read(1))[0]
        # String encoded utf-16 is 2*string length bytes
        varchar_length_blob = varchar_length * 2
        # Sometimes (root), length is 0, string is empty
        varchar_name = ''
        if varchar_length > 0:
            varchar_name = self.read(
                varchar_length_blob).decode('utf-16')
        return varchar_name

    def update_filelist(self, folders):
        """
        Get file details for a folder from the patch server.

        Stores data in :attr:`.directory`

        Patchserver works top down:
        PatchFileList().directory.children entries are not known
        until that directory is traversed.

        Once a directory level is traversed,
        patchserver can be queried for next directory.

        It will return item details for all items in queried directory.

        Parameters
        ---------
        folders : list
            The list of folders to get details for
            ?Only one level at a time


        Raises
        -----
        ValueError
            If folders list contains repeated folders

        ValueError
            If root is requested alongside additional folders

        KeyError
            If the patch server sends data not understood
        """
        if len(set(folders)) != len(folders):
            raise ValueError('folder list contains non unique folder')

        folder_query = b''
        for folder in folders:
            if folder == '':
                if len(folders) > 1:
                    raise ValueError('if querying root,'
                                     + 'only root allowed')
                # query root folder (0 length folder name)
                folder_query = (PatchFileList._PROTO_PRE
                                + b'\x00')
            else:
                # test if folder is known
                try:
                    test_directory = self.directory[folder].record
                    if not isinstance(test_directory, DirectoryRecord):
                        raise ValueError('Must only query folders.')
                except FileNotFoundError:
                    raise ValueError('Queried folder unknown.'
                                     + ' Must traverse patchserver'
                                     + ' top (root) to bottom')

                query_folder_length = struct.pack('B', len(folder))
                query_folder_name = folder.encode('utf-16le')
                query_folder = (PatchFileList._PROTO_PRE
                                + query_folder_length
                                + query_folder_name)
                folder_query += query_folder

        sock = self.sock
        sock.send(folder_query)
        sock.settimeout(self.sock_timeout)
        sock_data = sock.recv(2048)
        data = io.BytesIO(sock_data)
        # Set instance data, so that it can be modified by other methods
        self.data = data

        for folder in folders:
            # patch proto 4 decode
            query_header = struct.unpack('2s', self.read(2))[0]
            query_folder_name = ''
            folder_name = ''
            if query_header != PatchFileList._PROTO_HEADER2:
                raise KeyError('Unknown patch server header:'
                               + ' {} from query: {}'
                               .format(query_header, folder_query))

            folder_name = self.extract_varchar()

            item_count = struct.unpack('>I', self.read(4))[0]

            print('{} items in directory {}'
                  .format(item_count, folder_name))

            parent = self.directory[folder]

            folder_directory_nodes = []

            for item in range(0, item_count):
                header = struct.unpack('2s', self.read(2))[0]
                if header == b'\x00\x00':
                    tag = 'FILE'
                elif header == b'\x01\x00':
                    tag = 'PDIR'
                else:
                    raise KeyError('Unknown patch server'
                                   + ' item type:'
                                   + ' {} from query: {}'
                                   .format(header, folder_query))

                name = self.extract_varchar()

                # 4 byte unsigned int item size in bytes
                # 32 byte sha256 item checksum
                size, sha256sum = struct.unpack(
                    '>I32s', self.read(36))

                # store sha256sum as int
                sha256sum = int.from_bytes(sha256sum, byteorder='big')

                if tag == DirectoryRecord.tag:
                    temp_record = VirtualDirectoryRecord(
                        name=name,
                        hash=sha256sum)
                elif tag == FileRecord.tag:
                    temp_record = VirtualFileRecord(
                        name=name,
                        hash=sha256sum,
                        size=size)

                folder_directory_nodes.append(DirectoryNodeExtended(
                    record=temp_record,
                    hash=murmur2_32(name.lower().encode('utf-16le')),
                    parent=parent))

            parent.children = folder_directory_nodes

class BaseRecordData(ReprMixin):
    """
    Sibling to :class:`PyPoE.poe.file.ggpk.BaseRecord`.

    :attr:`PyPoE.poe.file.ggpk.DirectoryNode.record` item base class.
    Built from record data, rather than pointer details
    from GGPK file.

    Used for each item detailed by patchserver.

    Attributes
    ---------
    _name :  str
        Name of item
    hash :  int
        SHA256 hash of file contents
    """
    def __init__(self, name, hash):
        self._name = name
        self.hash = hash

class VirtualDirectoryRecord(BaseRecordData,
                             DirectoryRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class VirtualFileRecord(BaseRecordData,
                        FileRecord):
    def __init__(self, name, hash, size):
        self.data_length = size
        super().__init__(name, hash)

class DirectoryNodeExtended(DirectoryNode):
    """
    Adds methods:
        :meth:`.get_dict`

        :meth:`.load_dict`

        :meth:`.gen_walk`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_dict(self, recurse=True):
        """
        Get a dict of :class:`PyPoE.poe.file.ggpk.DirectoryNode`
        record item details

        Example::

            from json import dump
            dump_dict = patch_file_list.directory.get_dict()
            dump_dict['version'] = patch_file_list.patch.version
            file_handle = open('poe_file_details.json', 'w', encoding='utf-8')
            dump(dump_dict, file_handle)
            file_handle.close()

        Parameters
        --------
        recurse : bool
            True = include children

        Returns
        ------
        collections.OrderedDict
            keys:
                hash

                name

                size

                type: folder or file

                Folders have children[]
        """
        record_dict = OrderedDict()

        if isinstance(self.record, BaseRecordData):
            record_dict['name'] = self.record._name

            pretty_hash = format(self.record.hash, '064x')
            record_dict['hash'] = pretty_hash

            if isinstance(self.record, VirtualDirectoryRecord):
                record_dict['type'] = 'folder'
            elif isinstance(self.record, VirtualFileRecord):
                record_dict['type'] = 'file'
                record_dict['size'] = self.record.data_length
        else:
            record_dict['name'] = 'ROOT'


        if recurse is True:
            if len(self.children) > 1:
                children = []
                record_dict['children'] = children

                for child in self.children:
                    children.append(child.get_dict())

        return record_dict

    def load_dict(self, node_dict, parent=None):
        """
        Fill a :class:`DirectoryNode` from a dict

        Example::

            import json
            from collections import OrderedDict
            file_handle = open('poe_file_details.json', 'r', encoding='utf-8')
            file_dict = json.load(file_handle, object_pairs_hook=OrderedDict)
            file_handle.close()

        Parameters
        ---------
        node_dict : collections.OrderedDict
            Ordered dict from :meth:`DirectoryNodeExtended.get_dict`

        """
        if not isinstance(node_dict, OrderedDict):
            raise TypeError('OrderedDict required')

        node_children = []

        node_name = node_dict['name']
        if node_name == 'ROOT':
            temp_record = None
            node_hash = None
        else:
            node_type = node_dict['type']

            # unpretty hash. str hex bytes -> bytes
            pretty_hash = node_dict['hash']
            # store sha256sum as int
            node_hash = int(pretty_hash, 16)

            if node_type == 'file':
                node_file_size = node_dict['size']

                temp_record = VirtualFileRecord(
                    name=node_name,
                    hash=node_hash,
                    size=node_file_size)

            elif node_type == 'folder':
                temp_record = VirtualDirectoryRecord(
                    name=node_name,
                    hash=node_hash)

            else:
                raise KeyError('Unknown type: {}'.format(
                    node_type))

        if parent is None:
            self.record = temp_record
            self.hash = node_hash
            self.parent = None
            child_node = self
        else:
            child_node = DirectoryNodeExtended(
                record=temp_record,
                hash=node_name,
                parent=parent)
            parent.children.append(child_node)

        try:
            node_children = node_dict['children']
            if node_children:
                for child in node_children:
                    child_node.load_dict(child, child_node)
        except KeyError:
            pass

    def gen_walk(self, max_depth=-1, _depth=0):
        """
        A depth first recursive generator for a DirectoryNode

        Example::

            for node, depth in patch_file_list.directory.gen_walk():
              try:
                name = node.record.name
              except:
                name = 'ROOT'
              print('{blank:>{width}}{name}'.format(
                name=name, width=depth, blank=''))

        Parameters
        ---------
        max_depth : int
            how many levels of children to walk

        Returns
        ------
        tuple
            (:class:`.DirectoryNodeExtended`, depth)
        """
        # only continue if not past maximum depth
        if (max_depth == -1 or _depth <= max_depth):
            yield (self, _depth)
            _depth += 1
            # don't recurse it that goes over max_depth
            if (max_depth == -1 or _depth <= max_depth):
                # depth first
                for child in self.children:
                    yield from child.gen_walk(max_depth, _depth)
