"""
.ot File Format

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/ot.py                                             |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

.ot file seem to be generally used for server-side settings related to abstract
objects.

Generally make sure to consider the context of the file when interpreting the
contents; there is a chance they're extended or embedded though .dat files and
the key/value pairs found are in relevance to the context.

Usually they're accompanied by .otc files which handle client-side settings.


Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE


See also
-------------------------------------------------------------------------------
* :ref:`PyPoE.poe.file.otc`
* :ref:`PyPoE.poe.file.dat`
"""

# =============================================================================
# Imports
# =============================================================================

# Python

# 3rd-party

# self
from PyPoE.poe.file.shared.keyvalues import (
    AbstractKeyValueSection, AbstractKeyValueFile
)

# =============================================================================
# Globals
# =============================================================================

__all__ = ['OTFile']

# =============================================================================
# Classes
# =============================================================================


class ActionKeyValueSection(AbstractKeyValueSection):
    NAME = 'Actor'
    '''OVERRIDE_KEYS = [
        'actor',
        'armour_surface_type',
        'basic_action',
        'off_hand_unarmed_type',
        'main_hand_unarmed_type'
    ]'''
    OVERRIDE_WARNING = False


class AnimatedKeyValueSection(AbstractKeyValueSection):
    NAME = 'Animated'
    # I think this is safe to assume
    OVERRIDE_WARNING = False


class BaseKeyValueSection(AbstractKeyValueSection):
    NAME = 'Base'
    APPEND_KEYS = ['tag']
    OVERRIDE_KEYS = ['description_text']


class ModsKeyValueSection(AbstractKeyValueSection):
    NAME = 'Mods'
    APPEND_KEYS = ['enable_rarity']


class PathfindingKeyValueSection(AbstractKeyValueSection):
    NAME = 'Pathfinding'
    #OVERRIDE_KEYS = ['base_speed']
    OVERRIDE_WARNING = False


class PositionedKeyValueSection(AbstractKeyValueSection):
    NAME = 'Positioned'
    OVERRIDE_WARNING = False


class SocketsKeyValueSection(AbstractKeyValueSection):
    NAME = 'Sockets'
    OVERRIDE_KEYS = ['socket_info']


class StatsKeyValueSection(AbstractKeyValueSection):
    NAME = 'Stats'
    OVERRIDE_WARNING = False


class OTFile(AbstractKeyValueFile):
    """
    Representation of a .dat file.
    """

    SECTIONS = dict((s.NAME, s) for s in [
        ActionKeyValueSection,
        AnimatedKeyValueSection,
        BaseKeyValueSection,
        ModsKeyValueSection,
        PathfindingKeyValueSection,
        PositionedKeyValueSection,
        SocketsKeyValueSection,
        StatsKeyValueSection,
    ])

    EXTENSION = '.ot'

    def __init__(self, *args, **kwargs):
        super(OTFile, self).__init__(*args, **kwargs)


# =============================================================================
# Functions
# =============================================================================


if __name__ == '__main__':
    import os

    import line_profiler
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