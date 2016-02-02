"""


Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | translations.py                                                |
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

# 3rd-party
from line_profiler import LineProfiler

# self
from PyPoE.poe.file import translations

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
    profiler = LineProfiler()

    #profiler.add_function(translations.TranslationFile.get_translation)
    #profiler.add_function(translations.TranslationFile._read)
    profiler.add_function(translations.TranslationString._set_string)
    #profiler.add_function(translations.Translation.get_language)
    #profiler.add_function(translations.TranslationQuantifier.handle)
    #profiler.add_function(translations.TranslationRange.in_range)
    #profiler.add_function(translations.TranslationLanguage.get_string)

    profiler.run("s = translations.TranslationFile('C:/Temp/MetaData/stat_descriptions.txt')")
    profiler.run("for i in range(0, 100): t = s.get_translation(tags=['additional_chance_to_take_critical_strike_%', 'additional_chance_to_take_critical_strike_%'], values=((3, 5), 6))")

    profiler.print_stats()

    print('translations.Translation:', t)