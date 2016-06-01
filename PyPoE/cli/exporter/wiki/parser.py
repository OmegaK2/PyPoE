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
    install_data_dependant_quantifiers,
)
from PyPoE.poe.file.ot import OTFileCache
from PyPoE.poe.sim.mods import get_translation

# =============================================================================
# Globals
# =============================================================================

__all__ = ['BaseParser']

_inter_wiki_map = (
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
    ('Life', {'link': 'Life'}),
    ('Mana Reservation', {'link': 'Mana Reservation'}),
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
    ('Anger', {'link': 'Anger'}),
    ('Animate(?:|d) Guardian', {'link': 'Animate Guardian'}),
    ('Animate(?:|d) Weapon', {'link': 'Animate Weapon'}),
    ('Arc ', {'link': 'Arc'}),
    ('Arctic Armour', {'link': 'Arctic Armour'}),
    ('Arctic Breath', {'link': 'Arctic Breath'}),
    ('Assassin\'s Mark', {}),
    ('Ball Lightning', {'link': 'Ball Lightning'}),
    ('Barrage', {'link': 'Barrage'}),
    ('Bear Trap', {'link': 'Bear Trap'}),
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
    ('Clarity', {'link': 'Clarity'}),
    ('Cleave', {'link': 'Cleave'}),
    ('Cold Snap', {'link': 'Cold Snap'}),
    ('Conductivity', {'link': 'Conductivity'}),
    ('Contagion', {'link': 'Contagion'}),
    ('Conversion Trap', {'link': 'Conversion Trap'}),
    ('Convocation', {'link': 'Convocation'}),
    ('Cyclone', {'link': 'Cyclone'}),
    ('Damage Infusion', {'link': 'Damage Infusion'}),
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
    ('Split Arrow', {'link': 'Split Arrow'}),
    ('Static Strike', {'link': 'Static Strike'}),
    ('Static Tether', {'link': 'Static Tether'}),
    ('Storm Call', {'link': 'Storm Call'}),
    ('Summon Chaos Golem', {'link': 'Summon Chaos Golem'}),
    ('Summon Flame Golem', {'link': 'Summon Flame Golem'}),
    ('Summon Ice Golem', {'link': 'Summon Ice Golem'}),
    ('Summon Lightning Golem', {'link': 'Summon Lightning Golem'}),
    ('Summon Raging Spirit', {'link': 'Summon Raging Spirit'}),
    ('Summon Skeletons', {'link': 'Summon Skeletons'}),
    ('Summon Stone Golem', {'link': 'Summon Stone Golem'}),
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
    ('Vulnerability', {'link': 'Vulnerability'}),
    ('Warlord\'s Mark', {'link': 'Warlord\'s Mark'}),
    ('Whirling Blades', {'link': 'Whirling Blades'}),
    ('Wild Strike', {'link': 'Wild Strike'}),
    ('Wither', {'link': 'Wither'}),
    ('Wrath', {'link': 'Wrath'}),
    #
    # Enchantment skills
    #
    ('Commandment of Blades', {'link': 'of Blades'}),
    ('Commandment of Flames', {'link': 'of Flames'}),
    ('Commandment of Force', {'link': 'of Force'}),
    ('Commandment of Frost', {'link': 'of Frost'}),
    ('Commandment of Fury', {'link': 'of Fury'}),
    ('Commandment of Inferno', {'link': 'of Inferno'}),
    ('Commandment of Ire', {'link': 'of Ire'}),
    ('Commandment of Light', {'link': 'of Light'}),
    ('Commandment of Reflection', {'link': 'of Reflection'}),
    ('Commandment of Spite', {'link': 'of Spite'}),
    ('Commandment of Thunder', {'link': 'of Thunder'}),
    ('Commandment of War', {'link': 'of War'}),
    ('Commandment of Winter', {'link': 'of Winter'}),
    ('Commandment of the Grave', {'link': 'of the Grave'}),
    ('Commandment of the Tempest', {'link': 'of the Tempest'}),
    ('Decree of Blades', {'link': 'of Blades'}),
    ('Decree of Flames', {'link': 'of Flames'}),
    ('Decree of Force', {'link': 'of Force'}),
    ('Decree of Frost', {'link': 'of Frost'}),
    ('Decree of Fury', {'link': 'of Fury'}),
    ('Decree of Inferno', {'link': 'of Inferno'}),
    ('Decree of Ire', {'link': 'of Ire'}),
    ('Decree of Light', {'link': 'of Light'}),
    ('Decree of Reflection', {'link': 'of Reflection'}),
    ('Decree of Spite', {'link': 'of Spite'}),
    ('Decree of Thunder', {'link': 'of Thunder'}),
    ('Decree of War', {'link': 'of War'}),
    ('Decree of Winter', {'link': 'of Winter'}),
    ('Decree of the Grave', {'link': 'of the Grave'}),
    ('Decree of the Tempest', {'link': 'of the Tempest'}),
    ('Edict of Blades', {'link': 'of Blades'}),
    ('Edict of Flames', {'link': 'of Flames'}),
    ('Edict of Force', {'link': 'of Force'}),
    ('Edict of Frost', {'link': 'of Frost'}),
    ('Edict of Fury', {'link': 'of Fury'}),
    ('Edict of Inferno', {'link': 'of Inferno'}),
    ('Edict of Ire', {'link': 'of Ire'}),
    ('Edict of Light', {'link': 'of Light'}),
    ('Edict of Reflection', {'link': 'of Reflection'}),
    ('Edict of Spite', {'link': 'of Spite'}),
    ('Edict of Thunder', {'link': 'of Thunder'}),
    ('Edict of War', {'link': 'of War'}),
    ('Edict of Winter', {'link': 'of Winter'}),
    ('Edict of the Grave', {'link': 'of the Grave'}),
    ('Edict of the Tempest', {'link': 'of the Tempest'}),
    ('Word of Blades', {'link': 'of Blades'}),
    ('Word of Flames', {'link': 'of Flames'}),
    ('Word of Force', {'link': 'of Force'}),
    ('Word of Frost', {'link': 'of Frost'}),
    ('Word of Fury', {'link': 'of Fury'}),
    ('Word of Inferno', {'link': 'of Inferno'}),
    ('Word of Ire', {'link': 'of Ire'}),
    ('Word of Light', {'link': 'of Light'}),
    ('Word of Reflection', {'link': 'of Reflection'}),
    ('Word of Spite', {'link': 'of Spite'}),
    ('Word of Thunder', {'link': 'of Thunder'}),
    ('Word of War', {'link': 'of War'}),
    ('Word of Winter', {'link': 'of Winter'}),
    ('Word of the Grave', {'link': 'of the Grave'}),
    ('Word of the Tempest', {'link': 'of the Tempest'}),
    #
    # Support gems
    #
    ('(?:level [0-9]+) Added Chaos Damage', {'link': 'Added Chaos Damage'}),
    ('(?:level [0-9]+) Added Cold Damage', {'link': 'Added Cold Damage'}),
    ('(?:level [0-9]+) Added Fire Damage', {'link': 'Added Fire Damage'}),
    ('(?:level [0-9]+) Added Lightning Damage', {
        'link': 'Added Lightning Damage'}),
    ('(?:level [0-9]+) Additional Accuracy', {'link': 'Additional Accuracy'}),
    ('(?:level [0-9]+) Blasphemy', {'link': 'Blasphemy'}),
    ('(?:level [0-9]+) Blind', {'link': 'Blind (support gem)'}),
    ('(?:level [0-9]+) Block Chance Reduction', {
        'link': 'Block Chance Reduction'}),
    ('(?:level [0-9]+) Blood Magic', {'link': 'Blood Magic'}),
    ('(?:level [0-9]+) Bloodlust', {'link': 'Bloodlust'}),
    ('(?:level [0-9]+) Cast On Critical Strike', {
        'link': 'Cast On Critical Strike'}),
    ('(?:level [0-9]+) Cast on Death', {'link': 'Cast on Death'}),
    ('(?:level [0-9]+) Cast on Melee Kill', {'link': 'Cast on Melee Kill'}),
    ('(?:level [0-9]+) Cast when Damage Taken', {
        'link': 'Cast when Damage Taken'}),
    ('(?:level [0-9]+) Cast when Stunned', {'link': 'Cast when Stunned'}),
    ('(?:level [0-9]+) Chain', {'link': 'Chain'}),
    ('(?:level [0-9]+) Chance to Flee', {'link': 'Chance to Flee'}),
    ('(?:level [0-9]+) Chance to Ignite', {'link': 'Chance to Ignite'}),
    ('(?:level [0-9]+) Cluster Traps', {'link': 'Cluster Traps'}),
    ('(?:level [0-9]+) Cold Penetration', {'link': 'Cold Penetration'}),
    ('(?:level [0-9]+) Cold to Fire', {'link': 'Cold to Fire'}),
    ('(?:level [0-9]+) Concentrated Effect', {'link': 'Concentrated Effect'}),
    ('(?:level [0-9]+) Controlled Destruction', {
        'link': 'Controlled Destruction'}),
    ('(?:level [0-9]+) Culling Strike', {'link': 'Culling Strike'}),
    ('(?:level [0-9]+) Curse On Hit', {'link': 'Curse On Hit'}),
    ('(?:level [0-9]+) Elemental Focus', {'link': 'Elemental Focus'}),
    ('(?:level [0-9]+) Elemental Proliferation', {
        'link': 'Elemental Proliferation'}),
    ('(?:level [0-9]+) Empower', {'link': 'Empower'}),
    ('(?:level [0-9]+) Endurance Charge on Melee Stun', {
        'link': 'Endurance Charge on Melee Stun'}),
    ('(?:level [0-9]+) Enhance', {'link': 'Enhance'}),
    ('(?:level [0-9]+) Enlighten', {'link': 'Enlighten'}),
    ('(?:level [0-9]+) Faster Attacks', {'link': 'Faster Attacks'}),
    ('(?:level [0-9]+) Faster Casting', {'link': 'Faster Casting'}),
    ('(?:level [0-9]+) Faster Projectiles', {'link': 'Faster Projectiles'}),
    ('(?:level [0-9]+) Fire Penetration', {'link': 'Fire Penetration'}),
    ('(?:level [0-9]+) Fork', {'link': 'Fork'}),
    ('(?:level [0-9]+) Fortify', {'link': 'Fortify'}),
    ('(?:level [0-9]+) Generosity', {'link': 'Generosity'}),
    ('(?:level [0-9]+) Greater Multiple Projectiles', {
        'link': 'Greater Multiple Projectiles'}),
    ('(?:level [0-9]+) Hypothermia', {'link': 'Hypothermia'}),
    ('(?:level [0-9]+) Ice Bite', {'link': 'Ice Bite'}),
    ('(?:level [0-9]+) Increased Area of Effect', {
        'link': 'Increased Area of Effect'}),
    ('(?:level [0-9]+) Increased Burning Damage', {
        'link': 'Increased Burning Damage'}),
    ('(?:level [0-9]+) Increased Critical Damage', {
        'link': 'Increased Critical Damage'}),
    ('(?:level [0-9]+) Increased Critical Strikes', {
        'link': 'Increased Critical Strikes'}),
    ('(?:level [0-9]+) Increased Duration', {'link': 'Increased Duration'}),
    ('(?:level [0-9]+) Innervate', {'link': 'Innervate'}),
    ('(?:level [0-9]+) Iron Grip', {'link': 'Iron Grip'}),
    ('(?:level [0-9]+) Iron Will', {'link': 'Iron Will'}),
    ('(?:level [0-9]+) Item Quantity', {'link': 'Item Quantity'}),
    ('(?:level [0-9]+) Item Rarity', {'link': 'Item Rarity'}),
    ('(?:level [0-9]+) Knockback', {'link': 'Knockback'}),
    ('(?:level [0-9]+) Less Duration', {'link': 'Less Duration'}),
    ('(?:level [0-9]+) Lesser Multiple Projectiles', {
        'link': 'Lesser Multiple Projectiles'}),
    ('(?:level [0-9]+) Life Gain on Hit', {'link': 'Life Gain on Hit'}),
    ('(?:level [0-9]+) Life Leech', {'link': 'Life Leech'}),
    ('(?:level [0-9]+) Lightning Penetration', {'link': 'Lightning Penetration'}),
    ('(?:level [0-9]+) Mana Leech', {'link': 'Mana Leech'}),
    ('(?:level [0-9]+) Melee Damage on Full Life', {
        'link': 'Melee Damage on Full Life'}),
    ('(?:level [0-9]+) Melee Physical Damage', {'link': 'Melee Physical Damage'}),
    ('(?:level [0-9]+) Melee Splash', {'link': 'Melee Splash'}),
    ('(?:level [0-9]+) Minefield', {'link': 'Minefield'}),
    ('(?:level [0-9]+) Minion Damage', {'link': 'Minion Damage'}),
    ('(?:level [0-9]+) Minion Life', {'link': 'Minion Life'}),
    ('(?:level [0-9]+) Minion Speed', {'link': 'Minion Speed'}),
    ('(?:level [0-9]+) Minion and Totem Elemental Resistance', {
        'link': 'Minion and Totem Elemental Resistance'}),
    ('(?:level [0-9]+) Multiple Traps', {'link': 'Multiple Traps'}),
    ('(?:level [0-9]+) Multistrike', {'link': 'Multistrike'}),
    ('(?:level [0-9]+) Physical Projectile Attack Damage', {
        'link': 'Physical Projectile Attack Damage'}),
    ('(?:level [0-9]+) Physical to Lightning', {'link': 'Physical to Lightning'}),
    ('(?:level [0-9]+) Pierce', {'link': 'Pierce (support gem)'}),
    ('(?:level [0-9]+) Point Blank', {'link': 'Point Blank'}),
    ('(?:level [0-9]+) Poison', {'link': 'Poison (support gem)'}),
    ('(?:level [0-9]+) Power Charge On Critical', {
        'link': 'Power Charge On Critical'}),
    ('(?:level [0-9]+) Ranged Attack Totem', {'link': 'Ranged Attack Totem'}),
    ('(?:level [0-9]+) Rapid Decay', {'link': 'Rapid Decay'}),
    ('(?:level [0-9]+) Reduced Mana', {'link': 'Reduced Mana'}),
    ('(?:level [0-9]+) Remote Mine', {'link': 'Remote Mine'}),
    ('(?:level [0-9]+) Return Projectiles', {'link': 'Return Projectiles'}),
    ('(?:level [0-9]+) Slower Projectiles', {'link': 'Slower Projectiles'}),
    ('(?:level [0-9]+) Spell Echo', {'link': 'Spell Echo'}),
    ('(?:level [0-9]+) Spell Totem', {'link': 'Spell Totem'}),
    ('(?:level [0-9]+) Split Projectiles', {'link': 'Split Projectiles'}),
    ('(?:level [0-9]+) Stun', {'link': 'Stun (support gem)'}),
    ('(?:level [0-9]+) Trap', {'link': 'Trap (support gem)'}),
    ('(?:level [0-9]+) Trap Cooldown', {'link': 'Trap Cooldown'}),
    ('(?:level [0-9]+) Trap and Mine Damage', {'link': 'Trap and Mine Damage'}),
    ('(?:level [0-9]+) Void Manipulation', {'link': 'Void Manipulation'}),
    ('(?:level [0-9]+) Weapon Elemental Damage', {
        'link': 'Weapon Elemental Damage'}),
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
)

'''_inter_wiki_re = re.compile(
    r'(?: |^)(?P<text>%s))' % '|'.join([item[0] for item in _inter_wiki_map]),
    re.UNICODE | re.IGNORECASE
)'''
_inter_wiki_re = []
_MAX_RE = 97
for i in range(0, (len(_inter_wiki_map)//_MAX_RE)+1):
    id = i*_MAX_RE
    _inter_wiki_re.append(re.compile(
        r'(?![^\[]*\]\])'
        r'(?: |^)'
        r'(?P<text>%s)'
        r'(?= |$)' %
        '|'.join(['(%s)' % item[0] for item in _inter_wiki_map[id:id+_MAX_RE]]),
        re.UNICODE | re.IGNORECASE ,
    ))

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
        self.rr = RelationalReader(
            path_or_ggpk=base_path,
            files=self._files,
            read_options=opt
        )
        install_data_dependant_quantifiers(self.rr)
        self.tc = TranslationFileCache(path_or_ggpk=base_path)
        for file_name in self._translations:
            self.tc[file_name]

        self.ot = OTFileCache(path_or_ggpk=base_path)

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
                    temp_trans.append(self._format_hidden(r1[0]))
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

    for i, regex in enumerate(_inter_wiki_re):
        out = []
        last_index = 0
        for match in regex.finditer(string):
            text = match.group('text')
            # Offset by 1 to account for text group
            index = match.groups().index(text, 1)-1
            data = _inter_wiki_map[i*_MAX_RE+index][1]

            out.append(string[last_index:match.start('text')])
            if text == data['link']:
                out.append('[[%s]]' % data['link'])
            else:
                out.append('[[%s|%s]]' % (data['link'], text))

            last_index = match.end('text')

        out.append(string[last_index:])
        string = ''.join(out)

    return string
