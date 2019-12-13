"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | scripts/make_empty_spec.py                                       |
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

Documentation
===============================================================================

Public API
-------------------------------------------------------------------------------

Internal API
-------------------------------------------------------------------------------
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
import struct

# 3rd-party

# self
from PyPoE.poe.constants import VERSION, DISTRIBUTOR
from PyPoE.poe.path import PoEPath
from PyPoE.poe.file import dat
from PyPoE.poe.file.ggpk import GGPKFile

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================

# =============================================================================
# Functions
# =============================================================================


def spec_unknown(size, i=0):
    if size == 0:
        return ''
    spec = "('Unknown%s', Field("
    out = []
    while size >= 4:
        out.append(spec % i)
        out.append("    name='Unknown%s'," % i)
        out.append("    type='int',")
        out.append(")),")
        size -= 4
        i+=1

    mod = size % 4
    for j in range(0, mod):
        out.append(spec % i)
        out.append("    name='Unknown%s'," % i)
        out.append("    type='byte',")
        out.append(")),")
        i+=1

    return ' '*12 + ('\n' + ' '*12).join(out)


def run():
    out = []

    path = PoEPath(version=VERSION.STABLE, distributor=DISTRIBUTOR.GGG
                   ).get_installation_paths()[0]
    dat.set_default_spec(VERSION.STABLE)
    existing_set = set(dat._default_spec.keys())

    ggpk = GGPKFile()
    ggpk.read(os.path.join(path, 'content.ggpk'))
    ggpk.directory_build()

    file_set = set()

    for node in ggpk['Data'].files:
        name = node.record.name
        if not name.endswith('.dat'):
            continue

        # Not a regular dat file, ignore
        if name in ['Languages.dat']:
            continue

        file_set.add(name)

    new = sorted(file_set.difference(set(existing_set)))

    for fn in new:
        binary = ggpk['Data'][fn].record.extract().read()
        data_offset = binary.find(dat.DAT_FILE_MAGIC_NUMBER)
        n_rows = struct.unpack('<I', binary[0:4])[0]
        length = data_offset - 4
        if n_rows > 0:
            record_length = length//n_rows

        out.append("""    '%s': File(
        fields=OrderedDict((
%s
        )),
    ),""" % (fn, spec_unknown(record_length)))

    print('\n'.join(out))


if __name__ == '__main__':
    run()