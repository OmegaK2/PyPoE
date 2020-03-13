"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/psg.py                                            |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Support for .psg (Passive Skill Graph) file format.

Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

Public API
-------------------------------------------------------------------------------

API for common and every day use.

.. autoclass:: PSGFile
    :inherited-members:

Internal API
-------------------------------------------------------------------------------

API for internal use, but still may be useful to work with more directly.

.. autoclass:: GraphGroup

.. autoclass:: GraphGroupNode
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import struct
from collections import OrderedDict

# 3rd-party

# self
from PyPoE.shared.mixins import ReprMixin
from PyPoE.poe.file.shared import AbstractFileReadOnly
from PyPoE.poe.file.dat import DatFile, RelationalReader

# =============================================================================
# Globals
# =============================================================================

__all__ = ['PSGFile']

PSG_COL = 'PassiveSkillGraphId'

# =============================================================================
# Classes
# =============================================================================


class GraphGroup(ReprMixin):
    """
    Representation of a group in the passive skill tree graph.

    Groups are a "circle" in the passive at a given position containing all the
    relevant nodes.

    It is possible that a group only contains one node - this is common for the
    highway/pathway nodes.

    Parameters
    ----------
    x :  float
        x coordinate in the passive skill tree
    y :  float
        y coordinate in the passive skill tree
    id :  int
        id (index in list) of the this group
    nodes : list[GraphGroupNode]
        list of child :class:`GraphGroupNode` instances
    flag : bool
        ?
    """

    __slots__ = ['x', 'y', 'id', 'nodes', 'flag']

    _REPR_EXTRA_ATTRIBUTES = OrderedDict((
        ('nodes', None),
    ))

    def __init__(self, x, y, id, flag):
        """
        Parameters
        ----------
        x :  float
            x coordinate in the passive skill tree
        y :  float
            y coordinate in the passive skill tree
        id :  int
            id (index in list) of the this group
        nodes : list[GraphGroupNode]
            list of child :class:`GraphGroupNode` instances
        flag : bool
            ?
        """
        self.x = x
        self.y = y
        self.id = id
        self.nodes = []
        self.flag = flag

    @property
    def point(self):
        """
        Returns a tuple containing the x and y coordinate.

        Returns
        -------
        tuple[int, int]
            Tuple containing the x and y coordinate
        """
        return self.x, self.y

    def _update_connections(self, dat_reader):
        """
        Updates the stored connections using the given dat_reader instance.

        Parameters
        ----------
        dat_reader: DatReader
            :class:`PyPoE.poe.file.dat.DatReader` instance
        """
        for node in self.nodes:
            node._update_connections(dat_reader)


class GraphGroupNode(ReprMixin):
    """
    Representation of a single node in a :class:`GraphGroup`.

    A node contains the actual information about the passive skill value it
    holds and the connection as well the as the position within the group.
    
    .. warning::
        If the parent :class:`PSGFile` was instantiated with a valid
        'PassiveSkills.dat' :class:`PyPoE.poe.file.dat.DatFile` instance, the
        passive_skill and connections variables contain references to the
        respective row (i.e. a `PyPoE.poe.file.dat.DatRecord` instance) instead
        of the integer id.

    Parameters
    ----------
    parent :  GraphGroup
        parent :class:`GraphGroup` this node belongs to

    passive_skill : int or DatRecord
        passive skill node of this node

    radius :  int
        radius from the parent's x,y-position

    position : int
        position of the node in the group; together with the radius this creates
        a clockwise rotation from 0 to 11

    connections : list[int] or list[DatRecord]
        list of passive skill nodes this node is connected to
    """

    __slots__ = ['parent', 'passive_skill', 'radius', 'position', 'connections']

    def __init__(self, parent, passive_skill, radius, position, connections):
        """
        Parameters
        ----------
        parent :  GraphGroup
            parent :class:`GraphGroup` this node belongs to
        passive_skill :  int
            passive skill node id of this node
        radius :  int
            radius from the parent's x,y-position
        position :  int
            position of the node in the group; together with the radius this 
            creates a clockwise rotation from 0 to 11
        connections : list[int]
            list of passive skill nodes ids this node is connected to
        """
        self.parent = parent
        self.passive_skill = passive_skill
        self.radius = radius
        self.position = position
        self.connections = connections

    def _update_connections(self, dat_reader):
        """
        Updates the stored connections using the given dat_reader instance.

        Parameters
        ----------
        dat_reader:  DatReader
            :class:`PyPoE.poe.file.dat.DatReader` instance
        """
        self.passive_skill = dat_reader.index[PSG_COL][
            self.passive_skill
        ]
        for i, connection in enumerate(self.connections):
            self.connections[i] = dat_reader.index[PSG_COL][
                connection
            ]


class PSGFile(AbstractFileReadOnly):
    """
    Representation of a .psg (Passive Skill Tree Graph) file.
    
    Parameters
    ----------
    _passive_skills : None or DatReader
        reference to the :class:`PyPoE.poe.file.dat.DatReader` if specified
    root_passives : list[int] or list[DatRecord]
        list of root (starting class) passive nodes
    groups : list[GraphGroup]
        list of :class:`GraphGroup` instances
    """

    EXTENSION = '.psg'

    def __init__(self, passive_skills_dat_file=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.root_passives = []
        self.groups = []

        if isinstance(passive_skills_dat_file, DatFile):
            #TODO check whether is read and raise exception
            self._passive_skills = passive_skills_dat_file.reader
        elif isinstance(passive_skills_dat_file, RelationalReader):
            self._passive_skills = passive_skills_dat_file.get_file(
                'Data/PassiveSkills.dat'
            ).reader
        elif passive_skills_dat_file is None:
            self._passive_skills = passive_skills_dat_file
        else:
            raise ValueError(
                'passive_skills_dat_file must be a DatFile instance, a '
                'RelationalReader instance or None'
            )

        if self._passive_skills:
            self._passive_skills.build_index('PassiveSkillGraphId')

    def _read(self, buffer, *args, **kwargs):
        data = buffer.read()
        offset = 0

        # version?
        version = struct.unpack_from('<B', data, offset=offset)[0]
        offset += 1

        unknown_length = struct.unpack_from('<B', data, offset=offset)[0]
        offset += 1

        unknown = struct.unpack_from(
            '<' + 'B'*unknown_length, data, offset=offset
        )
        offset += 1*unknown_length

        root_length = struct.unpack_from('<I', data, offset=offset)[0]
        offset += 4

        self.root_passives = list(struct.unpack_from(
            '<' + 'I'*root_length, data, offset=offset
        ))
        offset += 4*root_length

        group_length = struct.unpack_from('<I', data, offset=offset)[0]
        offset += 4

        self.groups = []
        for i in range(0, group_length):
            x, y, flag, passive_length = struct.unpack_from(
                '<ffbI', data, offset=offset
            )
            offset += 4*2+4+1

            group = GraphGroup(x=x, y=y, id=len(self.groups), flag=flag)

            for j in range(0, passive_length):
                rowid, radius, position, connections_length = struct.unpack_from(
                    '<IIII', data, offset=offset
                )
                offset += 4*4

                connections = struct.unpack_from(
                    '<' + 'I'*connections_length, data, offset=offset
                )
                offset += 4*connections_length

                group.nodes.append(
                    GraphGroupNode(
                        parent=group,
                        passive_skill=rowid,
                        radius=radius,
                        position=position,
                        connections=list(connections),
                    )
                )

            self.groups.append(group)

        # Done parsing, finalize the connections if the dat file is specified
        if self._passive_skills is not None:
            for i, psg_id in enumerate(self.root_passives):
                self.root_passives[i] = self._passive_skills.index[PSG_COL][psg_id]

            for group in self.groups:
                group._update_connections(self._passive_skills)

    @property
    def is_read(self):
        return bool(self.groups)

    @property
    def passive_skills_dat_file(self):
        return self._passive_skills


# =============================================================================
# Functions
# =============================================================================

if __name__ == '__main__':
    psg = PSGFile()
    psg.read('C:/Temp/Metadata/PassiveSkillGraph.psg')