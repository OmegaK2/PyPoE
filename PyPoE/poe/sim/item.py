"""
Utilities for dealing with items

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/sim/item.py                                            |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Utilities for dealing with items.

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE

Todo
-------
ValueError -> ParserError?
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
from enum import Enum

# 3rd-party

# self
from PyPoE.poe.constants import RARITY, SOCKET_COLOUR
from PyPoE.poe.file.dat import RelationalReader

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Functions
# =============================================================================


def _regex_build_single_re(k, v):
    if 're' in v:
        return r'%s: (?P<%s>.*)$' % (v['re'], k)
    elif 're2' in v:
        return v['re2']


def _regex_update_singular_dict(singular_dict):
    for k, v in singular_dict.items():
        v['re_compiled'] = re.compile(_regex_build_single_re(k, v), re.UNICODE)


def _regex_build_from_handler_dict(handler_dict):
    conditionals = []
    for k, v in handler_dict.items():
        conditionals.append(_regex_build_single_re(k, v))

    return re.compile('|'.join(conditionals), re.MULTILINE | re.UNICODE)

# =============================================================================
# Classes
# =============================================================================


class ITEM_TYPES(Enum):
    ITEM = 0
    GEM = 1
    CURRENCY = 2


class ItemSocket(object):
    """

    :ivar index:
    :type index: int

    :ivar colour:
    :type colour: SOCKET_COLOUR
    """

    __slots__ = ('index', 'colour')

    def __init__(self, index, colour):
        self.index = index
        self.colour = colour

    def __repr__(self):
        return 'ItemSocket(%s, %s)' % (self.index, repr(self.colour))

    def __eq__(self, other):
        if not isinstance(other, ItemSocket):
            return False

        return self.index == other.index and self.colour == other.colour


class ItemParser(object):
    """
    Class to parse/handle the string provided by items when using CTRL-C on
    items in game.
    """
    _re_split = re.compile(
        r'^\-{8}$',
        re.UNICODE | re.MULTILINE
    )

    _re_split_newline = re.compile(
        '(?:(?:\r|)\n)',
        re.UNICODE
    )

    _re_replace = re.compile(
        r' \((augmented|unmet)\)',
        re.UNICODE
    )

    _re_rarity =  re.compile(
        r'^Rarity: (?P<rarity>.*)$',
        re.UNICODE | re.MULTILINE
    )

    _stat_handlers = {
        ITEM_TYPES.ITEM: {
            'map_tier': {
                're': 'Map Tier',
                'func': int,
            },
            'item_quantity': {
                're': 'Item Quantity',
                'func': lambda s: int(s.strip('%')),
            },
            'item_rarity': {
                're': 'Item Rarity',
                'func': lambda s: int(s.strip('%')),
            },
            'pack_size': {
                're': 'Monster Pack Size',
                'func': lambda s: int(s.strip('%')),
            },
            'quality': {
                're': 'Quality',
                'func': lambda s: int(s.strip('%')),
            },
            'armour': {
                're': 'Armour',
                'func': int,
            },
            'evasion': {
                're': 'Evasion Rating',
                'func': int,
            },
            'energy_shield': {
                're': 'Energy Shield',
                'func': int,
            },
            'physical_damage': {
                're': 'Physical Damage',
                'func': lambda s: [int(s2) for s2 in s.split('-')],
            },
            'elemental_damage': {
                're': 'Elemental Damage',
                'func': lambda s: [
                    [int(s3) for s3 in s2.split('-')] for s2 in s.split(', ')
                ],
            },
            'chaos_damage': {
                're': 'Chaos Damage',
                'func': lambda s: [int(s2) for s2 in s.split('-')],
            },
            'critical_strike_chance': {
                're': 'Critical Strike Chance',
                'func': lambda s: float(s.strip('%')),
            },
            'attacks_per_second': {
                're': 'Attacks per Second',
                'func': lambda s: float(s),
            },
            'item_class': {
                're2': r'^(?P<item_class>[^:]+)$',
                'func': lambda s: s,
            },
        },
        ITEM_TYPES.GEM: {
            'gem_level': {
                're': 'Level',
                'func': int,
            },
            'mana_cost': {
                're': 'Mana Cost',
                'func': int,
            },
            'mana_reserved': {
                're': 'Mana Reserved',
                'func': lambda s: int(s.strip('%')),
            },
            'mana_multiplier': {
                're': 'Mana Multiplier',
                'func': lambda s: int(s.strip('%')),
            },
            'souls_per_use': {
                're': 'Souls Per Use',
                'func': int,
            },
            'stored_uses': {
                're2': r'^Can Store (?P<stored_uses>[0-9]+) Use(?:|s)$',
                'func': int,
            },
            'cooldown_time': {
                're': 'Cooldown Time',
                'func': lambda s: float(s.strip(' sec')),
            },
            'cast_time': {
                're': 'Cast Time',
                'func': lambda s: float(s.strip(' sec')),
            },
            'critical_strike_chance': {
                're': 'Critical Strike Chance',
                'func': lambda s: float(s.strip('%')),
            },
            'damage_effectiveness': {
                're': 'Damage Effectiveness',
                'func': lambda s: int(s.strip('%')) / 100,
            },
            'quality': {
                're': 'Quality',
                'func': lambda s: int(s.strip('%')),
            },
            'experience': {
                're': 'Experience',
                'func': lambda s: [int(s2.replace('.', '')) for s2 in s.split('/')],
            }
        },
        ITEM_TYPES.CURRENCY: {
            'stack_size': {
                're': 'Stack Size',
                'func': lambda s: [int(s2) for s2 in s.split('/')],
            },
        },
    }

    _re_stat_handlers = {
        ITEM_TYPES.ITEM: _regex_build_from_handler_dict(
            _stat_handlers[ITEM_TYPES.ITEM]
        ),
        ITEM_TYPES.GEM: _regex_build_from_handler_dict(
            _stat_handlers[ITEM_TYPES.GEM]
        ),
        ITEM_TYPES.CURRENCY: _regex_build_from_handler_dict(
            _stat_handlers[ITEM_TYPES.CURRENCY]
        ),
    }

    _requirement_handlers = {
        'required_level': {
            're': 'Level',
            'func': int,
        },
        'required_str': {
            're': 'Str',
            'func': int,
        },
        'required_dex': {
            're': 'Dex',
            'func': int,
        },
        'required_int': {
            're': 'Int',
            'func': int,
        },
    }

    _re_requirement_handlers = _regex_build_from_handler_dict(_requirement_handlers)

    _re_requirement = re.compile(
        '^Requirements:',
        # No multi line, match start of section
        re.UNICODE
    )

    # Uses similar syntax, but is built for each value separately
    _re_singular = {
        'limit': {
            're': 'Limited to',
            'func': int,
        },
        'item_level': {
            're': 'Item Level',
            'func': int,
        },

        'gem_tags': {
            're2': r'^(?P<gem_tags>[^:]+)$',
            'func': lambda s: s.split(', '),
        },
    }
    _regex_update_singular_dict(_re_singular)

    _re_sockets = _re_sockets_split = re.compile(
        r'^Sockets: (?P<sockets>.+)$',
        re.UNICODE
    )

    _re_sockets_split = re.compile(
        '( |-)',
        re.UNICODE
    )

    _re_help_text_item_name = re.compile(
        '(Jewel|Map)',
        re.UNICODE
    )

    _re_is_map = re.compile(
        '('
        'Map'
        ')',
        re.UNICODE
    )

    _re_is_vaal_fragment = re.compile(
        '('
        'Sacrifice at (Dawn|Midnight|Noon|Dusk)|'
        'Mortal (Rage|Hope|Ignorance|Grief)'
        ')',
        re.UNICODE
    )

    _re_is_jewel = re.compile(
        '('
        '(Viridian|Cobalt|Crimson) Jewel'
        ')',
        re.UNICODE
    )

    _re_prefix = re.compile(
        '^(?P<prefix>[\S]+) .+$',
        re.UNICODE,
    )

    _re_suffix = re.compile(
        '^.+ (?P<suffix>of [\S]+)$',
        re.UNICODE,
    )

    def __init__(self, item_info_string):
        """
        :param item_info_string:
        :type item_info_string: str

        :param relational_reader:
        :type relational_reader: RelationalReader
        """
        self._type = None

        sections = self._re_split.split(item_info_string)
        if not sections:
            raise ValueError('No description sections found - malformed input?')

        current_sec = -len(sections)

        def increment_sec(value=True):
            # Python 3 is neat
            nonlocal current_sec
            if value:
                current_sec += 1

        def section(index=None, offset=0):
            return sections[index or (current_sec+offset)].strip('\r\n')

        # Header section
        header = self._split(section())

        self.base_item_name = header[-1]
        if len(header) == 3:
            self.name = header[1]
        elif len(header) in (1, 2):
            self.name = header[-1]
        else:
            raise ValueError('Header section is of unsupported length: %s' %
                             len(header))

        self.name = self.name

        if len(header) != 1:
            rarity = self._re_rarity.match(header[0])
            if rarity is None:
                raise ValueError('No rarity found in the item header')

            rarity = rarity.group('rarity')
            for rarity_const in RARITY:
                if rarity_const.name_upper == rarity:
                    self.rarity = rarity_const
                    self._type = ITEM_TYPES.ITEM
                    break

            if self._type is None:
                if rarity == 'Gem':
                    self._type = ITEM_TYPES.GEM
                elif rarity == 'Currency':
                    self._type = ITEM_TYPES.CURRENCY
                else:
                    raise ValueError('Unsupported value for "Rarity": %s' % rarity)
            elif self.rarity == RARITY.MAGIC:
                self.prefix = None
                self.suffix = None

                match = self._re_suffix.match(self.base_item_name)
                if match:
                    self.suffix = match.group('suffix')
                    self.base_item_name = self.base_item_name.replace(' ' + self.suffix, '')

                # Can't reliably detect the prefix yet. Will have to do based on
                # stats
        else:
            # case for MTX items
            self._type = ITEM_TYPES.CURRENCY

        is_map = self._re_is_map.search(self.base_item_name)
        is_jewel = self._re_is_jewel.search(self.base_item_name)
        is_vaal_fragment = self._re_is_vaal_fragment.search(self.base_item_name)

        increment_sec()

        # Base stats sections (not from mods)
        next = section()
        if self._type == ITEM_TYPES.GEM:
            next = self._re_split_newline.split(next, 1)
            self._handle_singular(next[0], 'gem_tags')
            next = next[1]

        if self._type in self._stat_handlers:
            increment_sec(
                self._handle_handlers(
                    next,
                    self._re_stat_handlers[self._type],
                    self._stat_handlers[self._type]
                )
            )

        # Requirements section
        if self._re_requirement.match(section()):
            increment_sec(
                self._handle_handlers(
                    section(),
                    self._re_requirement_handlers,
                    self._requirement_handlers,
                )
            )

        # Sockets section
        match = self._re_sockets.match(section())
        if match:
            self.sockets = []
            self.links = []
            last_linked = False
            for i, char in enumerate(
                    self._re_sockets_split.split(match.group('sockets'))
            ):
                if i % 2 == 0:
                    found = False
                    for socket_colour in SOCKET_COLOUR:
                        if socket_colour.char == char:
                            found = True
                            break

                    if not found:
                        raise ValueError('Unsupported socket colour: %s' % char)

                    self.sockets.append(ItemSocket(i//2, socket_colour))

                    if last_linked:
                        self.links[-1].append(self.sockets[-1])
                else:
                    if char == ' ':
                        # No links
                        last_linked = False
                    elif char == '-':
                        if not last_linked:
                            self.links.append([self.sockets[-1], ])
                        last_linked = True
                    else:
                        raise ValueError('Unsupported link character: %s' % char)
            increment_sec()
        else:
            self.sockets = None
            self.links = None

        # Limited to section
        increment_sec(self._handle_singular(section(), 'limit'))

        # Item level section
        increment_sec(self._handle_singular(section(), 'item_level'))

        # Stack size
        #if self._type == ITEM_TYPES.CURRENCY:
        #    increment_sec(self._handle_singular(section(), 'stack_size'))

        # stats, flavour text and help text would be here.
        # Below this point we're going backwards

        # Corrupted section
        last_sec = -1
        if section(index=last_sec) == 'Corrupted':
            last_sec -= 1
            self.is_corrupted = True
        else:
            self.is_corrupted = False

        # Help text
        if self._type in (ITEM_TYPES.GEM, ITEM_TYPES.CURRENCY) or is_jewel or is_map or is_vaal_fragment:
            self.help_text = section(index=last_sec)
            last_sec -= 1

        # Flavour text
        if (self._type == ITEM_TYPES.ITEM and self.rarity == RARITY.UNIQUE) or is_vaal_fragment:
            self.flavour_text = section(index=last_sec)
            # Unidentified uniques don't have a flavour text, I think setting
            # "Unidentifed" is appropriate, but still have to make sure not to
            # adjust the pointer so stats parsing works.
            if self.flavour_text != 'Unidentified':
                last_sec -= 1

        # Implicit section & stats section
        # We should be left at between 0 or 2 sections
        remaining = abs((last_sec + 1) - current_sec)
        if self._type == ITEM_TYPES.ITEM:
            if remaining == 0:
                self.implicit_stats = []
                self.stats = []
            elif remaining == 2:
                self.implicit_stats = self._re_split_newline.split(section())
                self.stats = self._re_split_newline.split(section(offset=1))
            elif remaining == 1:
                # Normal items can't have explicit stats
                if self.rarity == RARITY.NORMAL:
                    self.implicit_stats = self._re_split_newline.split(section())
                    self.stats = []
                # And magic/rare/unique items MUST have stats
                else:
                    self.implicit_stats = []
                    self.stats = self._re_split_newline.split(section())
            else:
                raise ValueError('Too many sections (%s) left for item stat parsing.' % remaining)
        elif self._type == ITEM_TYPES.GEM:
            if remaining == 0:
                self.stats = []
            elif remaining == 1:
                self.stats = self._re_split_newline.split(section())
            else:
                raise ValueError('Too many sections (%s) left for gem stat parsing.' % remaining)
        elif self._type == ITEM_TYPES.CURRENCY and remaining:
            if remaining == 1:
                self.description = section()
            else:
                raise ValueError('All sections (%s) should be parsed now.' % remaining)

        # Do a final pass on the prefix for magic items
        if self._type == ITEM_TYPES.ITEM and self.rarity == RARITY.MAGIC and ((self.suffix is None and len(self.stats) >= 1) or (self.suffix is not None and len(self.stats) >= 2)):
            match = self._re_prefix.match(self.base_item_name)
            self.prefix = match.group('prefix')
            self.base_item_name = self.base_item_name.replace(self.prefix + ' ', '')

    def _split(self, section):
        return self._re_split_newline.split(section)

    def _handle_singular(self, string, key):
        match = self._re_singular[key]['re_compiled'].match(string)
        if match:
            setattr(self, key, self._re_singular[key]['func'](match.group(key)))
            return True

        setattr(self, key, None)
        return False

    def _handle_handlers(self, string, regex, handlers):
        for k in handlers:
            setattr(self, k, None)

        found = False
        for match in regex.finditer(string):
            found = True
            setattr(
                self,
                match.lastgroup,
                handlers[match.lastgroup]['func'](
                    self._re_replace.sub('', match.group(match.lastgroup))
                )
            )

        return found