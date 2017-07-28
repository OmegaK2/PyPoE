"""Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/poe/file/_data/specifications/                       |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Specification used for tests

Agreement
===============================================================================

See PyPoE/LICENSE

"""

# =============================================================================
# Imports
# =============================================================================

# Python
from collections import OrderedDict

# 3rd-party

# self
from PyPoE.poe.file.specification.fields import *

# =============================================================================
# Globals
# =============================================================================

specification = Specification({
    'TestSpec.dat': File(
        fields=OrderedDict((
            ('bool', Field(
                type='bool',
            )),
            ('byte', Field(
                type='byte',
            )),
            ('ubyte', Field(
                type='ubyte',
            )),
            ('short', Field(
                type='short',
            )),
            ('ushort', Field(
                type='ushort',
            )),
            ('int', Field(
                type='int',
            )),
            ('uint', Field(
                type='uint',
            )),
            ('long', Field(
                type='long',
            )),
            ('ulong', Field(
                type='ulong',
            )),
            ('ref|string', Field(
                type='ref|string',
            )),
            ('ref|list|int', Field(
                type='ref|list|int',
            )),
            ('ref|ref|ref|int', Field(
                type='ref|ref|ref|int',
            )),
        )),
    ),
    'Index.dat': File(
        fields=OrderedDict((
            ('int', Field(
                type='int',
                unique=True,
            )),
        )),
    ),
    'VirtualFields.dat': File(
        fields=OrderedDict((
            ('A', Field(
                type='int',
            )),
            ('B', Field(
                type='int',
            )),
            ('ListA', Field(
                type='ref|list|int',
            )),
            ('ListB', Field(
                type='ref|list|int',
            )),
        )),
        virtual_fields=OrderedDict((
            ('CombinedA', VirtualField(
                fields=('A', 'ListA'),
            )),
            ('CombinedB', VirtualField(
                fields=('B', 'ListB'),
            )),
            ('ZipList', VirtualField(
                fields=('ListA', 'ListB'),
                zip=True,
            )),
            ('CombinedVirtual', VirtualField(
                fields=('CombinedA', 'CombinedB'),
            )),
        )),
    ),
    'RelationParent.dat': File(
        fields=OrderedDict((
            ('ForeignKey', Field(
                type='ulong',
                key='RelationChild.dat',
            )),
            ('ForeignKeyColumn', Field(
                type='int',
                key='RelationChild.dat',
                key_id='UniqueKey',
            )),
        )),
    ),
    'RelationChild.dat': File(
        fields=OrderedDict((
            ('UniqueKey', Field(
                type='ulong',
                unique=True,
            )),
            ('Data', Field(
                type='int',
            )),
        )),
    ),
})
