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
from PyPoE.poe.constants import MOD_DOMAIN
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
    ('Critical Strike', {}),
    ('Movement Speed', {}),
    ('Leech', {}), # Life Leech, Mana Leech
    ('Life', {}),
    ('Mana Reservation', {}),
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
    # Items
    #


    #
    # Skills
    #
    ('Abyssal Cry', {}),
    ('Ancestral Protector', {}),
    ('Anger', {}),
    ('Animate(?:|d) Guardian', {'link': 'Animate Guardian'}),
    ('Animate(?:|d) Weapon', {'link': 'Animate Weapon'}),
    ('Arc ', {'link': 'Arc'}),
    ('Arctic Armour', {}),
    ('Arctic Breath', {}),
    ('Assassin\'s Mark', {}),
    ('Ball Lightning', {}),
    ('Barrage', {}),
    ('Bear Trap', {}),
    ('Blade Trap', {}),
    ('Blade Vortex', {}),
    ('Bladefall', {}),
    ('Blast Rain', {}),
    ('Blight', {}),
    ('Blink Arrow', {}),
    ('Blood Rage', {}),
    ('Bone Offering', {}),
    ('Burning Arrow', {}),
    ('Caustic Arrow', {}),
    ('Clarity', {}),
    ('Cleave', {}),
    ('Cold Snap', {}),
    ('Conductivity', {}),
    ('Contagion', {}),
    ('Conversion Trap', {}),
    ('Convocation', {}),
    ('Cyclone', {}),
    ('Damage Infusion', {}),
    ('Decoy Totem', {}),
    ('Desecrate', {}),
    ('Determination', {}),
    ('Detonate Dead', {}),
    ('Detonate Mines', {}),
    ('Devouring Totem', {}),
    ('Discharge', {}),
    ('Discipline', {}),
    ('Dominating Blow', {}),
    ('Doom Arrow', {}),
    ('Double Strike', {}),
    ('Dual Strike', {}),
    ('Earthquake', {}),
    ('Elemental Hit', {}),
    ('Elemental Weakness', {}),
    ('Enduring Cry', {}),
    ('Energy Beam', {}),
    ('Enfeeble', {}),
    ('Essence Drain', {}),
    ('Ethereal Knives', {}),
    ('Explosive Arrow', {}),
    ('Fire Nova Mine', {}),
    ('Fire Trap', {}),
    ('Fire Weapon', {}),
    ('Fireball', {}),
    ('Firestorm', {}),
    ('Flame Dash', {}),
    ('Flame Surge', {}),
    ('Flame Totem', {}),
    ('Flameblast', {}),
    ('Flammability', {}),
    ('Flesh Offering', {}),
    ('Flicker Strike', {}),
    ('Freeze Mine', {}),
    ('Freezing Pulse', {}),
    ('Frenzy', {}),
    ('Frost Blades', {}),
    ('Frost Bomb', {}),
    ('Frost Wall', {}),
    ('Frostbite', {}),
    ('Glacial Cascade', {}),
    ('Glacial Hammer', {}),
    ('Grace', {}),
    ('Ground Slam', {}),
    ('Haste', {}),
    ('Hatred', {}),
    ('Heavy Strike', {}),
    ('Herald of Ash', {}),
    ('Herald of Blood', {}),
    ('Herald of Ice', {}),
    ('Herald of Thunder', {}),
    ('Ice Crash', {}),
    ('Ice Nova', {}),
    ('Ice Shot', {}),
    ('Ice Spear', {}),
    ('Ice Trap', {}),
    ('Ignite', {}),
    ('Immortal Call', {}),
    ('Incinerate', {}),
    ('Infernal Blow', {}),
    ('Kinetic Blast', {}),
    ('Leap Slam', {}),
    ('Lightning Arrow', {}),
    ('Lightning Channel', {}),
    ('Lightning Circle', {}),
    ('Lightning Strike', {}),
    ('Lightning Tendrils', {}),
    ('Lightning Trap', {}),
    ('Lightning Warp', {}),
    ('Magma Orb', {}),
    ('Mirror Arrow', {}),
    ('Molten Shell', {}),
    ('Molten Strike', {}),
    ('Orb of Storms', {}),
    ('Phase Run', {}),
    ('Poacher\'s Mark', {}),
    ('Portal', {}),
    ('Power Siphon', {}),
    ('Projectile Weakness', {}),
    ('Puncture', {}),
    ('Punishment', {}),
    ('Purity of Elements', {}),
    ('Purity of Fire', {}),
    ('Purity of Ice', {}),
    ('Purity of Lightning', {}),
    ('Rain of Arrows', {}),
    ('Raise Spectre', {}),
    ('Raise Zombie', {}),
    ('Rallying Cry', {}),
    ('Reave', {}),
    ('Reckoning', {}),
    ('Rejuvenation Totem', {}),
    ('Righteous Fire', {}),
    ('Righteous Lightning', {}),
    ('Riposte', {}),
    ('Searing Bond', {}),
    ('Shadow Blades', {}),
    ('Shield Charge', {}),
    ('Shock Nova', {}),
    ('Shockwave Totem', {}),
    ('Shrapnel Shot', {}),
    ('Siege Ballista', {}),
    ('Smoke Mine', {}),
    ('Spark', {}),
    ('Spectral Throw', {}),
    ('Split Arrow', {}),
    ('Static Strike', {}),
    ('Static Tether', {}),
    ('Storm Call', {}),
    ('Summon Chaos Golem', {}),
    ('Summon Flame Golem', {}),
    ('Summon Ice Golem', {}),
    ('Summon Lightning Golem', {}),
    ('Summon Raging Spirit', {}),
    ('Summon Skeletons', {}),
    ('Summon Stone Golem', {}),
    ('Sunder', {}),
    ('Sweep', {}),
    ('Tempest Shield', {}),
    ('Temporal Chains', {}),
    ('Tornado Shot', {}),
    ('Vaal Arc', {}),
    ('Vaal Burning Arrow', {}),
    ('Vaal Clarity', {}),
    ('Vaal Cold Snap', {}),
    ('Vaal Cyclone', {}),
    ('Vaal Detonate Dead', {}),
    ('Vaal Discipline', {}),
    ('Vaal Double Strike', {}),
    ('Vaal FireTrap', {}),
    ('Vaal Fireball', {}),
    ('Vaal Flameblast', {}),
    ('Vaal Glacial Hammer', {}),
    ('Vaal Grace', {}),
    ('Vaal Ground Slam', {}),
    ('Vaal Haste', {}),
    ('Vaal Heavy Strike', {}),
    ('Vaal Ice Nova', {}),
    ('Vaal Immortal Call', {}),
    ('Vaal Lightning Strike', {}),
    ('Vaal Lightning Trap', {}),
    ('Vaal Lightning Warp', {}),
    ('Vaal Molten Shell', {}),
    ('Vaal Power Siphon', {}),
    ('Vaal Rain of Arrows', {}),
    ('Vaal Reave', {}),
    ('Vaal Righteous Fire', {}),
    ('Vaal Spark', {}),
    ('Vaal Spectral Throw', {}),
    ('Vaal Storm Call', {}),
    ('Vaal Summon Skeletons', {}),
    ('Vaal Sweep', {}),
    ('Vengeance', {}),
    ('Vigilant Strike', {}),
    ('Viper Strike', {}),
    ('Vitality', {}),
    ('Vulnerability', {}),
    ('Warlord\'s Mark', {}),
    ('Whirling Blades', {}),
    ('Wild Strike', {}),
    ('Wither', {}),
    ('Wrath', {}),
    #
    # Enchantment skills
    #
    ('Commandment of Blades', {}),
    ('Commandment of Flames', {}),
    ('Commandment of Force', {}),
    ('Commandment of Frost', {}),
    ('Commandment of Fury', {}),
    ('Commandment of Inferno', {}),
    ('Commandment of Ire', {}),
    ('Commandment of Light', {}),
    ('Commandment of Reflection', {}),
    ('Commandment of Spite', {}),
    ('Commandment of Thunder', {}),
    ('Commandment of War', {}),
    ('Commandment of Winter', {}),
    ('Commandment of the Grave', {}),
    ('Commandment of the Tempest', {}),
    ('Decree of Blades', {}),
    ('Decree of Flames', {}),
    ('Decree of Force', {}),
    ('Decree of Frost', {}),
    ('Decree of Fury', {}),
    ('Decree of Inferno', {}),
    ('Decree of Ire', {}),
    ('Decree of Light', {}),
    ('Decree of Reflection', {}),
    ('Decree of Spite', {}),
    ('Decree of Thunder', {}),
    ('Decree of War', {}),
    ('Decree of Winter', {}),
    ('Decree of the Grave', {}),
    ('Decree of the Tempest', {}),
    ('Edict of Blades', {}),
    ('Edict of Flames', {}),
    ('Edict of Force', {}),
    ('Edict of Frost', {}),
    ('Edict of Fury', {}),
    ('Edict of Inferno', {}),
    ('Edict of Ire', {}),
    ('Edict of Light', {}),
    ('Edict of Reflection', {}),
    ('Edict of Spite', {}),
    ('Edict of Thunder', {}),
    ('Edict of War', {}),
    ('Edict of Winter', {}),
    ('Edict of the Grave', {}),
    ('Edict of the Tempest', {}),
    ('Word of Blades', {}),
    ('Word of Flames', {}),
    ('Word of Force', {}),
    ('Word of Frost', {}),
    ('Word of Fury', {}),
    ('Word of Inferno', {}),
    ('Word of Ire', {}),
    ('Word of Light', {}),
    ('Word of Reflection', {}),
    ('Word of Spite', {}),
    ('Word of Thunder', {}),
    ('Word of War', {}),
    ('Word of Winter', {}),
    ('Word of the Grave', {}),
    ('Word of the Tempest', {}),

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
    ('Hit', {}),
    ('Kill', {}),
    ('Charge', {}),
)

_inter_wiki_re = re.compile(
    r'(?P<short>%s)(?:[\w]*)' % '|'.join([item[0] for item in _inter_wiki_map]),
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
            'auto_build_index': True,
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

        if mod['Domain'] == MOD_DOMAIN.MONSTER:
            default = self.tc['stat_descriptions.txt'].get_translation(
                result.source_ids, result.source_values, full_result=True
            )

            temp_ids = []
            temp_trans = []

            for i, tr in enumerate(default.found):
                for j, tr2 in enumerate(result.found):
                    if tr.ids != tr2.ids:
                        continue

                    r1 = tr.get_language().get_string(default.values[i], default.indexes[i])
                    r2 = tr2.get_language().get_string(result.values[j], result.indexes[j])
                    if r1 and r2 and r1[0] != r2[0]:
                        temp_trans.append(self._format_detailed(r1[0], r2[0]))
                    elif r2 and r2[0]:
                        temp_trans.append(self._format_hidden(r2[0]))
                    temp_ids.append(tr.ids)

                is_missing = True
                for tid in tr.ids:
                    is_missing = is_missing and (tid in result.missing_ids)

                if not is_missing:
                    continue

                r1 = tr.get_language().get_string(default.values[i], default.indexes[i])
                if r1 and r1[0]:
                    temp_trans.append(self._HIDDEN_FORMAT % r1[0])
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

    Parameters
    ----------
    string : str
        String to format

    Returns
    -------
    str
        String formatted with inter wiki links
    """
    out = []

    last_index = 0

    for match in _inter_wiki_re.finditer(string):
        index = match.lastindex
        full = match.group(0)
        short = match.group('short')
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
