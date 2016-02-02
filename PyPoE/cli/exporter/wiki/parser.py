"""
Wiki Export Handler

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/wiki/parser.py                                |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Base classes and related functions for Wiki Export Handlers.

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import warnings
import re

# self
from PyPoE.poe.file.dat import RelationalReader
from PyPoE.poe.file.translations import (
    TranslationFileCache,
    MissingIdentifierWarning,
    get_custom_translation_file,
)
from PyPoE.poe.sim.mods import get_translation

# =============================================================================
# Globals
# =============================================================================

__all__ = ['BaseParser']

_inter_wiki_map = (
    #
    # Attibutes
    #
    ('Dexterity', {}),
    ('Intelligence', {}),
    ('Strength', {}),
    #
    # Offense stats
    #
    ('Accuracy Rating', {}),
    ('Accuracy', {}),
    ('Attack Speed', {}),
    ('Cast Speed', {}),
    ('Critical Strike Chance', {}),
    ('Critical Strike Multiplier', {}),
    ('Movement Speed', {}),
    ('Leech', {}), # Life Leech, Mana Leech
    ('Life', {}),
    ('Mana', {}),
    #
    # Damage
    #
    # Base types
    ('Chaos Damage', {}),
    ('Cold Damage', {}),
    ('Fire Damage', {}),
    ('Lightning Damage', {}),
    ('Physical Damage', {}),
    # Mixed and special
    ('Attack Damage', {}),
    ('Spell Damage', {}),
    ('Elemental Damage', {}),
    ('Minion Damage', {}),
    # Just damage
    #('Damage', {}),
    #
    # Defenses
    #
    ('Armour Rating', {}),
    ('Armour', {}),
    ('Energy Shield', {}),
    ('Evasion Rating', {}),
    ('Evasion Rating', {}),
    ('Spell Block', {}),
    ('Block', {}),
    ('Spell Dodge', {}),
    ('Dodge', {}),
    #
    ('Chaos Resistance', {}),
    ('Cold Resistance', {}),
    ('Fire Resistance', {}),
    ('Lightning Resistance', {}),
    ('Elemental Resistance', {}),
    #
    # Buffs
    #

    # Charges
    ('Endurance Charge', {}),
    ('Frenzy Charge', {}),
    ('Power Charge', {}),

    # Friendly
    ('Rampage', {}),

    # Hostile
    ('Corrupted Blood', {}),
    #
    # Skills
    #
    ('Explosive Arrow', {}),
    ('Viper Strike', {}),

    #
    # Misc
    #
    ('Minion', {}),
    ('Mine', {}),
    ('Totem', {}),
    ('Trap', {}),
    ('Dual Wield', {}),
    ('Level', {}),
    ('PvP', {}),
)

_inter_wiki_re = re.compile(
    '|'.join([r'(%s)(?:[\w]*)' % item[0] for item in _inter_wiki_map]),
    re.UNICODE | re.MULTILINE | re.IGNORECASE
)

# =============================================================================
# Classes
# =============================================================================


class BaseParser(object):
    """
    :ivar str base_path:

    :ivar rr:
    :type rr: RelationalReader

    :ivar tc:
    :type tc: TranslationFileCache

    :ivar custom:
    :type custom: TranslationFile
    """

    _DETAILED_FORMAT = '<abbr title="%s">%s</abbr>'
    _HIDDEN_FORMAT = '%s (Hidden)'

    _files = []
    _translations = []

    def __init__(self, base_path):
        self.base_path = base_path

        opt = {
            'use_dat_value': False,
        }

        # Load rr and translations which will be undoubtedly be needed for
        # parsing
        self.rr = RelationalReader(path_or_ggpk=base_path, files=self._files, read_options=opt)
        self.tc = TranslationFileCache(path_or_ggpk=base_path)
        for file_name in self._translations:
            self.tc[file_name]

        self.custom = get_custom_translation_file()

    def _format_hidden(self, custom):
        return self._HIDDEN_FORMAT % make_inter_wiki_links(custom)

    def _format_detailed(self, custom, ingame):
        return self._DETAILED_FORMAT % (
            ingame,
            make_inter_wiki_links(custom)
        )

    def _get_stats(self, mod, translation_file=None):
        result = get_translation(mod, self.tc, translation_file)

        if mod['Domain'] == 3:
            default = self.tc['stat_descriptions.txt'].get_translation(
                result.source_ids, result.source_values, full_result=True
            )

            temp_ids = []
            temp_trans = []

            for i, tr in enumerate(default.found):
                for j, tr2 in enumerate(result.found):
                    if tr.ids != tr2.ids:
                        continue

                    r1 = tr.get_language().get_string(default.values[i], default.indexes[i])[0]
                    r2 = tr2.get_language().get_string(result.values[j], result.indexes[j])[0]
                    if r1 != r2:
                        temp_trans.append(self._format_detailed(r1, r2))
                    elif r2:
                        temp_trans.append(self._format_hidden(r2))
                    temp_ids.append(tr.ids)

                is_missing = True
                for tid in tr.ids:
                    is_missing = is_missing and (tid in result.missing_ids)

                if not is_missing:
                    continue

                r1 = tr.get_language().get_string(default.values[i], default.indexes[i])[0]
                if r1:
                    temp_trans.append(self._HIDDEN_FORMAT % r1)
                    temp_ids.append(tr.ids)

                for tid in tr.ids:
                    i = result.missing_ids.index(tid)
                    del result.missing_ids[i]
                    del result.missing_values[i]

            index = 0
            for i, tr in enumerate(result.found):
                try:
                    index = temp_ids.index(tr.ids)
                except ValueError:
                    temp_ids.insert(index, tr.ids)
                    temp_trans.insert(index, make_inter_wiki_links(
                        tr.get_language().get_string(
                            result.values[i], result.indexes[i]
                        )[0]
                    ))
                else:
                    pass

            out = temp_trans
        else:
            out = [make_inter_wiki_links(line) for line in result.lines]

        if result.missing_ids:
            custom_result = self.custom.get_translation(
                result.missing_ids,
                result.missing_values,
                full_result=True,
            )

            if custom_result.missing_ids:
                warnings.warn(
                    'Missing translation for ids %s and values %s' % (
                        custom_result.missing_ids, custom_result.missing_values),
                    MissingIdentifierWarning,
                )

            for line in custom_result.lines:
                if line:
                    out.append(self._HIDDEN_FORMAT % line)

        finalout = []
        for line in out:
            if '\n' in line:
                finalout.extend(line.split('\n'))
            else:
                finalout.append(line)

        return finalout

# =============================================================================
# Functions
# =============================================================================


def make_inter_wiki_links(string):
    """
    Formats the given string according to the predefined inter wiki formatting
    rules and returns it.

    :param string: String to format
    :type string: str

    :return: String formatted with inter wiki links
    :rtype: str
    """
    out = []

    last_index = 0

    for match in _inter_wiki_re.finditer(string):
        index = match.lastindex
        full = match.group(0)
        short = match.group(index)
        index -= 1

        out.append(string[last_index:match.start()])

        if 'link' not in _inter_wiki_map[index] and short == full:
            out.append('[[%s]]' % full)
        elif 'link' in _inter_wiki_map[index]:
            out.append('[[%s|%s]]' % (_inter_wiki_map[index], full))
        else:
            out.append('[[%s|%s]]' % (short, full))

        last_index = match.end()

    out.append(string[last_index:])

    return ''.join(out)
