"""


Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | scripts/profile/PyPoE/poe/file/.py                               |
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
from line_profiler import LineProfiler

# self
from PyPoE.poe.file import dat

# =============================================================================
# Globals
# =============================================================================

__all__ = []

dir = 'C:/Temp/'

# =============================================================================
# Classes
# =============================================================================

# =============================================================================
# Functions
# =============================================================================

def read_dat(file_name='GrantedEffects.dat'):
    d = dat.DatFile('GrantedEffects.dat')
    d.read(os.path.join(dir, 'Data', file_name))
    return d

def rr(files=['BaseItemTypes.dat']):
    rr = dat.RelationalReader(path_or_file_system=dir, files=files)



# =============================================================================
# Init
# =============================================================================

if __name__ == '__main__':

    profiler = LineProfiler()
    #profiler.add_function(dat.DatValue.__init__)
    #profiler.add_function(dat.DatReader._cast_from_spec)
    #profiler.add_function(dat.DatReader._process_row)
    #profiler.add_function(dat.DatRecord.__getitem__)

    #profiler.run("d = read_dat()")
    #profiler.run("for i in range(0, 10000): d.reader[0]['Data1']")

    #print(d.reader[0])

    #profiler.add_function(dat.RelationalReader._set_value)
    #profiler.add_function(dat.RelationalReader._dv_set_value)
    #profiler.add_function(dat.RelationalReader._simple_set_value)
    #profiler.add_function(dat.RelationalReader.read_file)
    #profiler.run("rr = dat.RelationalReader(path_or_file_system=dir, files=['Data/BaseItemTypes.dat'], read_options={'use_dat_value': False})")
    #profiler.print_stats()
    rr = dat.RelationalReader(path_or_file_system=dir, files=['Data/MonsterVarieties.dat'], read_options={'use_dat_value': False})