"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | scripts/convert_conf_to_py.py                                    |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Quick and dirty script to convert the spec into python files.

Not maintained, just in case I need it again in the future.

Agreement
===============================================================================

See PyPoE/LICENSE

"""

# =============================================================================
# Imports
# =============================================================================

# Python

# 3rd-party
import configobj

# self

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

classes = {
    'fields': 'Field',
    'virtual_fields': 'VirtualField',
}


def convert_spec(inpath, outpath):
    spec = configobj.ConfigObj(infile=inpath)

    out = ["specification = Specification({"]

    def add_comments(comments, indent):
        if comments:
            for comment in comments:
                out.append(" "*indent + comment.strip())

    for file_key in spec:
        file = spec[file_key]

        add_comments(spec.comments[file_key], 4)
        out.append(" " * 4 + "'%s': File(" % file_key)
        for subsection_key in file:
            subsection = file[subsection_key]
            add_comments(file.comments[subsection_key], 8)
            out.append(" "*8 + "%s=OrderedDict((" % subsection_key)
            for field_key in subsection:
                field = subsection[field_key]
                add_comments(subsection.comments[field_key], 12)

                class_name = classes[subsection_key]
                out.append(" "*12 + "('%s', %s(" % (field_key, class_name))
                for key, value in field.items():
                    add_comments(field.comments[key], 16)
                    if key in ('type', 'key', 'key_id', 'enum', 'file_ext', 'display', 'display_type', 'description'):
                        if isinstance(value, list):
                            value = ', '.join(value)
                        value = value.replace('\n', '').replace("'", '"')
                        value = "'%s'" % value
                    elif key == 'fields':
                        value = "('" + "', '".join(value) + "')"
                    out.append(" "*16 + "%s=%s,%s" % (key, value, field.inline_comments[key] if field.inline_comments[key] else ''))
                out.append(" "*12 + ")),")
            out.append(" "*8 + ")),")
        out.append(" "*4 + "),")

    out.append("})")
    out.append('')
    out.insert(0, '''"""Overview
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
''')

    with open(outpath, 'w') as f:
        f.write('\n'.join(out))


if __name__ == '__main__':
    import os
    path = r'C:\Code\Scripts\PoE\PyPoE\tests\PyPoE\poe\file\_data\specifications'
    for fn in os.listdir(path):
        convert_spec(os.path.join(path, fn), os.path.join('C:/', fn.replace('.ini', '.py')))
