"""


Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | scripts/profile/PyPoE/poe/file/ot.py                             |
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
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os

# 3rd-party
import line_profiler

# self
from PyPoE.poe.file.shared.keyvalues import *
from PyPoE.poe.file.ot import OTFile

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

# =============================================================================
# Init
# =============================================================================

if __name__ == '__main__':
    profiler = line_profiler.LineProfiler()
    profiler.add_function(AbstractKeyValueFile._read)
    profiler.add_function(AbstractKeyValueFile.__missing__)

    def run():
        f = 'C:/Temp/'
        sections = set()
        for path, dirnames, filenames in os.walk(f):
            for filename in filenames:
                if not filename.endswith('.ot'):
                    continue

                ot = OTFile(parent_or_base_dir_or_ggpk=f)
                ot.read(os.path.join(path, filename))
                for k in ot.keys():
                    sections.add(k)

        sections = list(sections)
        sections.sort()
        print(sections)


    profiler.run('run()')

    #ot = OTFile(parent_or_base_dir_or_ggpk=f)
    #ot.read('C:\Temp\Metadata\Items\Armours\BodyArmours\AbstractBodyArmour.ot')
    #print(ot.keys())

    profiler.print_stats()