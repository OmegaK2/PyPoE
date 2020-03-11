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

Documentation
===============================================================================

Classes
-------------------------------------------------------------------------------

.. autoclass:: BaseParser

.. autoclass:: WikiCondition

.. autoclass:: TagHandler

Functions
-------------------------------------------------------------------------------

.. autofunction:: find_template

.. autofunction:: format_result_rows

.. autofunction:: make_inter_wiki_links

.. autofunction:: parse_and_handle_description_tags
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
import warnings
import os
from collections import OrderedDict
from functools import partial

# self
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter import config
from PyPoE.cli.exporter.util import get_content_ggpk_path
from PyPoE.poe.constants import MOD_DOMAIN, WORDLISTS, MOD_STATS_RANGE
from PyPoE.poe.text import parse_description_tags
from PyPoE.poe.file.dat import RelationalReader, set_default_spec
from PyPoE.poe.file.translations import (
    TranslationFileCache,
    MissingIdentifierWarning,
    get_custom_translation_file,
    install_data_dependant_quantifiers,
)
from PyPoE.poe.file.ggpk import GGPKFile, extract_dds
from PyPoE.poe.file.ot import OTFileCache
from PyPoE.poe.sim.mods import get_translation_file_from_domain

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'BaseParser',
    'WikiCondition',
    'TagHandler',

    'find_template',
    'format_result_rows',
    'make_inter_wiki_links',
    'parse_and_handle_description_tags',
]

DEFAULT_INDENT = 32

_inter_wiki_map = {
    'English': (
        #
        # Attibutes
        #
        ('Dexterity', {'link': 'Dexterity'}),
        ('Intelligence', {'link': 'Intelligence'}),
        ('Strength', {'link': 'Strength'}),
        #
        # Offense stats
        #
        ('Accuracy Rating', {'link': 'Accuracy Rating'}),
        ('Accuracy', {'link': 'Accuracy'}),
        ('Attack Speed', {'link': 'Attack Speed'}),
        ('Cast Speed', {'link': 'Cast Speed'}),
        ('Critical Strike Chance', {'link': 'Critical Strike Chance'}),
        ('Critical Strike Multiplier', {'link': 'Critical Strike Multiplier'}),
        ('Critical Strike', {'link': 'Critical Strike'}),
        ('Movement Speed', {'link': 'Movement Speed'}),
        ('Leech', {'link': 'Leech'}), # Life Leech, Mana Leech
        ('Low Life', {'link': 'Low Life'}),
        ('Full Life', {'link': 'Full Life'}),
        ('Life', {'link': 'Life'}),
        ('Mana Reservation', {'link': 'Mana Reservation'}),
        ('Low Mana', {'link': 'Low Mana'}),
        ('Full Mana', {'link': 'Full Mana'}),
        ('Mana', {'link': 'Mana'}),
        # Just damage
        #('Damage', {'link': 'Damage'}),
        #
        # Defenses
        #
        ('Armour Rating', {'link': 'Armour Rating'}),
        ('Armour', {'link': 'Armour'}),
        ('Energy Shield', {'link': 'Energy Shield'}),
        ('Evasion Rating', {'link': 'Evasion Rating'}),
        ('Evasion', {'link': 'Evasion'}),
        ('Spell Block', {'link': 'Spell Block'}),
        ('Block', {'link': 'Block'}),
        ('Spell Dodge', {'link': 'Spell Dodge'}),
        ('Dodge', {'link': 'Dodge'}),
        #
        ('Chaos Resistance(?:|s)', {'link': 'Chaos Resistance'}),
        ('Cold Resistance(?:|s)', {'link': 'Cold Resistance'}),
        ('Fire Resistance(?:|s)', {'link': 'Fire Resistance'}),
        ('Lightning Resistance(?:|s)', {'link': 'Lightning Resistance'}),
        ('Elemental Resistance(?:|s)', {'link': 'Elemental Resistance'}),
        #
        # Buffs
        #

        # Charges
        ('Endurance Charge(?:|s)', {'link': 'Endurance Charge'}),
        ('Frenzy Charge(?:|s)', {'link': 'Frenzy Charge'}),
        ('Power Charge(?:|s)', {'link': 'Power Charge'}),

        # Friendly
        ('Rampage', {'link': 'Rampage'}),

        # Hostile
        ('Corrupted Blood', {'link': 'Corrupted Blood'}),

        #
        # Misc stats
        #

        ('Character Size', {'link': 'Character Size'}),

        #
        # Skills
        #
        ('Abyssal Cry', {'link': 'Abyssal Cry'}),
        ('Ancestral Protector', {'link': 'Ancestral Protector'}),
        ('Ancestral Warchief', {'link': 'Ancestral Warchief'}),
        ('Anger', {'link': 'Anger'}),
        ('Animate(?:|d) Guardian', {'link': 'Animate Guardian'}),
        ('Animate(?:|d) Weapon', {'link': 'Animate Weapon'}),
        ('(?:Arc | Arc)', {'link': 'Arc'}),
        ('Arctic Armour', {'link': 'Arctic Armour'}),
        ('Arctic Breath', {'link': 'Arctic Breath'}),
        ('Assassin\'s Mark', {'link': 'Assassin\'s Mark'}),
        ('Ball Lightning', {'link': 'Ball Lightning'}),
        ('Barrage', {'link': 'Barrage'}),
        ('Bear Trap', {'link': 'Bear Trap'}),
        ('Blade Flurry', {'link': 'Blade Flurry'}),
        ('Blade Trap', {'link': 'Blade Trap'}),
        ('Blade Vortex', {'link': 'Blade Vortex'}),
        ('Bladefall', {'link': 'Bladefall'}),
        ('Blast Rain', {'link': 'Blast Rain'}),
        ('Blight', {'link': 'Blight'}),
        ('Blink Arrow', {'link': 'Blink Arrow'}),
        ('Blood Rage', {'link': 'Blood Rage'}),
        ('Bone Offering', {'link': 'Bone Offering'}),
        ('Burning Arrow', {'link': 'Burning Arrow'}),
        ('Caustic Arrow', {'link': 'Caustic Arrow'}),
        ('Charged Dash', {'link': 'Charged Dash'}),
        ('Clarity', {'link': 'Clarity'}),
        ('Cleave', {'link': 'Cleave'}),
        ('Cold Snap', {'link': 'Cold Snap'}),
        ('Conductivity', {'link': 'Conductivity'}),
        ('Contagion', {'link': 'Contagion'}),
        ('Conversion Trap', {'link': 'Conversion Trap'}),
        ('Convocation', {'link': 'Convocation'}),
        ('Cyclone', {'link': 'Cyclone'}),
        ('Damage Infusion', {'link': 'Damage Infusion'}),
        ('Dark Pact', {'link': 'Dark Pact'}),
        ('Decoy Totem', {'link': 'Decoy Totem'}),
        ('Desecrate', {'link': 'Desecrate'}),
        ('Determination', {'link': 'Determination'}),
        ('Detonate Dead', {'link': 'Detonate Dead'}),
        ('Detonate Mines', {'link': 'Detonate Mines'}),
        ('Devouring Totem', {'link': 'Devouring Totem'}),
        ('Discharge', {'link': 'Discharge'}),
        ('Discipline', {'link': 'Discipline'}),
        ('Dominating Blow', {'link': 'Dominating Blow'}),
        ('Doom Arrow', {'link': 'Doom Arrow'}),
        ('Double Strike', {'link': 'Double Strike'}),
        ('Dual Strike', {'link': 'Dual Strike'}),
        ('Earthquake', {'link': 'Earthquake'}),
        ('Elemental Hit', {'link': 'Elemental Hit'}),
        ('Elemental Weakness', {'link': 'Elemental Weakness'}),
        ('Enduring Cry', {'link': 'Enduring Cry'}),
        ('Energy Beam', {'link': 'Energy Beam'}),
        ('Enfeeble', {'link': 'Enfeeble'}),
        ('Essence Drain', {'link': 'Essence Drain'}),
        ('Ethereal Knives', {'link': 'Ethereal Knives'}),
        ('Explosive Arrow', {'link': 'Explosive Arrow'}),
        ('Fire Nova Mine', {'link': 'Fire Nova Mine'}),
        ('Fire Trap', {'link': 'Fire Trap'}),
        ('Fire Weapon', {'link': 'Fire Weapon'}),
        ('Fireball', {'link': 'Fireball'}),
        ('Firestorm', {'link': 'Firestorm'}),
        ('Flame Dash', {'link': 'Flame Dash'}),
        ('Flame Surge', {'link': 'Flame Surge'}),
        ('Flame Totem', {'link': 'Flame Totem'}),
        ('Flameblast', {'link': 'Flameblast'}),
        ('Flammability', {'link': 'Flammability'}),
        ('Flesh Offering', {'link': 'Flesh Offering'}),
        ('Flicker Strike', {'link': 'Flicker Strike'}),
        ('Freeze Mine', {'link': 'Freeze Mine'}),
        ('Freezing Pulse', {'link': 'Freezing Pulse'}),
        ('Frenzy', {'link': 'Frenzy'}),
        ('Frostbolt', {'link': 'Frostbolt'}),
        ('Frost Blades', {'link': 'Frost Blades'}),
        ('Frost Bomb', {'link': 'Frost Bomb'}),
        ('Frost Wall', {'link': 'Frost Wall'}),
        ('Frostbite', {'link': 'Frostbite'}),
        ('Glacial Cascade', {'link': 'Glacial Cascade'}),
        ('Glacial Hammer', {'link': 'Glacial Hammer'}),
        ('Grace', {'link': 'Grace'}),
        ('Ground Slam', {'link': 'Ground Slam'}),
        ('Haste', {'link': 'Haste'}),
        ('Hatred', {'link': 'Hatred'}),
        ('Heavy Strike', {'link': 'Heavy Strike'}),
        ('Herald of Ash', {'link': 'Herald of Ash'}),
        ('Herald of Blood', {'link': 'Herald of Blood'}),
        ('Herald of Ice', {'link': 'Herald of Ice'}),
        ('Herald of Thunder', {'link': 'Herald of Thunder'}),
        ('Ice Crash', {'link': 'Ice Crash'}),
        ('Ice Nova', {'link': 'Ice Nova'}),
        ('Ice Shot', {'link': 'Ice Shot'}),
        ('Ice Spear', {'link': 'Ice Spear'}),
        ('Ice Trap', {'link': 'Ice Trap'}),
        ('Immortal Call', {'link': 'Immortal Call'}),
        ('Incinerate', {'link': 'Incinerate'}),
        ('Infernal Blow', {'link': 'Infernal Blow'}),
        ('Kinetic Blast', {'link': 'Kinetic Blast'}),
        ('Lacerate', {'link': 'Lacerate'}),
        ('Leap Slam', {'link': 'Leap Slam'}),
        ('Lightning Arrow', {'link': 'Lightning Arrow'}),
        ('Lightning Channel', {'link': 'Lightning Channel'}),
        ('Lightning Circle', {'link': 'Lightning Circle'}),
        ('Lightning Strike', {'link': 'Lightning Strike'}),
        ('Lightning Tendrils', {'link': 'Lightning Tendrils'}),
        ('Lightning Trap', {'link': 'Lightning Trap'}),
        ('Lightning Warp', {'link': 'Lightning Warp'}),
        ('Magma Orb', {'link': 'Magma Orb'}),
        ('Mirror Arrow', {'link': 'Mirror Arrow'}),
        ('Molten Shell', {'link': 'Molten Shell'}),
        ('Molten Strike', {'link': 'Molten Strike'}),
        ('Orb of Storms', {'link': 'Orb of Storms'}),
        ('Phase Run', {'link': 'Phase Run'}),
        ('Poacher\'s Mark', {'link': 'Poacher\'s Mark'}),
        ('Portal', {'link': 'Portal'}),
        ('Power Siphon', {'link': 'Power Siphon'}),
        ('Projectile Weakness', {'link': 'Projectile Weakness'}),
        ('Puncture', {'link': 'Puncture'}),
        ('Punishment', {'link': 'Punishment'}),
        ('Purity of Elements', {'link': 'Purity of Elements'}),
        ('Purity of Fire', {'link': 'Purity of Fire'}),
        ('Purity of Ice', {'link': 'Purity of Ice'}),
        ('Purity of Lightning', {'link': 'Purity of Lightning'}),
        ('Rain of Arrows', {'link': 'Rain of Arrows'}),
        ('Raise Spectre', {'link': 'Raise Spectre'}),
        ('Raise Zombie', {'link': 'Raise Zombie'}),
        ('Rallying Cry', {'link': 'Rallying Cry'}),
        ('Reave', {'link': 'Reave'}),
        ('Reckoning', {'link': 'Reckoning'}),
        ('Rejuvenation Totem', {'link': 'Rejuvenation Totem'}),
        ('Righteous Fire', {'link': 'Righteous Fire'}),
        ('Righteous Lightning', {'link': 'Righteous Lightning'}),
        ('Riposte', {'link': 'Riposte'}),
        ('Scorching Ray', {'link': 'Scorching Ray'}),
        ('Searing Bond', {'link': 'Searing Bond'}),
        ('Shadow Blades', {'link': 'Shadow Blades'}),
        ('Shield Charge', {'link': 'Shield Charge'}),
        ('Shock Nova', {'link': 'Shock Nova'}),
        ('Shockwave Totem', {'link': 'Shockwave Totem'}),
        ('Shrapnel Shot', {'link': 'Shrapnel Shot'}),
        ('Siege Ballista', {'link': 'Siege Ballista'}),
        ('Smoke Mine', {'link': 'Smoke Mine'}),
        ('Spark', {'link': 'Spark'}),
        ('Spectral Throw', {'link': 'Spectral Throw'}),
        ('Spirit Offering', {'link': 'Spirit Offering'}),
        ('Split Arrow', {'link': 'Split Arrow'}),
        ('Static Strike', {'link': 'Static Strike'}),
        ('Static Tether', {'link': 'Static Tether'}),
        ('Storm Burst', {'link': 'Storm Burst'}),
        ('Storm Call', {'link': 'Storm Call'}),
        ('(?:Summon |)Chaos Golem(?:|s)', {'link': 'Summon Chaos Golem'}),
        ('(?:Summon |)Flame Golem(?:|s)', {'link': 'Summon Flame Golem'}),
        ('(?:Summon |)Ice Golem(?:|s)', {'link': 'Summon Ice Golem'}),
        ('(?:Summon |)Lightning Golem(?:|s)', {
            'link': 'Summon Lightning Golem'
        }),
        ('Summon Raging Spirit', {'link': 'Summon Raging Spirit'}),
        ('Summon Skeleton', {'link': 'Summon Skeleton'}),
        ('(?:Summon |)Stone Golem(?:|s)', {'link': 'Summon Stone Golem'}),
        ('Sunder', {'link': 'Sunder'}),
        ('Sweep', {'link': 'Sweep'}),
        ('Tempest Shield', {'link': 'Tempest Shield'}),
        ('Temporal Chains', {'link': 'Temporal Chains'}),
        ('Tornado Shot', {'link': 'Tornado Shot'}),
        ('Vaal Arc', {'link': 'Vaal Arc'}),
        ('Vaal Burning Arrow', {'link': 'Vaal Burning Arrow'}),
        ('Vaal Clarity', {'link': 'Vaal Clarity'}),
        ('Vaal Cold Snap', {'link': 'Vaal Cold Snap'}),
        ('Vaal Cyclone', {'link': 'Vaal Cyclone'}),
        ('Vaal Detonate Dead', {'link': 'Vaal Detonate Dead'}),
        ('Vaal Discipline', {'link': 'Vaal Discipline'}),
        ('Vaal Double Strike', {'link': 'Vaal Double Strike'}),
        ('Vaal FireTrap', {'link': 'Vaal FireTrap'}),
        ('Vaal Fireball', {'link': 'Vaal Fireball'}),
        ('Vaal Flameblast', {'link': 'Vaal Flameblast'}),
        ('Vaal Glacial Hammer', {'link': 'Vaal Glacial Hammer'}),
        ('Vaal Grace', {'link': 'Vaal Grace'}),
        ('Vaal Ground Slam', {'link': 'Vaal Ground Slam'}),
        ('Vaal Haste', {'link': 'Vaal Haste'}),
        ('Vaal Heavy Strike', {'link': 'Vaal Heavy Strike'}),
        ('Vaal Ice Nova', {'link': 'Vaal Ice Nova'}),
        ('Vaal Immortal Call', {'link': 'Vaal Immortal Call'}),
        ('Vaal Lightning Strike', {'link': 'Vaal Lightning Strike'}),
        ('Vaal Lightning Trap', {'link': 'Vaal Lightning Trap'}),
        ('Vaal Lightning Warp', {'link': 'Vaal Lightning Warp'}),
        ('Vaal Molten Shell', {'link': 'Vaal Molten Shell'}),
        ('Vaal Power Siphon', {'link': 'Vaal Power Siphon'}),
        ('Vaal Rain of Arrows', {'link': 'Vaal Rain of Arrows'}),
        ('Vaal Reave', {'link': 'Vaal Reave'}),
        ('Vaal Righteous Fire', {'link': 'Vaal Righteous Fire'}),
        ('Vaal Spark', {'link': 'Vaal Spark'}),
        ('Vaal Spectral Throw', {'link': 'Vaal Spectral Throw'}),
        ('Vaal Storm Call', {'link': 'Vaal Storm Call'}),
        ('Vaal Summon Skeletons', {'link': 'Vaal Summon Skeletons'}),
        ('Vaal Sweep', {'link': 'Vaal Sweep'}),
        ('Vengeance', {'link': 'Vengeance'}),
        ('Vigilant Strike', {'link': 'Vigilant Strike'}),
        ('Viper Strike', {'link': 'Viper Strike'}),
        ('Vitality', {'link': 'Vitality'}),
        ('Vortex', {'link': 'Vortex'}),
        ('Vulnerability', {'link': 'Vulnerability'}),
        ('Warlord\'s Mark', {'link': 'Warlord\'s Mark'}),
        ('Whirling Blades', {'link': 'Whirling Blades'}),
        ('Wild Strike', {'link': 'Wild Strike'}),
        ('Wither', {'link': 'Wither'}),
        ('Wrath', {'link': 'Wrath'}),
        #
        # Enchantment skills
        #
        ('Commandment of Blades', {'link': 'Commandment of Blades'}),
        ('Commandment of Flames', {'link': 'Commandment of Flames'}),
        ('Commandment of Force', {'link': 'Commandment of Force'}),
        ('Commandment of Frost', {'link': 'Commandment of Frost'}),
        ('Commandment of Fury', {'link': 'Commandment of Fury'}),
        ('Commandment of Inferno', {'link': 'Commandment of Inferno'}),
        ('Commandment of Ire', {'link': 'Commandment of Ire'}),
        ('Commandment of Light', {'link': 'Commandment of Light'}),
        ('Commandment of Reflection', {'link': 'Commandment of Reflection'}),
        ('Commandment of Spite', {'link': 'Commandment of Spite'}),
        ('Commandment of Thunder', {'link': 'Commandment of Thunder'}),
        ('Commandment of War', {'link': 'Commandment of War'}),
        ('Commandment of Winter', {'link': 'Commandment of Winter'}),
        ('Commandment of the Grave', {'link': 'Commandment of the Grave'}),
        ('Commandment of the Tempest', {'link': 'Commandment of the Tempest'}),
        ('Decree of Blades', {'link': 'Decree of Blades'}),
        ('Decree of Flames', {'link': 'Decree of Flames'}),
        ('Decree of Force', {'link': 'Decree of Force'}),
        ('Decree of Frost', {'link': 'Decree of Frost'}),
        ('Decree of Fury', {'link': 'Decree of Fury'}),
        ('Decree of Inferno', {'link': 'Decree of Inferno'}),
        ('Decree of Ire', {'link': 'Decree of Ire'}),
        ('Decree of Light', {'link': 'Decree of Light'}),
        ('Decree of Reflection', {'link': 'Decree of Reflection'}),
        ('Decree of Spite', {'link': 'Decree of Spite'}),
        ('Decree of Thunder', {'link': 'Decree of Thunder'}),
        ('Decree of War', {'link': 'Decree of War'}),
        ('Decree of Winter', {'link': 'Decree of Winter'}),
        ('Decree of the Grave', {'link': 'Decree of the Grave'}),
        ('Decree of the Tempest', {'link': 'Decree of the Tempest'}),
        ('Edict of Blades', {'link': 'Edict of Blades'}),
        ('Edict of Flames', {'link': 'Edict of Flames'}),
        ('Edict of Force', {'link': 'Edict of Force'}),
        ('Edict of Frost', {'link': 'Edict of Frost'}),
        ('Edict of Fury', {'link': 'Edict of Fury'}),
        ('Edict of Inferno', {'link': 'Edict of Inferno'}),
        ('Edict of Ire', {'link': 'Edict of Ire'}),
        ('Edict of Light', {'link': 'Edict of Light'}),
        ('Edict of Reflection', {'link': 'Edict of Reflection'}),
        ('Edict of Spite', {'link': 'Edict of Spite'}),
        ('Edict of Thunder', {'link': 'Edict of Thunder'}),
        ('Edict of War', {'link': 'Edict of War'}),
        ('Edict of Winter', {'link': 'Edict of Winter'}),
        ('Edict of the Grave', {'link': 'Edict of the Grave'}),
        ('Edict of the Tempest', {'link': 'Edict of the Tempest'}),
        ('Word of Blades', {'link': 'Word of Blades'}),
        ('Word of Flames', {'link': 'Word of Flames'}),
        ('Word of Force', {'link': 'Word of Force'}),
        ('Word of Frost', {'link': 'Word of Frost'}),
        ('Word of Fury', {'link': 'Word of Fury'}),
        ('Word of Inferno', {'link': 'Word of Inferno'}),
        ('Word of Ire', {'link': 'Word of Ire'}),
        ('Word of Light', {'link': 'Word of Light'}),
        ('Word of Reflection', {'link': 'Word of Reflection'}),
        ('Word of Spite', {'link': 'Word of Spite'}),
        ('Word of Thunder', {'link': 'Word of Thunder'}),
        ('Word of War', {'link': 'Word of War'}),
        ('Word of Winter', {'link': 'Word of Winter'}),
        ('Word of the Grave', {'link': 'Word of the Grave'}),
        ('Word of the Tempest', {'link': 'Word of the Tempest'}),
        #
        # Support gems
        #
        ('(?:level [0-9]+) Added Chaos Damage', {
            'link': 'Added Chaos Damage Support'}),
        ('(?:level [0-9]+) Added Cold Damage', {
            'link': 'Added Cold Damage Support'}),
        ('(?:level [0-9]+) Added Fire Damage', {
            'link': 'Added Fire Damage Support'}),
        ('(?:level [0-9]+) Added Lightning Damage', {
            'link': 'Added Lightning Damage Support'}),
        ('(?:level [0-9]+) Additional Accuracy', {
            'link': 'Additional Accuracy Support'}),
        ('(?:level [0-9]+) Arcane Surge', {'link': 'Arcane Surge Support'}),
        ('(?:level [0-9]+) Blasphemy', {'link': 'Blasphemy Support'}),
        ('(?:level [0-9]+) Blind', {'link': 'Blind Support'}),
        ('(?:level [0-9]+) Block Chance Reduction', {
            'link': 'Block Chance Reduction Support'}),
        ('(?:level [0-9]+) Blood Magic', {'link': 'Blood Magic Support'}),
        ('(?:level [0-9]+) Bloodlust', {'link': 'Bloodlust Support'}),
        ('(?:level [0-9]+) Brutality', {'link': 'Brutality Support'}),
        ('(?:level [0-9]+) Burning Damage', {'link': 'Burning Damage Support'}),
        ('(?:level [0-9]+) Cast On Critical Strike', {
            'link': 'Cast On Critical Strike Support'}),
        ('(?:level [0-9]+) Cast on Death', {'link': 'Cast on Death Support'}),
        ('(?:level [0-9]+) Cast on Melee Kill', {
            'link': 'Cast on Melee Kill Support'}),
        ('(?:level [0-9]+) Cast when Damage Taken', {
            'link': 'Cast when Damage Taken Support'}),
        ('(?:level [0-9]+) Cast when Stunned', {
            'link': 'Cast when Stunned Support'}),
        ('(?:level [0-9]+) Chain', {'link': 'Chain Support'}),
        ('(?:level [0-9]+) Chance to Bleed', {
            'link': 'Chance to Bleed Support'}),
        ('(?:level [0-9]+) Chance to Flee', {'link': 'Chance to Flee Support'}),
        ('(?:level [0-9]+) Chance to Ignite', {
            'link': 'Chance to Ignite Support'}),
        ('(?:level [0-9]+) Cluster Traps', {'link': 'Cluster Traps Support'}),
        ('(?:level [0-9]+) Cold Penetration', {
            'link': 'Cold Penetration Support'}),
        ('(?:level [0-9]+) Cold to Fire', {'link': 'Cold to Fire Support'}),
        ('(?:level [0-9]+) Concentrated Effect', {
            'link': 'Concentrated Effect Support'}),
        ('(?:level [0-9]+) Controlled Destruction', {
            'link': 'Controlled Destruction Support'}),
        ('(?:level [0-9]+) Culling Strike', {'link': 'Culling Strike Support'}),
        ('(?:level [0-9]+) Curse On Hit', {'link': 'Curse On Hit Support'}),
        ('(?:level [0-9]+) Damage on Full Life', {
            'link': 'Damage on Full Life Support'}),
        ('(?:level [0-9]+) Deadly Ailments', {
            'link': 'Deadly Ailments Support'}),
        ('(?:level [0-9]+) Decay', {'link': 'Decay Support'}),
        ('(?:level [0-9]+) Efficacy', {'link': 'Efficacy Support'}),
        ('(?:level [0-9]+) Elemental Focus', {
            'link': 'Elemental Focus Support'}),
        ('(?:level [0-9]+) Elemental Proliferation', {
            'link': 'Elemental Proliferation Support'}),
        ('(?:level [0-9]+) Empower', {'link': 'Empower Support'}),
        ('(?:level [0-9]+) Endurance Charge on Melee Stun', {
            'link': 'Endurance Charge on Melee Stun Support'}),
        ('(?:level [0-9]+) Enhance', {'link': 'Enhance Support'}),
        ('(?:level [0-9]+) Enlighten', {'link': 'Enlighten Support'}),
        ('(?:level [0-9]+) Elemental Damage with Attacks', {
            'link': 'Elemental Damage with Attacks Support'}),
        ('(?:level [0-9]+) Faster Attacks', {
            'link': 'Faster Attacks Support'}),
        ('(?:level [0-9]+) Faster Casting', {
            'link': 'Faster Casting Support'}),
        ('(?:level [0-9]+) Faster Projectiles', {
            'link': 'Faster Projectiles Support'}),
        ('(?:level [0-9]+) Fire Penetration', {
            'link': 'Fire Penetration Support'}),
        ('(?:level [0-9]+) Fork', {'link': 'Fork Support'}),
        ('(?:level [0-9]+) Fortify', {'link': 'Fortify Support'}),
        ('(?:level [0-9]+) Generosity', {'link': 'Generosity Support'}),
        ('(?:level [0-9]+) Greater Multiple Projectiles', {
            'link': 'Greater Multiple Projectiles Support'}),
        ('(?:level [0-9]+) Hypothermia', {'link': 'Hypothermia Support'}),
        ('(?:level [0-9]+) Ice Bite', {'link': 'Ice Bite Support'}),
        ('(?:level [0-9]+) Increased Area of Effect', {
            'link': 'Increased Area of Effect Support'}),
        ('(?:level [0-9]+) Increased Critical Damage', {
            'link': 'Increased Critical Damage Support'}),
        ('(?:level [0-9]+) Increased Critical Strikes', {
            'link': 'Increased Critical Strikes Support'}),
        ('(?:level [0-9]+) Increased Duration', {
            'link': 'Increased Duration Support'}),
        ('(?:level [0-9]+) Innervate', {'link': 'Innervate Support'}),
        ('(?:level [0-9]+) Ignite Proliferation', {
            'link': 'Ignite Proliferation Support'}),
        ('(?:level [0-9]+) Iron Grip', {'link': 'Iron Grip Support'}),
        ('(?:level [0-9]+) Iron Will', {'link': 'Iron Will Support'}),
        ('(?:level [0-9]+) Item Quantity', {'link': 'Item Quantity Support'}),
        ('(?:level [0-9]+) Item Rarity', {'link': 'Item Rarity Support'}),
        ('(?:level [0-9]+) Immolate', {'link': 'Immolate Support'}),
        ('(?:level [0-9]+) Knockback', {'link': 'Knockback Support'}),
        ('(?:level [0-9]+) Less Duration', {'link': 'Less Duration Support'}),
        ('(?:level [0-9]+) Lesser Multiple Projectiles', {
            'link': 'Lesser Multiple Projectiles Support'}),
        ('(?:level [0-9]+) Lesser Poison', {'link': 'Lesser Poison Support'}),
        ('(?:level [0-9]+) Life Gain on Hit', {
            'link': 'Life Gain on Hit Support'}),
        ('(?:level [0-9]+) Life Leech', {'link': 'Life Leech Support'}),
        ('(?:level [0-9]+) Lightning Penetration', {
            'link': 'Lightning Penetration Support'}),
        ('(?:level [0-9]+) Maim', {'link': 'Maim Support'}),
        ('(?:level [0-9]+) Mana Leech', {'link': 'Mana Leech Support'}),
        ('(?:level [0-9]+) Melee Physical Damage', {
            'link': 'Melee Physical Damage Support'}),
        ('(?:level [0-9]+) Melee Splash', {'link': 'Melee Splash Support'}),
        ('(?:level [0-9]+) Minefield', {'link': 'Minefield Support'}),
        ('(?:level [0-9]+) Minion Damage', {'link': 'Minion Damage Support'}),
        ('(?:level [0-9]+) Minion Life', {'link': 'Minion Life Support'}),
        ('(?:level [0-9]+) Minion Speed', {'link': 'Minion Speed Support'}),
        ('(?:level [0-9]+) Minion and Totem Elemental Resistance', {
            'link': 'Minion and Totem Elemental Resistance Support'}),
        ('(?:level [0-9]+) Multiple Traps', {'link': 'Multiple Traps Support'}),
        ('(?:level [0-9]+) Multistrike', {'link': 'Multistrike Support'}),
        ('(?:level [0-9]+) Onslaught', {'link': 'Onslaught Support'}),
        ('(?:level [0-9]+) Physical Projectile Attack Damage', {
            'link': 'Physical Projectile Attack Damage Support'}),
        ('(?:level [0-9]+) Physical to Lightning', {
            'link': 'Physical to Lightning Support'}),
        ('(?:level [0-9]+) Pierce', {'link': 'Pierce Support'}),
        ('(?:level [0-9]+) Point Blank', {'link': 'Point Blank Support'}),
        ('(?:level [0-9]+) Poison', {'link': 'Poison Support'}),
        ('(?:level [0-9]+) Power Charge On Critical', {
            'link': 'Power Charge On Critical Support'}),
        ('(?:level [0-9]+) Ranged Attack Totem', {
            'link': 'Ranged Attack Totem Support'}),
        ('(?:level [0-9]+) Reduced Mana', {'link': 'Reduced Mana Support'}),
        ('(?:level [0-9]+) Remote Mine', {'link': 'Remote Mine Support'}),
        ('(?:level [0-9]+) Return Projectiles', {
            'link': 'Return Projectiles Support'}),
        ('(?:level [0-9]+) Ruthless', {'link': 'Ruthless Support'}),
        ('(?:level [0-9]+) Slower Projectiles', {
            'link': 'Slower Projectiles Support'}),
        ('(?:level [0-9]+) Spell Echo', {'link': 'Spell Echo Support'}),
        ('(?:level [0-9]+) Spell Totem', {'link': 'Spell Totem Support'}),
        ('(?:level [0-9]+) Split Projectiles', {
            'link': 'Split Projectiles Support'}),
        ('(?:level [0-9]+) Stun', {'link': 'Stun Support'}),
        ('(?:level [0-9]+) Swift Affliction', {
            'link': 'Swift Affliction Support'}),
        ('(?:level [0-9]+) Trap', {'link': 'Trap Support'}),
        ('(?:level [0-9]+) Trap Cooldown', {'link': 'Trap Cooldown Support'}),
        ('(?:level [0-9]+) Trap and Mine Damage', {
            'link': 'Trap and Mine Damage Support'}),
        ('(?:level [0-9]+) Unbound Ailments', {
            'link': 'Unbound Ailments Support'}),
        ('(?:level [0-9]+) Vile Toxins', {'link': 'Vile Toxins Support'}),
        ('(?:level [0-9]+) Void Manipulation', {
            'link': 'Void Manipulation Support'}),
        #
        # Groups
        #
        ('Physical(?:Skill|Gem)', {'link': 'Physical Skills'}),
        ('Fire (?:Skill|Gem)', {'link': 'Fire Skills'}),
        ('Cold (?:Skill|Gem)', {'link': 'Cold Skills'}),
        ('Lightning (?:Skill|Gem)', {'link': 'Lightning Skills'}),
        ('Chaos (?:Skill|Gem)', {'link': 'Chaos Skills'}),
        ('Area (?:Skill|Gem)', {'link': 'Area Skills'}),
        ('Melee (?:Skill|Gem)', {'link': 'Melee Skills'}),
        ('Bow (?:Skill|Gem)', {'link': 'Bow Skills'}),
        ('Minion (?:Skill|Gem)', {'link': 'Minion Skills'}),

        #
        # Damage
        #
        # Base types
        ('Chaos Damage', {'link': 'Chaos Damage'}),
        ('Cold Damage', {'link': 'Cold Damage'}),
        ('Fire Damage', {'link': 'Fire Damage'}),
        ('Lightning Damage', {'link': 'Lightning Damage'}),
        ('Physical Damage', {'link': 'Physical Damage'}),
        # Mixed and special
        ('Attack Damage', {'link': 'Attack Damage'}),
        ('Spell Damage', {'link': 'Spell Damage'}),
        ('Elemental Damage', {'link': 'Elemental Damage'}),
        ('Minion Damage', {'link': 'Minion Damage'}),

        #
        # Armour & weapon types
        #

        # Generic
        ('Two Handed Melee Weapon(?:|s)', {'link': 'Two Handed Melee Weapons'}),

        # Armour
        ('Shield(?:|s)', {'link': 'Shield'}),

        # Melee
        ('Axe(?:|s)', {'link': 'Axe'}),
        ('Claw(?:|s)', {'link': 'Claw'}),
        ('Dagger(?:|s)', {'link': 'Dagger'}),
        ('Mace(?:|s)', {'link': 'Mace'}),
        ('Staff|Staves', {'link': 'Staff'}),
        ('Sword(?:|s)', {'link': 'Sword'}),

        # Range
        ('Bow(?:|s)', {'link': 'Bow'}),
        ('Wand(?:|s)', {'link': 'Axe'}),
        #
        # Status
        #

        ('Shock(?:|s|ed)', {'link': 'Shock'}),
        ('Ignite(?:|s|ed)', {'link': 'Ignite'}),
        ('Frozen|Freeze(?:|s)', {'link': 'Freeze'}),
        ('Poison(?:|s|ed)', {'link': 'Poison'}),

        #
        # Misc
        #
        ('Curse(?:|s|ed)', {'link': 'Curse'}),
        ('Socket(?:|s|ed)', {'link': 'Item socket'}),
        ('Recently', {'link': 'Recently'}),
        ('Skill(?:|s)', {'link': 'Skill'}),
        ('Spell(?:|s)', {'link': 'Spell'}),
        ('Attack(?:|s)', {'link': 'Attack'}),
        ('Minion(?:|s)', {'link': 'Minion'}),
        ('Mine(?:|s)', {'link': 'Mine'}),
        ('Totem(?:|s)', {'link': 'Totem'}),
        ('Trap(?:|s)', {'link': 'Trap'}),
        ('Dual Wield(?:|ing)', {'link': 'Dual Wield'}),
        ('Level', {'link': 'Level'}),
        ('PvP', {'link': 'PvP'}),
        ('Hit(?:|s)', {'link': 'Hit'}),
        ('Kill(?:|s)', {'link': 'Kill'}),
        ('Charge(?:|s)', {'link': 'Charge'}),
        ('Lucky', {'link': 'Lucky'}),
        ('Unlucky', {'link': 'Unlucky'}),
    ),
    'Russian': (
        #
        # Attibutes
        #
        ('ловкост(?:|ь|и)', {'link': 'Ловкость'}),
        ('интеллект(?:|а|у)', {'link': 'Интеллект'}),
        ('сил(?:|а|е|ы)', {'link': 'Сила'}),
        ('характеристик(?:|ам)', {'link': 'Характеристики'}),
        #
        # Offense stats
        #
        ('меткост(?:|ь|и)', {'link': 'Меткость (механика)'}),
        ('скорост(?:|ь|и) атак(?:|и)', {'link': 'Скорость атаки'}),
        ('скорост(?:|ь|и) сотворения чар', {'link': 'Скорость сотворения чар'}),
        ('сотворения чар', {'link': 'Скорость сотворения чар'}),
        (
        'шанс(?:|а|у) критического удара', {'link': 'Шанс критического удара'}),
        ('множител(?:|ь|ю|я) критического удара',
         {'link': 'Множитель критического удара'}),
        ('критическ(?:|ий|им|ими|их) удар(?:|ом|ами|ов)',
         {'link': 'Критический удар'}),
        ('скорост(?:|ь|и) передвижения', {'link': 'Скорость передвижения'}),
        ('похищ(?:|ение|ения|ается|ать|енного|ают)', {'link': 'Похищение'}),
        # Life Leech, Mana Leech
        ('мало(?:|е|м|го) количеств(?:|о|е|а) здоровья|мало здоровья',
         {'link': 'Малое количество здоровья'}),
        ('полн(?:|ое|ом|ым) здоровье(?:|м)', {'link': 'Полное здоровье'}),
        ('здоровь(?:|е|я)', {'link': 'Здоровье'}),
        ('удерж(?:|анной|ивают) ман(?:|ы|у)', {'link': 'Удержание маны'}),
        ('малом количестве маны|мана не на низком уровне',
         {'link': 'Малое количество маны'}),
        ('полн(?:|ая|ой) ман(?:|а|е)', {'link': 'Полная мана'}),
        ('ман(?:|а|у|ы)', {'link': 'Мана'}),
        ('полном энергетическом щите', {'link': 'Полный энергетический щит'}),
        # Just damage
        # ('урон(?:|а)', {'link': 'Урон'}),
        #
        # Defenses
        #
        ('брон(?:|я|е|и|ю|ей)', {'link': 'Броня'}),
        ('энергетическ(?:|ий|ого|ом) щит(?:|а|е)',
         {'link': 'Энергетический щит'}),
        ('уклонени(?:|е|ю|я)', {'link': 'Уклонение'}),
        ('(?:за|)блок(?:|а|е|ировать|ировали|ированный)', {'link': 'Блок'}),
        ('увернуться|уворот(?:|а)', {'link': 'Уворот'}),
        #
        ('сопротивлени(?:|е|ю|я|ем) хаосу', {'link': 'Сопротивление хаосу'}),
        ('сопротивлени(?:|е|ю|я|ем) холоду', {'link': 'Сопротивление холоду'}),
        ('сопротивлени(?:|е|ю|я|ем) огню', {'link': 'Сопротивление огню'}),
        ('сопротивлени(?:|е|ю|я|ем) молнии', {'link': 'Сопротивление молнии'}),
        ('сопротивлени(?:|е|ю|я|ем) все(?:|м|х) стихи(?:|й|ям)',
         {'link': 'Сопротивление стихиям'}),
        #
        # Buffs
        #

        # Charges
        ('заряд(?:|а|ы|ов) выносливости', {'link': 'Заряд выносливости'}),
        ('заряд(?:|а|ы|ов) ярости', {'link': 'Заряд ярости'}),
        ('заряд(?:|а|ы|ов) энергии', {'link': 'Заряд энергии'}),

        # Friendly
        ('буйств(?:|о|е|а)', {'link': 'Буйство'}),

        # Hostile
        ('оскверненной крови', {'link': 'Оскверненная кровь'}),

        #
        # Misc stats
        #

        ('размер(?:|а) персонажа', {'link': 'Размер персонажа'}),

        #
        # Skills
        #
        ('Клич(?:|а) бездны', {'link': 'Клич бездны'}),
        ('Защитник(?:|а) предков', {'link': 'Защитник предков'}),
        ('Вожд(?:|ь|я) предков', {'link': 'Вождь предков'}),
        ('Жгуч(?:|ая|ей) злоб(?:|а|ы|ой)', {'link': 'Жгучая злоба'}),
        ('Аниматрон(?:|а|ы)', {'link': 'Аниматрон'}),
        ('Живо(?:|е|го)|оживл(?:|е|ё)нно(?:|е|го) оружи(?:|е|я)',
         {'link': 'Живое оружие'}),
        ('Цеп(?:|ь|и) молний', {'link': 'Цепь молний'}),
        ('Северн(?:|ая|ой) брон(?:|я|и|ёй)', {'link': 'Северная броня'}),
        ('Северно(?:|е|го) дыхани(?:|е|я)', {'link': 'Северное дыхание'}),
        ('Артиллерийск(?:|ая|ой) баллист(?:|а|ы)',
         {'link': 'Артиллерийская баллиста'}),
        ('Метк(?:|а|и|ой) убийцы', {'link': 'Метка убийцы'}),
        ('Шаров(?:|ая|ой) молни(?:|я|и)', {'link': 'Шаровая молния'}),
        ('Очеред(?:|ь|и)', {'link': 'Очередь'}),
        ('Медвеж(?:|ий|ьего) капкан(?:|а)', {'link': 'Медвежий капкан'}),
        ('Порыв(?:|а) клинков', {'link': 'Порыв клинков'}),
        ('Ловушка лезвий', {'link': 'Ловушка лезвий'}),
        ('Вихр(?:|ь|ю|я) клинков', {'link': 'Вихрь клинков'}),
        ('Мечепад(?:|а|у)', {'link': 'Мечепад'}),
        ('Дожд(?:|ь|ю|я) взрывов', {'link': 'Дождь взрывов'}),
        ('Мор(?:|а)', {'link': 'Мор'}),
        ('Стрел(?:|а|е|ы)-телепорт(?:|а|у)', {'link': 'Стрела-телепорт'}),
        ('Кровавый угар', {'link': 'Кровавый угар'}),
        ('Подношени(?:|е|я) костей', {'link': 'Подношение костей'}),
        ('Горящ(?:|ая|ей) стрел(?:|а|ы)', {'link': 'Горящая стрела'}),
        ('Едк(?:|ая|ой) стрел(?:|а|е|ы)', {'link': 'Едкая стрела'}),
        ('Заряженн(?:|ый|ого) рыв(?:|ок|ка)', {'link': 'Заряженный рывок'}),
        ('Ясност(?:|ь|и|ью) ума', {'link': 'Ясность ума'}),
        ('Рассечени(?:|е|я)', {'link': 'Рассечение'}),
        ('Бросок кобры', {'link': 'Бросок кобры'}),
        ('Укус(?:|а) стужи', {'link': 'Укус стужи'}),
        ('Проводимост(?:|ь|и|ью)', {'link': 'Проводимость'}),
        ('Инфекци(?:|и|я)', {'link': 'Инфекция'}),
        ('Ловушк(?:|а|и) переманивания', {'link': 'Ловушка переманивания'}),
        ('Сбор(?:|а)', {'link': 'Сбор'}),
        ('Вихр(?:|ь|я|ю)', {'link': 'Вихрь'}),
        ('Вливание урона', {'link': 'Вливание урона'}),
        ('Т(?:|е|ё)мн(?:|ый|ого) договор(?:|а)', {'link': 'Тёмный договор'}),
        ('Тотем(?:|а)-приманк(?:|а|и)', {'link': 'Тотем-приманка'}),
        ('Осквернение', {'link': 'Осквернение'}),
        ('Решимост(?:|и|ь|ью)', {'link': 'Решимость'}),
        ('Подрыв(?:|а|е) трупа', {'link': 'Подрыв трупа'}),
        ('Подрыв мин', {'link': 'Подрыв мин'}),
        ('Поглощающ(?:|ий|его) тотем(?:|а)', {'link': 'Поглощающий тотем'}),
        ('Разряд(?:|а)', {'link': 'Разряд'}),
        ('Дисциплин(?:|а|ы|ой)', {'link': 'Дисциплина'}),
        ('Удар(?:|а) власти', {'link': 'Удар власти'}),
        ('Стрела рока', {'link': 'Стрела рока'}),
        ('Двойн(?:|ой|ым|ого) удар(?:|а|ом)', {'link': 'Двойной удар'}),
        ('Парн(?:|ый|ым|ого) удар(?:|а|ом)', {'link': 'Парный удар'}),
        ('Землетрясени(?:|е|ю|я)', {'link': 'Землетрясение'}),
        ('Удар(?:|а|ом) стихии', {'link': 'Удар стихии'}),
        ('Уязвимост(?:|и|ь|ью) к стихиям', {'link': 'Уязвимость к стихиям'}),
        ('Клич(?:|а) стойкости', {'link': 'Клич стойкости'}),
        ('Слабост(?:|и|ь|ью)', {'link': 'Слабость'}),
        ('Похищени(?:|е|я) сущности', {'link': 'Похищение сущности'}),
        ('Бесплотны(?:|е|х) нож(?:|и|ей)', {'link': 'Бесплотные ножи'}),
        ('Взрывн(?:|ая|ой|ые) стрел(?:|а|ы)', {'link': 'Взрывная стрела'}),
        (
        'Пирокластов(?:|ая|ой|ые) мин(?:|а|ы)', {'link': 'Пирокластовая мина'}),
        ('Огненн(?:|ая|ой) ловушк(?:|а|и)', {'link': 'Огненная ловушка'}),
        ('Горящее оружие', {'link': 'Горящее оружие'}),
        ('Огненн(?:|ый|ого) шар(?:|а)', {'link': 'Огненный шар'}),
        ('Огненн(?:|ый|ого) шторм(?:|а)', {'link': 'Огненный шторм'}),
        ('Огненн(?:|ый|ого|ому) рыв(?:|ок|ка|ку)', {'link': 'Огненный рывок'}),
        ('Выброс(?:|а) пламени', {'link': 'Выброс пламени'}),
        ('Тотем(?:|а|ом) священного огня', {'link': 'Тотем священного огня'}),
        ('Пламенн(?:|ый|ого) взрыв(?:|а)', {'link': 'Пламенный взрыв'}),
        ('Горючест(?:|и|ь|ью)', {'link': 'Горючесть'}),
        ('Подношени(?:|е|я) плоти', {'link': 'Подношение плоти'}),
        ('Внезапн(?:|ый|ым|ого) удар(?:|а|ом)', {'link': 'Внезапный удар'}),
        ('Шквальн(?:|ая|ой) мин(?:|а|ы)', {'link': 'Шквальная мина'}),
        ('Волн(?:|а|ы) холода', {'link': 'Волна холода'}),
        ('Бешенств(?:|а|о)', {'link': 'Бешенство'}),
        ('Морозн(?:|ый|ого) шар(?:|а)', {'link': 'Морозный шар'}),
        ('Ледяны(?:|е|х|ми) клинк(?:|и|ов|ами)', {'link': 'Ледяные клинки'}),
        ('Морозн(?:|ая|ой) бомб(?:|а|ы)', {'link': 'Морозная бомба'}),
        ('Стен(?:|а|ы) льда', {'link': 'Стена льда'}),
        ('Обморожени(?:|е|ю|я|ем)', {'link': 'Обморожение'}),
        ('Ледян(?:|ой|ым|ого) каскад(?:|а|ом)', {'link': 'Ледяной каскад'}),
        ('Леденящ(?:|ий|им|его) молот(?:|а|ом)', {'link': 'Леденящий молот'}),
        ('Граци(?:|и|я|ей)', {'link': 'Грация'}),
        ('Сотрясени(?:|е|я)', {'link': 'Сотрясение'}),
        ('Спешк(?:|а|и|ой)', {'link': 'Спешка'}),
        (
        'Холодн(?:|ая|ой) ненавист(?:|ь|и|ью)', {'link': 'Холодная ненависть'}),
        ('Тяж(?:|е|ё)л(?:|ый|ого) удар(?:|а|ой)', {'link': 'Тяжёлый удар'}),
        ('Вестник(?:|а|у|ом) пепла', {'link': 'Вестник пепла'}),
        ('Вестник(?:|а|у|ом) крови', {'link': 'Вестник крови'}),
        ('Вестник(?:|а|у|ом) льда', {'link': 'Вестник льда'}),
        ('Вестник(?:|а|у|ом) грома', {'link': 'Вестник грома'}),
        ('Вестник(?:|а|у|ом) агонии', {'link': 'Вестник агонии'}),
        ('Вестник(?:|а|у|ом) чистоты', {'link': 'Вестник чистоты'}),
        ('Ледяно(?:|е|го) сокрушени(?:|е|я)', {'link': 'Ледяное сокрушение'}),
        ('Кольц(?:|а|о|ом) льда', {'link': 'Кольцо льда'}),
        ('Ледяно(?:|й|го) выстрел(?:|а)', {'link': 'Ледяной выстрел'}),
        ('Ледян(?:|ое|ым|ого) копь(?:|е|ё|я|ем|ём)', {'link': 'Ледяное копье'}),
        ('Ледян(?:|ая|ой) ловушк(?:|а|е|и)', {'link': 'Ледяная ловушка'}),
        ('Призыв(?:|а|у) к бессмертию', {'link': 'Призыв к бессмертию'}),
        ('Испепелени(?:|е|я)', {'link': 'Испепеление'}),
        ('Удар(?:|а) преисподней', {'link': 'Удар преисподней'}),
        ('Кинетическ(?:|ий|ого) взрыв(?:|а)', {'link': 'Кинетический взрыв'}),
        ('Разрубани(?:|е|я)', {'link': 'Разрубание'}),
        ('Наскок(?:|а)', {'link': 'Наскок'}),
        ('Стрел(?:|а|е|ы) молни(?:|и|й)', {'link': 'Стрела молнии'}),
        ('Поток(?:|а) молни(?:|и|й)', {'link': 'Поток молний'}),
        ('Круг(?:|а) молни(?:|и|й)', {'link': 'Круг молний'}),
        ('Удар(?:|а) молни(?:|и|й)', {'link': 'Удар молнии'}),
        ('Побег(?:|и|ов) молни(?:|и|й)', {'link': 'Побеги молний'}),
        ('Ловушк(?:|а|и) молни(?:|и|й)', {'link': 'Ловушка молний'}),
        ('Грозов(?:|ой|ого) переход(?:|а)', {'link': 'Грозовой переход'}),
        ('Магмов(?:|ый|ого) шар(?:|а)', {'link': 'Магмовый шар'}),
        ('Стрел(?:|а|е|ы)-двойник(?:|а|у)', {'link': 'Стрела-двойник'}),
        ('Расплавленн(?:|ый|ого) панцир(?:|ь|я)',
         {'link': 'Расплавленный панцирь'}),
        ('Магмов(?:|ый|ого) удар(?:|а)', {'link': 'Магмовый удар'}),
        ('Сфер(?:|а|ы) бурь', {'link': 'Сфера бурь'}),
        ('Призрачн(?:|ый|ого) бег(?:|а)', {'link': 'Призрачный бег'}),
        ('Метк(?:|а|и|ой) браконьера', {'link': 'Метка браконьера'}),
        ('Портал', {'link': 'Портал (камень умения)'}),
        ('Перелив(?:|а|ом) энергии', {'link': 'Перелив энергии'}),
        ('Уязвимост(?:|и|ь|ью) к снарядам', {'link': 'Уязвимость к снарядам'}),
        ('Надрез(?:|а)', {'link': 'Надрез'}),
        ('Наказани(?:|е|я)', {'link': 'Наказание'}),
        ('Спасени(?:|е|я|ем) от стихий', {'link': 'Спасение от стихий'}),
        ('Спасени(?:|е|я|ем) от огня', {'link': 'Спасение от огня'}),
        ('Спасени(?:|е|я|ем) от холода', {'link': 'Спасение от холода'}),
        ('Спасени(?:|е|я|ем) от молни(?:|и|й)', {'link': 'Спасение от молний'}),
        ('Лив(?:|ня|ень) стрел', {'link': 'Ливень стрел'}),
        ('Сотвор(?:|е|ё)н(?:|ие|ием|ные) призрак(?:|а|и|ов)',
         {'link': 'Сотворение призрака'}),
        ('Поднят(?:|ие|ия|ые|ых|ого) зомби', {'link': 'Поднятие зомби'}),
        ('Клич(?:|а) сплочения', {'link': 'Клич сплочения'}),
        ('Опустошени(?:|е|я)', {'link': 'Опустошение'}),
        ('Возмезди(?:|е|я)', {'link': 'Возмездие'}),
        ('Восполняющ(?:|ий|им|его) тотем(?:|а|ом)',
         {'link': 'Восполняющий тотем'}),
        ('Праведн(?:|ый|ого) ог(?:|ня|онь)', {'link': 'Праведный огонь'}),
        ('Праведн(?:|ая|ой) молни(?:|и|я)', {'link': 'Праведная молния'}),
        ('Парировани(?:|е|я)', {'link': 'Парирование'}),
        ('Опаляющ(?:|ий|его|ему) луч(?:|а|у)', {'link': 'Опаляющий луч'}),
        ('Обжигающи(?:|е|х) уз(?:|ы)', {'link': 'Обжигающие узы'}),
        ('Клинки тени', {'link': 'Клинки тени'}),
        ('Удар(?:|а) щитом', {'link': 'Удар щитом'}),
        ('Кольц(?:|а|о|ом) молни(?:|и|й)', {'link': 'Кольцо молний'}),
        ('Сотрясающ(?:|ий|им|его) тотем(?:|а|ом)',
         {'link': 'Сотрясающий тотем'}),
        ('Электризующ(?:|ая|ей) стрел(?:|а|ы)',
         {'link': 'Электризующая стрела'}),
        ('Осадн(?:|ая|ой) баллист(?:|а|ы)', {'link': 'Осадная баллиста'}),
        ('Дымов(?:|ая|ой) мин(?:|а|ы)', {'link': 'Дымовая мина'}),
        ('Искр(?:|а|ы)', {'link': 'Искра'}),
        ('Призрачн(?:|ый|ого) брос(?:|ок|ка)', {'link': 'Призрачный бросок'}),
        ('Подношени(?:|е|я) духа', {'link': 'Подношение духа'}),
        ('Расколот(?:|ая|ой) стрел(?:|а|е|ы)', {'link': 'Расколотая стрела'}),
        ('Статичн(?:|ый|ого) разряд(?:|а)', {'link': 'Статичный разряд'}),
        ('Статичная связь', {'link': 'Статичная связь'}),
        ('Грозов(?:|ой|ого) взрыв(?:|а)', {'link': 'Грозовой взрыв'}),
        ('Призыв(?:|а) бури', {'link': 'Призыв бури'}),
        ('(?:Призыв |Призванные |)голем(?:|а|ы|ов|ами) хаоса',
         {'link': 'Призыв голема хаоса'}),
        ('(?:Призыв |Призванные |)трупн(?:|ые|ый|ого|ыми) голем(?:|а|ы|ов|ами)',
         {'link': 'Призыв трупного голема'}),
        ('(?:Призыв |Призванные |)голем(?:|а|ы|ов|ами) огня',
         {'link': 'Призыв голема огня'}),
        ('(?:Призыв |Призванные |)голем(?:|а|ы|ов|ами) льда',
         {'link': 'Призыв голема льда'}),
        ('(?:Призыв |Призванные |)голем(?:|а|ы|ов|ами) молнии',
         {'link': 'Призыв голема молнии'}),
        ('Приз(?:|ванные|ванных|ыв|ыва) неистов(?:|ые|ых|ого) дух(?:|а|и|ов)',
         {'link': 'Призыв неистового духа'}),
        ('Сотворен(?:|ие|ия|ного|ные) скелет(?:|а|ы|ов)',
         {'link': 'Сотворение скелетов'}),
        (
        '(?:Призыв |Призванные |)каменн(?:|ые|ый|ых|ого|ыми) голем(?:|а|ы|ов|ами)',
        {'link': 'Призыв каменного голема'}),
        ('Раскол(?:|а|у)', {'link': 'Раскол'}),
        ('Кругов(?:|ой|ым|ого|ому) взмах(?:|а|у|ом)',
         {'link': 'Круговой взмах'}),
        ('Щит(?:|а|у) бури', {'link': 'Щит бури'}),
        ('Пут(?:|ы|ами) времени', {'link': 'Путы времени'}),
        ('Вихр(?:|ь|я) стрел', {'link': 'Вихрь стрел'}),
        ('Цепь молний ваал', {'link': 'Цепь молний ваал'}),
        ('Горящая стрела ваал', {'link': 'Горящая стрела ваал'}),
        ('Ясность ума ваал', {'link': 'Ясность ума ваал'}),
        ('Укус стужи ваал', {'link': 'Укус стужи ваал'}),
        ('Вихрь ваал', {'link': 'Вихрь ваал'}),
        ('Подрыв трупа ваал', {'link': 'Подрыв трупа ваал'}),
        ('Дисциплина ваал', {'link': 'Дисциплина ваал'}),
        ('Двойной удар ваал', {'link': 'Двойной удар ваал'}),
        ('Огненная ловушка ваал', {'link': 'Огненная ловушка ваал'}),
        ('Огненный шар ваал', {'link': 'Огненный шар ваал'}),
        ('Пламенный взрыв ваал', {'link': 'Пламенный взрыв ваал'}),
        ('Леденящий молот ваал', {'link': 'Леденящий молот ваал'}),
        ('Грация ваал', {'link': 'Грация ваал'}),
        ('Сотрясение ваал', {'link': 'Сотрясение ваал'}),
        ('Спешка ваал', {'link': 'Спешка ваал'}),
        ('Тяжелый удар ваал', {'link': 'Тяжелый удар ваал'}),
        ('Кольцо льда ваал', {'link': 'Кольцо льда ваал'}),
        ('Призыв к бессмертию ваал', {'link': 'Призыв к бессмертию ваал'}),
        ('Удар молнии ваал', {'link': 'Удар молнии ваал'}),
        ('Ловушка молний ваал', {'link': 'Ловушка молний ваал'}),
        ('Грозовой переход ваал', {'link': 'Грозовой переход ваал'}),
        ('Расплавленный панцирь ваал', {'link': 'Расплавленный панцирь ваал'}),
        ('Перелив энергии ваал', {'link': 'Перелив энергии ваал'}),
        ('Ливень стрел ваал', {'link': 'Ливень стрел ваал'}),
        ('Опустошение ваал', {'link': 'Опустошение ваал'}),
        ('Праведный огонь ваал', {'link': 'Праведный огонь ваал'}),
        ('Искра ваал', {'link': 'Искра ваал'}),
        ('Призрачный бросок ваал', {'link': 'Призрачный бросок ваал'}),
        ('Призыв бури ваал', {'link': 'Призыв бури ваал'}),
        ('Сотворение скелетов ваал', {'link': 'Сотворение скелетов ваал'}),
        ('Круговой взмах ваал', {'link': 'Круговой взмах ваал'}),
        ('Отмщени(?:|е|я)', {'link': 'Отмщение'}),
        ('Расчётлив(?:|ый|ого) удар(?:|а)', {'link': 'Расчётливый удар'}),
        ('Удар(?:|а) гадюки', {'link': 'Удар гадюки'}),
        ('Живучест(?:|и|ь|ью)', {'link': 'Живучесть'}),
        ('Пург(?:|а|и)', {'link': 'Пурга'}),
        ('Беззащитност(?:|и|ь|ью)', {'link': 'Беззащитность'}),
        ('Метк(?:|а|и|ой) вождя', {'link': 'Метка вождя'}),
        ('Шквал(?:|а) клинков', {'link': 'Шквал клинков'}),
        ('Шальн(?:|ой|ого) удар(?:|а)', {'link': 'Шальной удар'}),
        ('Увядани(?:|е|я)', {'link': 'Увядание'}),
        ('Грозн(?:|ый|ым|ого) гнев(?:|а|ом)', {'link': 'Грозный гнев'}),
        #
        # Enchantment skills
        #
        ('Приказ(?:|а) клинков', {'link': 'Приказ клинков'}),
        ('Приказ(?:|а) огня', {'link': 'Приказ огня'}),
        ('Приказ(?:|а) силы', {'link': 'Приказ силы'}),
        ('Приказ(?:|а) холода', {'link': 'Приказ холода'}),
        ('Приказ(?:|а) ярости', {'link': 'Приказ ярости'}),
        ('Приказ(?:|а) ада', {'link': 'Приказ ада'}),
        ('Приказ(?:|а) гнева', {'link': 'Приказ гнева'}),
        ('Приказ(?:|а) света', {'link': 'Приказ света'}),
        ('Приказ(?:|а) отражения', {'link': 'Приказ отражения'}),
        ('Приказ(?:|а) злобы', {'link': 'Приказ злобы'}),
        ('Приказ(?:|а) грома', {'link': 'Приказ грома'}),
        ('Приказ(?:|а) войны', {'link': 'Приказ войны'}),
        ('Приказ(?:|а) зимы', {'link': 'Приказ зимы'}),
        ('Приказ(?:|а) смерти', {'link': 'Приказ смерти'}),
        ('Приказ(?:|а) бури', {'link': 'Приказ бури'}),
        ('Указ(?:|а) клинков', {'link': 'Указ клинков'}),
        ('Указ(?:|а) огня', {'link': 'Указ огня'}),
        ('Указ(?:|а) силы', {'link': 'Указ силы'}),
        ('Указ(?:|а) холода', {'link': 'Указ холода'}),
        ('Указ(?:|а) ярости', {'link': 'Указ ярости'}),
        ('Указ(?:|а) ада', {'link': 'Указ ада'}),
        ('Указ(?:|а) гнева', {'link': 'Указ гнева'}),
        ('Указ(?:|а) света', {'link': 'Указ света'}),
        ('Указ(?:|а) отражения', {'link': 'Указ отражения'}),
        ('Указ(?:|а) злобы', {'link': 'Указ злобы'}),
        ('Указ(?:|а) грома', {'link': 'Указ грома'}),
        ('Указ(?:|а) войны', {'link': 'Указ войны'}),
        ('Указ(?:|а) зимы', {'link': 'Указ зимы'}),
        ('Указ(?:|а) смерти', {'link': 'Указ смерти'}),
        ('Указ(?:|а) бури', {'link': 'Указ бури'}),
        ('Эдикт(?:|а) клинков', {'link': 'Эдикт клинков'}),
        ('Эдикт(?:|а) огня', {'link': 'Эдикт огня'}),
        ('Эдикт(?:|а) силы', {'link': 'Эдикт силы'}),
        ('Эдикт(?:|а) холода', {'link': 'Эдикт холода'}),
        ('Эдикт(?:|а) ярости', {'link': 'Эдикт ярости'}),
        ('Эдикт(?:|а) ада', {'link': 'Эдикт ада'}),
        ('Эдикт(?:|а) гнева', {'link': 'Эдикт гнева'}),
        ('Эдикт(?:|а) света', {'link': 'Эдикт света'}),
        ('Эдикт(?:|а) отражения', {'link': 'Эдикт отражения'}),
        ('Эдикт(?:|а) злобы', {'link': 'Эдикт злобы'}),
        ('Эдикт(?:|а) грома', {'link': 'Эдикт грома'}),
        ('Эдикт(?:|а) войны', {'link': 'Эдикт войны'}),
        ('Эдикт(?:|а) зимы', {'link': 'Эдикт зимы'}),
        ('Эдикт(?:|а) смерти', {'link': 'Эдикт смерти'}),
        ('Эдикт(?:|а) бури', {'link': 'Эдикт бури'}),
        ('Слов(?:|а|о) клинков', {'link': 'Слово клинков'}),
        ('Слов(?:|а|о) огня', {'link': 'Слово огня'}),
        ('Слов(?:|а|о) силы', {'link': 'Слово силы'}),
        ('Слов(?:|а|о) холода', {'link': 'Слово холода'}),
        ('Слов(?:|а|о) ярости', {'link': 'Слово ярости'}),
        ('Слов(?:|а|о) ада', {'link': 'Слово ада'}),
        ('Слов(?:|а|о) гнева', {'link': 'Слово гнева'}),
        ('Слов(?:|а|о) света', {'link': 'Слово света'}),
        ('Слов(?:|а|о) отражения', {'link': 'Слово отражения'}),
        ('Слов(?:|а|о) злобы', {'link': 'Слово злобы'}),
        ('Слов(?:|а|о) грома', {'link': 'Слово грома'}),
        ('Слов(?:|а|о) войны', {'link': 'Слово войны'}),
        ('Слов(?:|а|о) зимы', {'link': 'Слово зимы'}),
        ('Слов(?:|а|о) смерти', {'link': 'Слово смерти'}),
        ('Слов(?:|а|о) бури', {'link': 'Слово бури'}),
        #
        # Support gems
        #
        ('Уроном хаосом (?:[0-9]+ уровня)', {'link': 'Урон хаосом'}),
        ('Уроном холодом  (?:[0-9]+ уровня)', {'link': 'Урон холодом'}),
        ('(?:Уроном от огня|Уроном огнем) (?:[0-9]+ уровня)',
         {'link': 'Урон огнем'}),
        ('(?:Уроном от молнии|Уроном молнией) (?:[0-9]+ уровня)',
         {'link': 'Урон молнией'}),
        ('Меткостью (?:[0-9]+ уровня)', {'link': 'Меткость'}),
        (
        'Колдовским выбросом (?:[0-9]+ уровня)', {'link': 'Колдовской выброс'}),
        ('Богохульством (?:[0-9]+ уровня)', {'link': 'Богохульство'}),
        ('Ослеплением (?:[0-9]+ уровня)', {'link': 'Ослепление'}),
        ('Затруднением блока (?:[0-9]+ уровня)', {'link': 'Затруднение блока'}),
        ('Магией крови (?:[0-9]+ уровня)', {'link': 'Магия крови'}),
        ('Жаждой крови (?:[0-9]+ уровня)', {'link': 'Жажда крови'}),
        ('Жестокостью (?:[0-9]+ уровня)', {'link': 'Жестокость'}),
        ('Уроном от горения (?:[0-9]+ уровня)', {'link': 'Урон от горения'}),
        ('Сотворением чар при критическом ударе (?:[0-9]+ уровня)',
         {'link': 'Сотворение чар при критическом ударе'}),
        ('Сотворением чар при смерти (?:[0-9]+ уровня)',
         {'link': 'Сотворение чар при смерти'}),
        ('Сотворением чар при убийстве в ближнем бою (?:[0-9]+ уровня)',
         {'link': 'Сотворение чар при убийстве в ближнем бою'}),
        ('Сотворением чар при получении урона (?:[0-9]+ уровня)',
         {'link': 'Сотворение чар при получении урона'}),
        ('Сотворением чар при оглушении (?:[0-9]+ уровня)',
         {'link': 'Сотворение чар при оглушении'}),
        ('Сотворением чар при поддержании (?:[0-9]+ уровня)',
         {'link': 'Сотворение чар при поддержании'}),
        ('Цепью (?:[0-9]+ уровня)', {'link': 'Цепь'}),
        (
        'Шансом кровотечения (?:[0-9]+ уровня)', {'link': 'Шанс кровотечения'}),
        ('Паникой (?:[0-9]+ уровня)', {'link': 'Паника'}),
        ('Воспламенением (?:[0-9]+ уровня)', {'link': 'Воспламенение'}),
        ('Кассетными ловушками (?:[0-9]+ уровня)',
         {'link': 'Кассетные ловушки'}),
        ('Пронизывающим холодом (?:[0-9]+ уровня)',
         {'link': 'Пронизывающий холод'}),
        ('Холодом в огонь (?:[0-9]+ уровня)', {'link': 'Холод в огонь'}),
        ('Средоточием (?:[0-9]+ уровня)', {'link': 'Средоточие'}),
        ('Контролируемым разрушением (?:[0-9]+ уровня)',
         {'link': 'Контролируемое разрушение'}),
        ('Добиванием (?:[0-9]+ уровня)', {'link': 'Добивание'}),
        ('Проклятием при попадании (?:[0-9]+ уровня)',
         {'link': 'Проклятие при попадании'}),
        ('Уроном при полном здоровье (?:[0-9]+ уровня)',
         {'link': 'Урон при полном здоровье'}),
        ('Смертельными состояниями (?:[0-9]+ уровня)',
         {'link': 'Смертельные состояния'}),
        ('Разложением (?:[0-9]+ уровня)', {'link': 'Разложение'}),
        ('Эффективностью (?:[0-9]+ уровня)', {'link': 'Эффективность'}),
        ('Концентрацией стихий (?:[0-9]+ уровня)',
         {'link': 'Концентрация стихий'}),
        ('Разгулом стихий (?:[0-9]+ уровня)', {'link': 'Разгул стихий'}),
        ('Усилителем (?:[0-9]+ уровня)', {'link': 'Усилитель'}),
        ('Зарядом выносливости при оглушении в ближнем бою (?:[0-9]+ уровня)',
         {'link': 'Заряд выносливости при оглушении в ближнем бою'}),
        ('Улучшителем (?:[0-9]+ уровня)', {'link': 'Улучшитель'}),
        ('Наставником (?:[0-9]+ уровня)', {'link': 'Наставник'}),
        ('Уроном от стихий атаками (?:[0-9]+ уровня)',
         {'link': 'Урон от стихий атаками'}),
        ('Ускорением атак (?:[0-9]+ уровня)', {'link': 'Ускорение атак'}),
        ('Ускоренным сотворением чар (?:[0-9]+ уровня)',
         {'link': 'Ускоренное сотворение чар'}),
        ('Ускорением снарядов (?:[0-9]+ уровня)',
         {'link': 'Ускорение снарядов'}),
        (
        'Пронизывающим жаром (?:[0-9]+ уровня)', {'link': 'Пронизывающий жар'}),
        ('Разветвлением (?:[0-9]+ уровня)', {'link': 'Разветвление'}),
        ('Укреплением (?:[0-9]+ уровня)', {'link': 'Укрепление'}),
        ('Щедростью (?:[0-9]+ уровня)', {'link': 'Щедрость'}),
        ('Множеством дополнительных снарядов (?:[0-9]+ уровня)',
         {'link': 'Много дополнительных снарядов'}),
        ('Переохлаждением (?:[0-9]+ уровня)', {'link': 'Переохлаждение'}),
        ('Укусом Льда (?:[0-9]+ уровня)', {'link': 'Укус льда'}),
        ('Расширенной областью действия (?:[0-9]+ уровня)',
         {'link': 'Расширенная область действия'}),
        ('Усилением критических ударов (?:[0-9]+ уровня)',
         {'link': 'Усиление критических ударов'}),
        ('Учащением критических ударов (?:[0-9]+ уровня)',
         {'link': 'Учащение критических ударов'}),
        ('Продлением (?:[0-9]+ уровня)', {'link': 'Продление'}),
        ('Возбуждением (?:[0-9]+ уровня)', {'link': 'Возбуждение'}),
        ('Распространением поджога (?:[0-9]+ уровня)',
         {'link': 'Распространение поджога'}),
        ('Железной хваткой (?:[0-9]+ уровня)', {'link': 'Железная хватка'}),
        ('Железной волей (?:[0-9]+ уровня)', {'link': 'Железная воля'}),
        ('Количеством предметов (?:[0-9]+ уровня)',
         {'link': 'Количество предметов'}),
        ('Редкостью предметов (?:[0-9]+ уровня)',
         {'link': 'Редкость предметов'}),
        ('Жертвенностью (?:[0-9]+ уровня)', {'link': 'Жертвенность'}),
        ('Отбрасыванием (?:[0-9]+ уровня)', {'link': 'Отбрасывание'}),
        ('Сокращением (?:[0-9]+ уровня)', {'link': 'Сокращение'}),
        ('Дополнительными снарядами (?:[0-9]+ уровня)',
         {'link': 'Дополнительные снаряды'}),
        ('Меньшим ядом (?:[0-9]+ уровня)', {'link': 'Меньший яд'}),
        ('Здоровьем за удар (?:[0-9]+ уровня)', {'link': 'Здоровье за удар'}),
        ('(?:Похищением|Вытягиванием) здоровья (?:[0-9]+ уровня)',
         {'link': 'Вытягивание здоровья'}),
        ('Пронизывающими молниями (?:[0-9]+ уровня)',
         {'link': 'Пронизывающие молнии'}),
        ('Увечьем (?:[0-9]+ уровня)', {'link': 'Увечье'}),
        ('(?:Похищением|Вытягиванием) маны (?:[0-9]+ уровня)',
         {'link': 'Вытягивание маны'}),
        ('Физическим урон ближнего боя (?:[0-9]+ уровня)',
         {'link': 'Физический урон ближнего боя'}),
        ('Раскатистым ударом (?:[0-9]+ уровня)', {'link': 'Раскатистый удар'}),
        ('Минным полем (?:[0-9]+ уровня)', {'link': 'Минное поле'}),
        (
        'Уроном приспешников (?:[0-9]+ уровня)', {'link': 'Урон приспешников'}),
        ('Здоровьем приспешников (?:[0-9]+ уровня)',
         {'link': 'Здоровье приспешников'}),
        ('Скоростью приспешников (?:[0-9]+ уровня)',
         {'link': 'Скорость приспешников'}),
        ('Стихийным войском (?:[0-9]+ уровня)', {'link': 'Стихийное войско'}),
        ('Дополнительными ловушками (?:[0-9]+ уровня)',
         {'link': 'Дополнительные ловушки'}),
        ('Градом ударов (?:[0-9]+ уровня)', {'link': 'Град ударов'}),
        ('Боевым ражем (?:[0-9]+ уровня)', {'link': 'Боевой раж'}),
        ('Яростными снарядами (?:[0-9]+ уровня)', {'link': 'Яростные снаряды'}),
        ('Физическим уроном в молнии (?:[0-9]+ уровня)',
         {'link': 'Физический урон в молнии'}),
        ('Пронзанием (?:[0-9]+ уровня)', {'link': 'Пронзание'}),
        ('Стрельбой в упор (?:[0-9]+ уровня)', {'link': 'Стрельба в упор'}),
        ('Ядом (?:[0-9]+ уровня)', {'link': 'Яд'}),
        ('Зарядом энергии при критическом ударе (?:[0-9]+ уровня)',
         {'link': 'Энергетический заряд при критическом ударе'}),
        ('Тотемом-баллистой (?:[0-9]+ уровня)', {'link': 'Тотем-баллиста'}),
        ('Вдохновением (?:[0-9]+ уровня)', {'link': 'Вдохновение'}),
        ('Цепным подрывом (?:[0-9]+ уровня)', {'link': 'Цепной подрыв'}),
        ('Возвращающимися снарядами (?:[0-9]+ уровня)',
         {'link': 'Возвращающиеся снаряды'}),
        ('Беспощадностью (?:[0-9]+ уровня)', {'link': 'Беспощадность'}),
        ('Замедленными снарядами (?:[0-9]+ уровня)',
         {'link': 'Замедленные снаряды'}),
        ('Эхом (?:магии|чар) (?:[0-9]+ уровня)', {'link': 'Эхо магии'}),
        ('Колдующим тотемом (?:[0-9]+ уровня)', {'link': 'Колдующий тотем'}),
        ('Разделением снарядов (?:[0-9]+ уровня)',
         {'link': 'Разделение снарядов'}),
        ('Оглушением (?:[0-9]+ уровня)', {'link': 'Оглушение'}),
        ('Стремительным недугом (?:[0-9]+ уровня)',
         {'link': 'Стремительный недуг'}),
        ('Ловушкой (?:[0-9]+ уровня)', {'link': 'Ловушка'}),
        ('Улучшенными ловушками (?:[0-9]+ уровня)',
         {'link': 'Улучшенные ловушки'}),
        ('Уроном ловушек и мин (?:[0-9]+ уровня)',
         {'link': 'Урон ловушек и мин'}),
        ('Безграничными состояниями (?:[0-9]+ уровня)',
         {'link': 'Безграничные состояния'}),
        ('Едкими токсинами (?:[0-9]+ уровня)', {'link': 'Едкие токсины'}),
        ('Манипуляцией пустотой (?:[0-9]+ уровня)',
         {'link': 'Манипуляция пустотой'}),
        ('Быстрой сборкой (?:[0-9]+ уровня)', {'link': 'Быстрая сборка'}),
        ('Зовом предков (?:[0-9]+ уровня)', {'link': 'Зов предков'}),
        ('Кольцом стрел (?:[0-9]+ уровня)', {'link': 'Кольцо стрел'}),
        ('Очередью (?:[0-9]+ уровня)', {'link': 'Очередь'}),
        ('Ударной волной (?:[0-9]+ уровня)', {'link': 'Ударная волна'}),
        ('Леденящим охлаждением (?:[0-9]+ уровня)',
         {'link': 'Леденящее охлаждение'}),
        ('Пылающим легионом (?:[0-9]+ уровня)', {'link': 'Пылающий легион'}),
        ('Заряженными минами (?:[0-9]+ уровня)', {'link': 'Заряженные мины'}),
        ('Губительным прикосновением (?:[0-9]+ уровня)',
         {'link': 'Губительное прикосновение'}),
        ('Похищением энергетического щита (?:[0-9]+ уровня)',
         {'link': 'Похищение энергетического щита'}),
        (
        'Призрачным лучником (?:[0-9]+ уровня)', {'link': 'Призрачный лучник'}),
        ('Большим залпом (?:[0-9]+ уровня)', {'link': 'Большой залп'}),
        ('Высвобождением (?:[0-9]+ уровня)', {'link': 'Высвобождение'}),
        ('Интенсивностью (?:[0-9]+ уровня)', {'link': 'Интенсивность'}),
        ('Проколом (?:[0-9]+ уровня)', {'link': 'Прокол'}),
        ('пробуждённым Уроном хаосом (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Урон хаосом'}),
        ('пробуждённым Уроном холодом (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Урон холодом'}),
        ('пробуждённым Уроном огнём (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Урон огнем'}),
        ('пробуждённым Уроном молнией (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Урон молнией'}),
        ('пробуждённым Зовом предков (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Зов предков'}),
        ('пробуждённым Кольцом стрел (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Кольцом стрел'}),
        ('пробуждённым Богохульством (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Богохульство'}),
        ('пробуждённой Жестокостью (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Жестокость'}),
        ('пробуждённым Уроном от горения (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Урон от горения'}),
        ('пробуждённым Сотворением чар при критическом ударе (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Сотворение чар при критическом ударе'}),
        ('пробуждённым Сотворением чар при поддержании (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Сотворение чар при поддержании'}),
        (
        'пробуждённой Цепью (?:[0-9]+ уровня)', {'link': 'Пробужденный: Цепь'}),
        ('пробуждённым Пронизывающим холодом (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Пронизывающий холод'}),
        ('пробуждённым Контролируемым разрушением (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Контролируемое разрушение'}),
        ('пробуждённым Проклятием при попадании (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Проклятие при попадании'}),
        ('пробуждёнными Смертельными состояниями (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Смертельные состояния'}),
        ('пробуждённой Концентрацией стихий (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Концентрация стихий'}),
        ('пробуждённым Пронизывающим жаром (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Пронизывающий жар'}),
        ('пробуждённым Разветвлением (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Разветвление'}),
        ('пробуждённой Щедростью (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Щедрость'}),
        ('пробуждёнными Многими дополнительными снарядами (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Много дополнительных снарядов'}),
        ('пробуждённой Расширенной областью действия (?:[0-9]+ уровня)',
         {'link': 'Пробужденный: Расширенная область действия'}),
        #
        # Groups
        #
        # ('Physical(?:Skill|Gem)', {'link': 'Physical Skills'}),
        ('умен(?:|ие|ий|ия|иями) огня', {'link': 'Умения огня'}),
        ('умен(?:|ие|ий|ия|иями) холода', {'link': 'Умения холода'}),
        ('умен(?:|ие|ий|ия|иями) молнии', {'link': 'Умения молнии'}),
        ('умен(?:|ие|ий|ия|иями) хаоса ', {'link': 'Умения хаоса'}),
        # ('Area (?:Skill|Gem)', {'link': 'Area Skills'}),
        (
        'умен(?:|ие|ий|ия|иями) ближнего боя', {'link': 'Умения ближнего боя'}),
        ('умен(?:|ие|ий|ия|иями) луков', {'link': 'Умения луков'}),
        (
        'умен(?:|ие|ий|ия|иями) приспешников', {'link': 'Умения приспешников'}),
        ('умен(?:|ие|ий|ия|иями) обороны', {'link': 'Умения обороны'}),
        (
        'умен(?:|ие|ий|ия|иями) передвижения', {'link': 'Умения передвижения'}),
        ('поддерживаем(?:|ое|ые|ых|ыми) умен(?:|ие|ий|ия|иями)',
         {'link': 'Поддерживаемые умения'}),
        ('умен(?:|ие|ий|ия|иями) атак', {'link': 'Умения атак'}),
        ('умен(?:|ие|ий|ия|иями) чар', {'link': 'Умения чар'}),
        ('умен(?:|ие|ий|ия|иями) аур', {'link': 'Умения аур'}),
        ('умен(?:|ие|ий|ия|иями) клейм(?:|а)', {'link': 'Умения клейм'}),
        ('умен(?:|ие|ий|ия|иями) знамён', {'link': 'Умения знамён'}),
        ('умен(?:|ие|ий|ия|иями) подношений', {'link': 'Умения подношений'}),
        ('умен(?:|ие|ий|ия|иями) вестников', {'link': 'Умения вестников'}),

        #
        # Damage
        #
        # Base types
        ('урон(?:|а|ом) хаосом', {'link': 'Урон от хаоса'}),
        ('урон(?:|а|ом) от холода', {'link': 'Урон от холода'}),
        ('урон(?:|а|ом) от огня', {'link': 'Урон от огня'}),
        ('урон(?:|а|ом) от молнии', {'link': 'Урон от молнии'}),
        ('физическ(?:|ий|им|ого) урон(?:|а|ом)', {'link': 'Физический урон'}),
        # Mixed and special
        ('урон(?:|а) от атак', {'link': 'Урон от атак'}),
        ('урон(?:|а) от чар', {'link': 'Урон от чар'}),
        ('урон(?:|а) от стихий', {'link': 'Урон от стихий'}),
        ('урон(?:|а) приспешников', {'link': 'Урон приспешников'}),

        #
        # Armour & weapon types
        #

        # Generic
        ('двуручн(?:|ое|ым|ого) оружи(?:|е|я|ем) ближнего боя',
         {'link': 'Двуручное оружие ближнего боя'}),

        # Armour
        ('щит(?:|а|ы|ом)', {'link': 'Щит'}),

        # Melee
        ('топор(?:|ы|ом|ами)', {'link': 'Топор'}),
        ('когт(?:|и|ей|ями)', {'link': 'Когти'}),
        ('кинжал(?:|ы|ом|ами)', {'link': 'Кинжал'}),
        ('булав(?:|а|ой|ами)', {'link': 'Булава'}),
        ('скипетр(?:|а|ом|ами)', {'link': 'Скипетр'}),
        ('посох(?:|а|ом|ами)', {'link': 'Посох'}),
        ('меч(?:|а|ом|ами)', {'link': 'Меч'}),

        # Range
        ('лук(?:|ов|ами)', {'link': 'Лук'}),
        ('жезл(?:|ом|ами)', {'link': 'Жезл'}),

        #
        # Status
        #
        ('шок(?:|а|у|ом)', {'link': 'Шок'}),
        (
        'поджог(?:|а|е|и|у)|подожж(?:|ен|ён|ены|енного|ённого|енные|ённые|енным|ённым|енных|ённых)',
        {'link': 'Поджог'}),
        (
        'заморо(?:|жен|зка|зке|зки|зку|зить|зили|женные|женным|женных|женного)',
        {'link': 'Заморозка'}),
        (
        'яд(?:|а|у|ом)|отрав(?:|ить|лены|ление|ления|ленные|ленным|ленных|ляются|ленного)',
        {'link': 'Отравление'}),

        #
        # Misc
        #
        ('прокля(?:|т|ты|сть|тие|тия|тий|тым|того|тому|тыми|тием)',
         {'link': 'Проклятие'}),
        ('гн(?:|е|ё)зд(?:|а|о|ах)', {'link': 'Гнездо предмета'}),
        ('недавно', {'link': 'Недавно'}),
        ('умени(?:|е|й|я|ем)', {'link': 'Умения'}),
        ('чар(?:|ы|ами)', {'link': 'Чары'}),
        ('атак(?:|а|и)', {'link': 'Атака'}),
        ('приспешник(?:|а|и|ам|ах|ов|ами)', {'link': 'Приспешник'}),
        ('мин(?:|а|у|ы|ами)', {'link': 'Мина'}),
        ('тотем(?:|а|ы|ов|ами)', {'link': 'Тотем'}),
        ('ловуш(?:|ка|ки|ек|ками)', {'link': 'Ловушки'}),
        ('парн(?:|ое|ым|ого) оружи(?:|е|я|ем)|парными',
         {'link': 'Парное оружие'}),
        ('уров(?:|ня|ень)', {'link': 'Уровень'}),
        # ('PvP', {'link': 'PvP'}),
        ('удар(?:|а|е|ов|ами)', {'link': 'Удар'}),
        ('убийств(?:|а|е|о)|убиваете|убит(?:|ые)', {'link': 'Убийство'}),
        ('заряд(?:|а|ы|ов|ами)', {'link': 'Заряд'}),
        ('удач(?:|а|лив|ливы)', {'link': 'Удача'}),
        ('неудач(?:|а|лив|ливы)', {'link': 'Неудача'}),
        ('двойной урон', {'link': 'Двойной урон'}),
        ('снаряды кольцом', {'link': 'Кольцо снарядов'}),
        ('чар(?:|ы) колец', {'link': 'Чары колец'}),
    ),
}

'''_inter_wiki_re = re.compile(
    r'(?: |^)(?P<text>%s))' % '|'.join([item[0] for item in _inter_wiki_map]),
    re.UNICODE | re.IGNORECASE
)'''

_MAX_RE = 97


def _make_inter_wiki_re():
    out = {}
    for language, _inter_wiki_mapping in _inter_wiki_map.items():
        out[language] = []
        for i in range(0, (len(_inter_wiki_mapping)//_MAX_RE)+1):
            id = i*_MAX_RE
            out[language].append(re.compile(
                r'(?![^\[]*\]\])'
                r'(?: |^)'
                r'(?P<text>%s)'
                r'(?= |$)' %
                '|'.join(['(%s)' % item[0] for item in _inter_wiki_mapping[id:id+_MAX_RE]]),
                re.UNICODE | re.IGNORECASE,
            ))
    return out

_inter_wiki_re = _make_inter_wiki_re()

# =============================================================================
# Classes
# =============================================================================


class BaseParser:
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

    _HIDDEN_FORMAT = {
        'English': '%s (Hidden)',
        'German': '%s (nicht sichtbar)',
        'Russian': '%s (скрытый)',
    }
    _MISSING_MSG = 'Several arguments have not been found:\n%s'

    _files = []
    _translations = []

    def __init__(self, base_path, parsed_args):
        self.parsed_args = parsed_args
        # Make sure to load the appropriate version of the specification
        set_default_spec(version=config.get_option('version'))

        self.base_path = base_path

        opt = {
            'use_dat_value': False,
            'auto_build_index': True,
        }

        # Load rr and translations which will be undoubtedly be needed for
        # parsing
        self.rr = RelationalReader(
            path_or_ggpk=base_path,
            files=self._files,
            read_options=opt,
            raise_error_on_missing_relation=False,
            language=config.get_option('language'),
        )
        install_data_dependant_quantifiers(self.rr)
        self.tc = TranslationFileCache(path_or_ggpk=base_path)
        for file_name in self._translations:
            self.tc[file_name]

        self.ot = OTFileCache(path_or_ggpk=base_path)

        self.custom = get_custom_translation_file()

        self.ggpk = None
        self._img_path = None
        self.lang = config.get_option('language')

    def _column_index_filter(self, dat_file_name, column_id, arg_list,
                             error_msg=_MISSING_MSG):
        self.rr[dat_file_name].build_index(column_id)

        rows = []
        missing = []

        if column_id in self.rr[dat_file_name].columns_unique:
            func = rows.append
        else:
            func = rows.extend

        for argument in arg_list:
            if argument in self.rr[dat_file_name].index[column_id]:
                func(
                    self.rr[dat_file_name].index[column_id][argument]
                )
            else:
                missing.append(argument)

        if missing:
            console(
                self._MISSING_MSG % '\n'.join(missing), msg=Msg.warning
            )

        return rows

    def _format_lines(self, lines):
        return '<br>'.join(lines).replace('\n', '<br>')

    def _format_wiki_title(self, title):
        return title.replace('_', '~').replace('~~~', '_~~_~~_')

    def _format_hidden(self, custom):
        return self._HIDDEN_FORMAT[self.lang] % make_inter_wiki_links(custom)

    def _format_detailed(self, custom, ingame):
        return self._DETAILED_FORMAT % (
            ingame,
            make_inter_wiki_links(custom)
        )

    def _write_dds(self, data, out_path, parsed_args):
        with open(out_path, 'wb') as f:
            f.write(extract_dds(
                data,
                path_or_ggpk=self.ggpk,
            ))

            console('Wrote "%s"' % out_path)

        if not parsed_args.convert_images:
            return

        os.system('magick convert "%s" "%s"' % (
            out_path, out_path.replace('.dds', '.png'),
        ))
        os.remove(out_path)

        console('Converted "%s" to png' % out_path)

    def _load_ggpk(self):
        if self.ggpk is None:
            self.ggpk = GGPKFile()
            self.ggpk.read(get_content_ggpk_path())
            self.ggpk.directory_build()
            console('content.ggpk has been loaded.')

    def _image_init(self, parsed_args):
        if parsed_args.store_images:
            console(
                'Images are flagged for extraction. Loading content.ggpk '
                '...'
            )
            self._load_ggpk()

            self._img_path = os.path.join(self.base_path, 'img')
            if not os.path.exists(self._img_path):
                os.makedirs(self._img_path)

    def _get_stats(self, stats=None, values=None, mod=None,
                   translation_file=None):
        if translation_file is None:
            if mod is None:
                raise ValueError(
                    'Can not automatically determine translation file if mod '
                    'is not set'
                )
            else:
                translation_file = get_translation_file_from_domain(
                    mod['Domain'])
        if stats is None or values is None:
            if mod is None:
                raise ValueError(
                    'Mod must be set if any of stats or values aren\'t set'
                )
            else:
                stats = []
                values = []
                for i in MOD_STATS_RANGE:
                    k = mod['StatsKey%s' % i]
                    if k is None:
                        continue

                    stat = k['Id']
                    value = mod['Stat%sMin' % i], mod['Stat%sMax' % i]

                    if value[0] == 0 and value[1] == 0:
                        continue

                    stats.append(stat)
                    values.append(value)

        result = self.tc[translation_file].get_translation(
            stats, values, full_result=True, lang=self.lang
        )

        if mod and mod['Domain'] == MOD_DOMAIN.MONSTER:
            default = self.tc['stat_descriptions.txt'].get_translation(
                result.source_ids, result.source_values, full_result=True,
                lang=self.lang
            )
            temp_ids = []
            temp_trans = []

            for i, tr in enumerate(default.found):
                for j, tr2 in enumerate(result.found):
                    if tr.ids != tr2.ids:
                        continue

                    r1 = tr.get_language(self.lang).get_string(default.values[i])
                    r2 = tr2.get_language(self.lang).get_string(result.values[j])
                    if r1 and r2 and r1[0] != r2[0]:
                        temp_trans.append(self._format_detailed(r1[0], r2[0]))
                    elif r2 and r2[0]:
                        temp_trans.append(self._format_hidden(r2[0]))
                    temp_ids.append(tr.ids)

                is_missing = False
                for tid in tr.ids:
                    if tid in result.missing_ids:
                        is_missing = True
                        break

                if not is_missing:
                    continue

                r1 = tr.get_language(self.lang).\
                    get_string(default.values[i])
                if r1 and r1[0]:
                    temp_trans.append(self._format_hidden(r1[0]))
                    temp_ids.append(tr.ids)

                for tid in tr.ids:
                    try:
                        i = result.missing_ids.index(tid)
                    except ValueError:
                        continue
                    del result.missing_ids[i]
                    del result.missing_values[i]

            index = 0
            for i, tr in enumerate(result.found):
                try:
                    index = temp_ids.index(tr.ids)
                except ValueError:
                    temp_ids.insert(index, tr.ids)
                    temp_trans.insert(index, make_inter_wiki_links(
                        tr.get_language(self.lang).\
                            get_string(result.values[i])[0]
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
                lang=self.lang,
            )

            if custom_result.missing_ids:
                warnings.warn(
                    'Missing translation for ids %s and values %s' % (
                        custom_result.missing_ids, custom_result.missing_values),
                    MissingIdentifierWarning,
                )

            for line in custom_result.lines:
                if line:
                    out.append(self._HIDDEN_FORMAT[self.lang] % line)

        finalout = []
        for line in out:
            if '\n' in line:
                # By request differentiate between breaks from the source file
                # and different stats
                finalout.append('<br />'.join(line.split('\n')))
            else:
                finalout.append(line)

        return finalout


class TagHandler:
    """
    Provides tag handlers for use with :func:`parse_description_tags`

    Parameters
    ----------
    tag_handlers : dict[str, callable]
        dictionary containing tags and a callable function for passing to
        :func:`parse_description_tags`
    """

    _IL_FORMAT = '{{il|%s|html=}}'
    _C_FORMAT = '{{c|%s|%s}}'

    def __init__(self, rr):
        """
        Parameters
        ----------
        rr : RelationalReader
            RelationalReader instance to use when looking up whether items are
            'real' for linking purposes
        """
        self.rr = rr
        self.rr['BaseItemTypes.dat'].build_index('Name')
        self.rr['Words.dat'].build_index('Text')

        self.tag_handlers = {}
        for key, func in TagHandler.tag_handlers.items():
            self.tag_handlers[key] = partial(func, self)

    def _check_link(self, string):
        items = self.rr['BaseItemTypes.dat'].index['Name'][string]
        if items:
            if items[0]['ItemClassesKey']['Name'] == 'Maps':
                string = self._IL_FORMAT % string
            elif len(items) > 1:
                return '[[%s]]' % string
            else:
                string = self._IL_FORMAT % string
        return string

    def _default_handler(self, hstr, parameter, tid):
        return self._C_FORMAT % (tid, self._check_link(hstr))

    def _link_handler(self, hstr, parameter, tid):
        return self._C_FORMAT % (tid, '[[%s]]' % hstr)

    def _unique_handler(self, hstr, parameter):
        words = self.rr['Words.dat'].index['Text'][hstr]
        if words and words[0]['WordlistsKey'] == WORDLISTS.UNIQUE_ITEM:
            # Check whether unique item name clashes with base item name
            items = self.rr['BaseItemTypes.dat'].index['Name'][hstr]
            if len(items) > 0:
                hstr = '[[%s]]' % hstr
            else:
                hstr = self._IL_FORMAT % hstr
        else:
            hstr = self._check_link(hstr)
        return self._C_FORMAT % ('unique', hstr)

    def _currency_handler(self, hstr, parameter):
        if 'x ' in hstr:
            s = hstr.split('x ', maxsplit=1)
            return self._C_FORMAT % (
                'currency', '%sx %s' % (s[0], self._check_link(s[1]))
            )
        else:
            return self._default_handler(hstr, parameter, 'currency')

    def _pass_through_handler(self, hstr, parameter):
        return hstr

    tag_handlers = {
        'normal': partial(_default_handler, tid='normal'),
        'default': partial(_default_handler, tid='default'),
        'augmented': partial(_default_handler, tid='augmented'),
        'enchanted': partial(_default_handler, tid='enchanted'),

        'size': _pass_through_handler,
        'smaller': _pass_through_handler,

        'gemitem': partial(_default_handler, tid='gem'),
        'currencyitem': _currency_handler,

        'whiteitem': partial(_default_handler, tid='white'),
        'magicitem': partial(_default_handler, tid='magic'),
        'rareitem': partial(_default_handler, tid='rare'),
        'uniqueitem': _unique_handler,

        'divination': partial(_default_handler, tid='divination'),
        'prophecy': partial(_default_handler, tid='prophecy'),

        'corrupted': partial(_link_handler, tid='corrupted'),
    }


class WikiCondition:
    COPY_KEYS = (
    )
    COPY_MATCH = None

    NAME = NotImplemented
    MATCH = None
    INDENT = 33
    ADD_INCLUDE = False

    def __init__(self, data, cmdargs, handler=None):
        self.data = data
        self.cmdargs = cmdargs
        if handler is None:
            self.handler = self._handler
        self.template_arguments = None

    def __call__(self, *args, **kwargs):
        page = kwargs.get('page')

        if page is not None:
            # Abuse this so it can be called as "text" and "condition"
            if self.template_arguments is None:
                self.template_arguments = find_template(
                    page.text(), self.MATCH or self.NAME)
                if len(self.template_arguments['texts']) == 1:
                    self.template_arguments = None
                    return False

                return True

            for k in self.COPY_KEYS:
                try:
                    self.data[k] = self.template_arguments['kwargs'][k]
                except KeyError:
                    pass

            if self.COPY_MATCH:
                for k, v in self.template_arguments['kwargs'].items():
                    if self.COPY_MATCH.match(k):
                        self.data[k] = v

            prefix = ''
            if self.ADD_INCLUDE and '<onlyinclude></onlyinclude>' not in \
                    page.text():
                prefix = '<onlyinclude></onlyinclude>'

            return self.handler(prefix + self.template_arguments['texts'][0] + \
                   self._get_text() + \
                   ''.join(self.template_arguments['texts'][1:]))
        else:
            return self.handler(self._get_text())

    def _handler(self, text):
        return text

    def _get_text(self):
        return format_result_rows(
            parsed_args=self.cmdargs,
            template_name=self.NAME,
            indent=self.INDENT,
            ordered_dict=self.data,
        )

# =============================================================================
# Functions
# =============================================================================


def format_result_rows(parsed_args, ordered_dict, template_name,
                       indent=DEFAULT_INDENT):
    """
    Formats the given result rows as mediawiki template or module.

    Parameters
    ----------
    parsed_args
        argument parser argument containing the format argument
    ordered_dict : OrderedDict
        OrderedDict instance of the rows to format
    template_name : str
        name of the template
    indent : int
        number of spaces to use for indentation/padding up to the given size

    Returns
    -------
    out : str
        formatted string
    """
    if parsed_args.format == 'template':
        out = ['{{%s\n' % template_name]
        for k, v in ordered_dict.items():
            if v is not None:
                out.append(('|{0: <%s}= {1}\n' % indent).format(k, v))
        out.append('}}')
    elif parsed_args.format == 'module':
        ordered_dict['debug_id'] = 1
        out = ['{']
        for k, v in ordered_dict.items():
            if v is not None:
                out.append('{0} = "{1}", '.format(k, v))
        out[-1] = out[-1].strip(', ')
        out.append('}')
    return ''.join(out)


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

    _inter_wiki = _inter_wiki_re.get(config.get_option('language'))

    if _inter_wiki is None:
        return string

    mapping = _inter_wiki_map.get(config.get_option('language'))

    for i, regex in enumerate(_inter_wiki):
        out = []
        last_index = 0
        for match in regex.finditer(string):
            text = match.group('text')
            # Offset by 1 to account for text group
            index = match.groups().index(text, 1)-1
            data = mapping[i*_MAX_RE+index][1]

            out.append(string[last_index:match.start('text')])
            if text == data['link']:
                out.append('[[%s]]' % data['link'])
            else:
                out.append('[[%s|%s]]' % (data['link'], text))

            last_index = match.end('text')

        out.append(string[last_index:])
        string = ''.join(out)

    return string


def find_template(wikitext, template_name):
    """
    Finds a template within wikitext and parses the arguments.

    Parameters
    ----------
    wikitext: string
        wiktext
    template_name: string
        Name of the template to find

    Returns
    -------
    dict[str, object]
        returns a dictionary containing 3 keys:

        texts: list[str]
            text not included in the template itself; each template call
            inbetween
        args: list[str]
            positional arguments passed to the template
        kwargs: OrderedDict[str, str]
            keyword arguments passed to the template in the order they
            appeared in the wikitext

    """
    def f(scanner, result, tid):
        return tid, scanner.match, result

    scanner = re.Scanner([
        # Need to have this look ahead to avoid matching templates that start
        # with the same name.
        (r'{{%s(?=[^\w}\|]*\||}})' % template_name,
            partial(f, tid='template')),
        (r'{{', partial(f, tid='l_brace')),
        (r'}}', partial(f, tid='r_brace')),
        (r'\[\[', partial(f, tid='l_brackets')),
        (r'\]\]', partial(f, tid='r_brackets')),
        (r'\|', partial(f, tid='pipe')),
        (r'=', partial(f, tid='equals')),
        (r'[{}]{1}', partial(f, tid='single_brace')),
        (r'[\[\]]{1}', partial(f, tid='single_bracket')),
        (r'[^{}\|=\[\]]+', partial(f, tid='text')),
    ], re.UNICODE | re.MULTILINE)

    # Returns
    texts = [[], ]
    kw_arguments = OrderedDict()
    arguments = []

    # Loop parameters
    in_template = False
    pre_equal = True
    brace_count = 0
    bracket_count = 0
    template_argument = ['', '']

    for tid, match, text in scanner.scan(wikitext)[0]:
        if tid == 'template':
            in_template = True
        elif in_template:
            # r_brace is needed to capture the last argument, as it's not
            # delimited by a pipe
            # It also prevents reaching the second condition in that case
            if tid in ('pipe', 'r_brace') and brace_count == 0 and \
                            bracket_count == 0:
                pre_equal = True
                for i in range(0, 2):
                    template_argument[i] = template_argument[i].strip(' \n')

                if template_argument[1]:
                    kw_arguments[template_argument[0]] = \
                        template_argument[1]
                elif template_argument[0]:
                    arguments.append([template_argument[0]])
                template_argument = ['', '']
            elif tid in ('text', 'l_brace', 'r_brace', 'single_brace', 'pipe',
                         'l_brackets', 'r_brackets', 'single_bracket') or (
                    tid == 'equals' and brace_count >= 1):
                index = 0 if pre_equal else 1
                template_argument[index] += text
            elif tid == 'equals' and brace_count == 0:
                pre_equal = False

            # Brace counting must be done after the text parsing because
            # the previous brace count is needed up there
            if tid == 'l_brace':
                brace_count += 1
            elif tid == 'r_brace':
                if brace_count == 0:
                    in_template = False
                    texts.append([])
                else:
                    brace_count -= 1
            elif tid == 'l_brackets':
                bracket_count += 1
            elif tid == 'r_brackets':
                bracket_count -= 1
        else:
            texts[-1].append(text)

    # Don't really need the list anymore
    texts = [''.join(t) for t in texts]

    return {'texts': texts, 'args': arguments, 'kwargs': kw_arguments}


def parse_and_handle_description_tags(rr, text):
    """
    Parses and handles description texts

    Parameters
    ----------
    rr : RelationalReader
        RelationalReader instance to pass to TagHandler when parsing
    text : str
        Text which to parse

    Returns
    -------
    str
        Parsed texts with wiki templates/links
    """
    return parse_description_tags(text).handle_tags(
        TagHandler(rr).tag_handlers).replace('\n', '<br>').replace('\r', '')
