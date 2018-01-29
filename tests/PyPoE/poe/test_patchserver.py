"""
Tests for PyPoE.poe.patchserver

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/poe/test_patchserver.py                              |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Tests for patchserver.py

Agreement
===============================================================================

See PyPoE/LICENSE

TODO
===============================================================================
Testing on live data is difficult, since we can't verify it was downloaded
correctly as the contents of the files may change. Perhaps find a good
candidate for testing.
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
import re
from urllib.error import HTTPError
from socket import socket

# 3rd-party
import pytest

# self
from PyPoE.poe import patchserver
from PyPoE.poe.file import ggpk

# =============================================================================
# Setup
# =============================================================================

_TEST_FILE = 'Data/Wordlists.dat'
_re_version = re.compile(r'[\d]+\.[\d]+\.[\d]+\.[\d]+', re.UNICODE)

def get_node_folders(file):
    dir_paths = []
    parent_dirs = file.rsplit('/', 1)
    if len(parent_dirs) < 2:
        return []
    cdir = ''
    for dirname in parent_dirs[0].split('/'):
        if cdir:
            cdir += '/'
        cdir += dirname
        dir_paths.append(cdir)
    return dir_paths

_TEST_NODE_PATHS = get_node_folders(_TEST_FILE)

# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(scope='module')
def patch():
    return patchserver.Patch()

@pytest.fixture(scope='function')
def patch_temp():
    return patchserver.Patch()

@pytest.fixture(scope='module')
def patch_file_list(patch):
    return patchserver.PatchFileList(patch)

# =============================================================================
# Tests
# =============================================================================

@pytest.mark.dependency(name="test_socket")
def test_socket_fd_open_close(patch_temp):
    test_sock_from_fd = patchserver.socket_fd_open(patch_temp.sock_fd)
    assert isinstance(test_sock_from_fd, socket)
    sock_fd = test_sock_from_fd.detach()
    patchserver.socket_fd_close(sock_fd)

class TestPatch(object):
    def test_dst_file(self, patch, tmpdir):
        patch.download(
            file_path=_TEST_FILE,
            dst_file=os.path.join(str(tmpdir), 'test.txt'),
        )

    def test_dst_dir(self, patch, tmpdir):
        patch.download(
            file_path=_TEST_FILE,
            dst_dir=str(tmpdir),
        )

    def test_missing_dst_error(self, patch):
        with pytest.raises(ValueError):
            patch.download(
                file_path=_TEST_FILE,
            )

    def test_file_not_found(self, patch):
        with pytest.raises(HTTPError):
            patch.download_raw(
                file_path='THIS_SHOULD_NOT_EXIST.FILE',
            )

    def test_version(self, patch):
        assert _re_version.match(patch.version) is not None, 'patch.version ' \
            'result is expected to match the x.x.x.x format'

@pytest.mark.dependency(depends=["test_socket"])
class TestPatchFileList(object):
    @pytest.mark.dependency()
    def test_init(self, patch_file_list):
        assert isinstance(patch_file_list.directory,
                          ggpk.DirectoryNode)
        assert len(patch_file_list.directory.children) > 1

    @pytest.mark.dependency(name="test_updatelist",
                            depends="TestPatchFileList::test_init")
    @pytest.mark.parametrize("node_path",
                             [_TEST_FILE]
                             + _TEST_NODE_PATHS
                             + [_TEST_FILE])
    def test_updatelist(self, patch_file_list, node_path):
        try:
            node = patch_file_list.directory[node_path]
            # if already have metadata for this node,
            # do not redownload
            if node.children:
                return
        except FileNotFoundError:
            with pytest.raises(ValueError):
                # test update_filelist will not query an unknown path
                patch_file_list.update_filelist([node_path])
            return
        # test update_filelist will not query a file
        if isinstance(node.record, ggpk.FileRecord):
            with pytest.raises(ValueError):
                patch_file_list.update_filelist([node_path])
        else:
            patch_file_list.update_filelist([node_path])
        # check that there is a record for the queried node
        assert patch_file_list.directory[node_path].record
