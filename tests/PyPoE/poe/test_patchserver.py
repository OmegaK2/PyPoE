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

_TEST_FILE = 'Redist/brotliLicense.txt'
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

@pytest.fixture(scope='module')
def temp(tmpdir_factory):
    tempdir = tmpdir_factory.mktemp('patchserver')
    return tempdir

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

class TestPatch:
    def test_dst_file(self, patch, tmpdir):
        patch.download(
            file_path=_TEST_FILE,
            dst_file=os.path.join(str(tmpdir), 'test.txt'),
        )

    @pytest.mark.dependency(name="test_download_file")
    def test_dst_dir(self, patch, temp):
        patch.download(
            file_path=_TEST_FILE,
            dst_dir=str(temp),
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
class TestPatchFileList:
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

@pytest.mark.dependency(name="test_node_check_hash",
                        depends=["test_updatelist",
                                 "test_download_file"])
@pytest.mark.parametrize("recurse,node_path", [
    (True, _TEST_FILE),
    (True, _TEST_FILE.rsplit('/', 1)[0]),
    (False, _TEST_FILE.rsplit('/', 1)[0])
])
def test_node_check_hash(temp, patch_file_list, recurse, node_path):
    node = patch_file_list.directory[node_path]
    node_hashes = patchserver.node_check_hash(node,
                                              str(temp),
                                              recurse=recurse)
    if (isinstance(node, ggpk.FileRecord)
            and os.path.exists(os.path.join(str(temp),
                                            node.record.name))):
        assert node_hashes[-1][2] is True
    else:
        if recurse:
            assert len(node_hashes) > len(node.children)
        else:
            assert (len(node_hashes) == (len(node.children)
                                         - len(node.directories)))

@pytest.mark.dependency(name="test_node_outdated_files",
                        depends=["test_node_check_hash"])
@pytest.mark.parametrize("recurse,node_path", [
    (True, _TEST_FILE),
    (False, _TEST_FILE),
    (True, _TEST_FILE + 'BAD'),
    (True, _TEST_NODE_PATHS[-1]),
    (False, _TEST_NODE_PATHS[-1])
    #,(True, _TEST_NODE_PATHS[-2]) #expensive test
])
def test_node_outdated_files(temp, patch_file_list, recurse, node_path):
    # already have metadata, so know what will fail
    try:
        node = patch_file_list.directory[node_path]
    except FileNotFoundError:
        # check that error is raised if node_path not found
        with pytest.raises(ValueError):
            files_needed = patchserver.node_outdated_files(patch_file_list,
                                                           node_path,
                                                           str(temp),
                                                           recurse=recurse)
        return

    temp = temp.join(node_path.rsplit('/', 1)[0])
    # get return values for the tested function
    files_needed_dict = patchserver.node_outdated_files(patch_file_list,
                                                        node_path,
                                                        str(temp),
                                                        recurse=recurse)
    # get list of nodes needed
    files_needed = []
    for needed_node in files_needed_dict.values():
        files_needed = files_needed + needed_node

    # get list of files in a directory node
    files_in_node = []
    # if recursing, walk through sub directories to find files
    if recurse:
        max_depth = -1
    else:
        max_depth = 1
    for walk_node, depth in node.gen_walk(max_depth=max_depth):
        if isinstance(walk_node.record, ggpk.FileRecord):
            files_in_node.append(walk_node)

    # if the previously downloaded test file is one of the files in the
    # directory node being tested, it should match the expected hash
    # then it is expected that it will not be in the needed files
    one_matching_file = (patch_file_list.directory[_TEST_FILE]
                         in files_in_node)
    assert patch_file_list.directory[_TEST_FILE] not in files_needed
    assert len(files_needed) == (len(files_in_node) - one_matching_file)

@pytest.mark.dependency(depends=["test_node_check_hash"])
@pytest.mark.parametrize("recurse,node_path", [
    (False,_TEST_NODE_PATHS[-1])
])
@pytest.mark.skip(reason="expensive test")
def test_node_update_files(patch_file_list, temp, recurse, node_path):
    patchserver.node_update_files(patch_file_list,
                                  node_path,
                                  str(temp),
                                  recurse=recurse)

    node = patch_file_list.directory[node_path]
    if recurse:
        max_depth = -1
    else:
        max_depth = 1
    for walk_node, depth in node.gen_walk(max_depth=max_depth):
        if isinstance(walk_node.record, ggpk.FileRecord):
            assert os.path.exists(os.path.join(str(temp),
                                               node.get_path()))

    files_needed = patchserver.node_outdated_files(patch_file_list,
                                                   node_path,
                                                   str(temp),
                                                   recurse=recurse)
    assert files_needed
