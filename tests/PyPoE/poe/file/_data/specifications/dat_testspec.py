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
# 3rd-party

# self
from PyPoE.poe.file.specification.fields import *

# =============================================================================
# Globals
# =============================================================================

specification = Specification({
    'TestSpec.dat': File(
        fields=(
            Field(
                name='bool',
                type='bool',
            ),
            Field(
                name='byte',
                type='byte',
            ),
            Field(
                name='ubyte',
                type='ubyte',
            ),
            Field(
                name='short',
                type='short',
            ),
            Field(
                name='ushort',
                type='ushort',
            ),
            Field(
                name='int',
                type='int',
            ),
            Field(
                name='uint',
                type='uint',
            ),
            Field(
                name='long',
                type='long',
            ),
            Field(
                name='ulong',
                type='ulong',
            ),
            Field(
                name='ref|string',
                type='ref|string',
            ),
            Field(
                name='ref|list|int',
                type='ref|list|int',
            ),
            Field(
                name='ref|ref|ref|int',
                type='ref|ref|ref|int',
            ),
        ),
    ),
    'Index.dat': File(
        fields=(
            Field(
                name='int',
                type='int',
                unique=True,
            ),
        ),
    ),
    'VirtualFields.dat': File(
        fields=(
            Field(
                name='A',
                type='int',
            ),
            Field(
                name='B',
                type='int',
            ),
            Field(
                name='ListA',
                type='ref|list|int',
            ),
            Field(
                name='ListB',
                type='ref|list|int',
            ),
        ),
        virtual_fields=(
            VirtualField(
                name='CombinedA',
                fields=('A', 'ListA'),
            ),
            VirtualField(
                name='CombinedB',
                fields=('B', 'ListB'),
            ),
            VirtualField(
                name='ZipList',
                fields=('ListA', 'ListB'),
                zip=True,
            ),
            VirtualField(
                name='CombinedVirtual',
                fields=('CombinedA', 'CombinedB'),
            ),
        ),
    ),
    'RelationParent.dat': File(
        fields=(
            Field(
                name='ForeignKey',
                type='ulong',
                key='RelationChild.dat',
            ),
            Field(
                name='ForeignKeyColumn',
                type='int',
                key='RelationChild.dat',
                key_id='UniqueKey',
            ),
        ),
    ),
    'RelationChild.dat': File(
        fields=(
            Field(
                name='UniqueKey',
                type='ulong',
                unique=True,
            ),
            Field(
                name='Data',
                type='int',
            ),
        ),
    ),
})
