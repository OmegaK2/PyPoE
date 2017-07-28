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
    'Main.dat': File(
        fields=OrderedDict((
            ('ForeignKey', Field(
                type='int',
                key='Other.dat',
            )),
            ('ForeignKeyOffset', Field(
                type='int',
                key='Other.dat',
                key_offset=1,
            )),
            ('ForeignKeyMismatch', Field(
                type='int',
            )),
            ('ForeignKeyNone', Field(
                type='int',
                key='Other.dat',
            )),
            ('ForeignKeyCellValue', Field(
                type='int',
                key='Other.dat',
                key_id='Value',
            )),
            ('ConstTest', Field(
                type='int',
                enum='MOD_DOMAIN',
            )),
        )),
    ),
    'Other.dat': File(
        fields=OrderedDict((
            ('Value', Field(
                type='int',
                unique=True,
            )),
        )),
    ),
})
