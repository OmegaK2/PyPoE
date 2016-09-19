"""
Wiki gems exporter

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/wiki/parsers/gems.py                          |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

http://pathofexile.gamepedia.com

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
import sys
import warnings
import os
from collections import defaultdict, OrderedDict

# Self
from PyPoE.poe.file.ggpk import GGPKFile, extract_dds
from PyPoE.poe.file.stat_filters import StatFilterFile, SkillEntry
from PyPoE.poe.sim.formula import gem_stat_requirement, GemTypes
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter.util import get_content_ggpk_path
from PyPoE.cli.exporter.wiki.handler import ExporterHandler, ExporterResult, \
    add_format_argument
from PyPoE.cli.exporter.wiki.parser import (
    BaseParser, format_result_rows, make_inter_wiki_links
)

# =============================================================================
# Functions
# =============================================================================


def _apply_column_map(infobox, column_map, list_object):
    for k, data in column_map:
        value = list_object[k]
        if data.get('condition') and not data['condition'](value):
            continue

        if data.get('format'):
            value = data['format'](value)
        infobox[data['template']] = value


def _type_factory(data_file, data_mapping, row_index=True, function=None,
                  fail_condition=False):
    def func(self, infobox, base_item_type):
        try:
            data = self.rr[data_file].index['BaseItemTypesKey'][
                base_item_type.rowid if row_index else base_item_type['Id']
            ]
        except KeyError:
            warnings.warn(
                'Missing %s info for "%s"' % (data_file, base_item_type['Name'])
            )
            return fail_condition

        _apply_column_map(infobox, data_mapping, data)

        if function:
            function(self, infobox, base_item_type, data)

        return True
    return func

# =============================================================================
# Classes
# =============================================================================


class WikiCondition(object):
    # This only works as long there aren't nested templates inside the infobox
    regex_search = re.compile(
        '(<onlyinclude>|<onlyinclude></onlyinclude>|)\{\{(Item|#invoke:item\|item)\n'
        '(?P<data>[^\}]*)'
        '\n\}\}(</onlyinclude>|)',
        re.UNICODE | re.IGNORECASE | re.MULTILINE | re.DOTALL
    )

    regex_infobox_split = re.compile(
        '\|(?P<key>[\S]+)[\s]*=[\s]*(?P<value>[^|]*)',
        re.UNICODE | re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    COPY_KEYS = (
        # for skills
        'radius',
        'radius_description',
        'radius_secondary',
        'radius_secondary_description',
        'radius_tertiary',
        'radius_tertiary_description',
        'has_percentage_mana_cost',
        'has_reservation_mana_cost',
        # all items
        'drop_enabled',
        'name_list',
        'inventory_icon',
        'alternate_art_inventory_icons',
        'release_version',
        'removal_version',
    )

    def __init__(self, data, cmdargs):
        self.data = data
        self.cmdargs = cmdargs
        self.itembox = None

    def __call__(self, *args, **kwargs):
        page = kwargs.get('page')

        if page is not None:
            # Abuse this so it can be called as "text" and "condition"
            if self.itembox is None:
                self.itembox = self.regex_search.search(page.text())
                if self.itembox is None:
                    return False

                return True

            for match in self.regex_infobox_split.finditer(
                    self.itembox.group('data')):
                k = match.group('key')
                if k in self.COPY_KEYS:
                    self.data[k] = match.group('value').strip('\n\r ')

            text = self._get_text()
            if self.data['class'] not in ('Support Skill Gems',
                                          'Active Skill Gems'):
                text = '<onlyinclude></onlyinclude>' + self._get_text()

            # I need the +1 offset or it adds a space everytime for some reason.
            return page.text()[:self.itembox.start()] + text + \
                page.text()[self.itembox.end()+1:]
        else:
            return self._get_text()

    def _get_text(self):
        return format_result_rows(
            parsed_args=self.cmdargs,
            template_name='Item',
            indent=33,
            ordered_dict=self.data,
        )


class ItemsHandler(ExporterHandler):
    def __init__(self, sub_parser, *args, **kwargs):
        super(ItemsHandler, self).__init__(self, sub_parser, *args, **kwargs)
        self.parser = sub_parser.add_parser('items', help='Items Exporter')
        self.parser.set_defaults(func=lambda args: self.parser.print_help())
        sub = self.parser.add_subparsers()

        #
        # Generic base item export
        #
        parser = sub.add_parser(
            'export',
            help='Extracts the item information'
        )
        self.add_default_parsers(
            parser=parser,
            cls=ItemsParser,
            func=ItemsParser.export,
        )

        add_format_argument(parser)

        parser.add_argument(
            '-ft-c', '--filter-class',
            help='Filter by item class(es). Case sensitive.',
            nargs='*',
            dest='item_class',
        )

        parser.add_argument(
            '-mid', '--is-metadata-id',
            help='Whether the given item names are metadata ids instead',
            action='store_true',
            dest='is_metadata_id',
        )

        parser.add_argument(
            '-im', '--store-images',
            help='If specified item 2d art images will be extracted. '
                 'Requires brotli to be installed.',
            action='store_true',
            dest='store_images',
        )

        parser.add_argument(
            '-im-c', '--convert-images',
            help='Convert extracted images to png using ImageMagick '
                 '(requires "magick" command to be executeable)',
            action='store_true',
            dest='convert_images',
        )

        parser.add_argument(
            'item',
            help='Name of the item; can be specified multiple times',
            nargs='+',
        )
        #
        # Prophecies
        #
        parser = sub.add_parser(
            'prophecy',
            help='Extracts the prophecy information'
        )
        self.add_default_parsers(
            parser=parser,
            cls=ItemsParser,
            func=ItemsParser.prophecy,
        )

        parser.add_argument(
            '--allow-disabled',
            help='Allows disabled prophecies to be exported',
            action='store_true',
            dest='allow_disabled',
            default=False,
        )

        parser.add_argument(
            'name',
            help='Name of the prophecy; can be specified multiple times',
            nargs='+',
        )

        add_format_argument(parser)


class ItemsParser(BaseParser):
    _regex_format = re.compile(
        '(?P<index>x|y|z)'
        '(?:[\W]*)'
        '(?P<tag>%|second)',
        re.IGNORECASE
    )

    # Core files we need to load
    _files = [
        'BaseItemTypes.dat',
    ]

    # Core translations we need
    _translations = [
        'stat_descriptions.txt',
        'gem_stat_descriptions.txt',
        'skill_stat_descriptions.txt',
        'active_skill_gem_stat_descriptions.txt',
    ]

    _IGNORE_DROP_LEVEL_CLASSES = (
        'Hideout Doodads',
        'Microtransactions',
        'Labyrinth Item',
        'Labyrinth Trinket',
        'Labyrinth Map Item',
    )

    _IGNORE_DROP_LEVEL_ITEMS = {
        'Alchemy Shard',
        'Alteration Shard',
        'Enchant',
        'Imprint',
        'Transmutation Shard',
        'Scroll Fragment',
    }

    _DROP_DISABLED_ITEMS = {
        'Perandus Coin',
        'Eternal Orb'
    }

    # Values without the Metadata/Projectiles/ prefix
    _skill_gem_to_projectile_map = {
        'Fireball': 'Fireball',
        'Spark': 'Spark',
        'Ice Spear': 'IceSpear',
        'Freezing Pulse': 'FreezingPulse',
        'Ethereal Knives': 'ShadowProjectile',
        'Arctic Breath': 'ArcticBreath',
        'Flame Totem': 'TotemFireSpray',
        'Caustic Arrow': 'CausticArrow',
        'Burning Arrow': 'BurningArrow',
        'Vaal Burning Arrow': 'VaalBurningArrow',
        'Explosive Arrow': 'FuseArrow',
        'Lightning Arrow': 'LightningArrow',
        'Ice Shot': 'IceArrow',
        'Incinerate': 'Flamethrower1',
        'Lightning Trap': 'LightningTrap',
        'Spectral Throw': 'ThrownWeapon',
        'Ball Lightning': 'BallLightningPlayer',
        'Tornado Shot': 'TornadoShotArrow',
        # TornadoShotSecondaryArrow,
        'Frost Blades': 'IceStrikeProjectile',
        'Molten Strike': 'FireMortar',
        'Wild Strike': 'ElementalStrikeColdProjectile',
        'Shrapnel Shot': 'ShrapnelShot',
        'Power Siphon': 'Siphon',
        'Siege Ballista': 'CrossbowSnipeProjectile',
        #'Ethereal Knives': 'ShadowBlades',
        'Frostbolt': 'FrostBolt',
        'Split Arrow': 'SplitArrowDefault',
    }

    _cp_columns = (
        'Level', 'LevelRequirement', 'ManaMultiplier', 'CriticalStrikeChance',
        'ManaCost', 'DamageMultiplier', 'VaalSouls', 'VaalStoredUses',
        'Cooldown', 'StoredUses', 'DamageEffectiveness'
    )

    _attribute_map = OrderedDict((
        ('Str', 'Strength'),
        ('Dex', 'Dexterity'),
        ('Int', 'Intelligence'),
    ))

    _skill_gem_stat_remove = {
        'Molten Shell': [{'id': 'base_resist_all_elements_%', 'value': 0}],
        'Vaal Molten Shell': [{'id': 'base_resist_all_elements_%', 'value': 0}],
    }

    def __init__(self, *args, **kwargs):
        super(ItemsParser, self).__init__(*args, **kwargs)

        self._skill_stat_filters = None

    @property
    def skill_stat_filter(self):
        """

        Returns
        -------
        StatFilterFile
        """
        if self._skill_stat_filters is None:
            self._skill_stat_filters = StatFilterFile()
            self._skill_stat_filters.read(os.path.join(
                self.base_path, 'Metadata', 'StatDescriptions',
                'skillpopup_stat_filters.txt'
            ))
            #TODO remove once fixed
            #self._skill_stat_filters.skills['spirit_offering'] = SkillEntry(skill_id='spirit_offering', translation_file_path='Metadata/StatDescriptions/offering_skill_stat_descriptions.txt', stats=[])

        return self._skill_stat_filters

    def _format_lines(self, lines):
        return '<br>'.join(lines).replace('\n', '<br>')

    _skill_column_map = (
        ('ManaCost', {
            'template': 'mana_cost',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v),
        }),
        ('ManaMultiplier', {
            'template': 'mana_multiplier',
            'format': lambda v: '{0:n}'.format(v),
            'default_cls': ('Active Skill Gems', ),
        }),
        ('StoredUses', {
            'template': 'stored_uses',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v),
        }),
        ('Cooldown', {
            'template': 'cooldown',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v/1000),
        }),
        ('VaalSouls', {
            'template': 'vaal_souls_requirement',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v),
        }),
        ('VaalStoredUses', {
            'template': 'vaal_stored_uses',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v),
        }),
        ('CriticalStrikeChance', {
            'template': 'critical_strike_chance',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v/100),
        }),
        ('DamageEffectiveness', {
            'template': 'damage_effectiveness',
            'format': lambda v: '{0:n}'.format(v+100),
        }),
        ('DamageMultiplier', {
            'template': 'damage_multiplier',
            'format': lambda v: '{0:n}'.format(v/100+100),
        }),
    )

    def _skill_gem(self, infobox, base_item_type):
        try:
            skill_gem = self.rr['SkillGems.dat'].index['BaseItemTypesKey'][
                base_item_type.rowid]
        except KeyError:
            return False

        # TODO: Maybe catch empty stuff here?
        exp = 0
        exp_level = []
        exp_total = []
        for row in self.rr['ItemExperiencePerLevel.dat']:
            if row['BaseItemTypesKey'] == base_item_type:
                exp_new = row['Experience']
                exp_level.append(exp_new - exp)
                exp_total.append(exp_new)
                exp = exp_new

        if not exp_level:
            console('No experience progression found for "%s". Skipping.' %
                    base_item_type['Name'], msg=Msg.error)
            return False

        ge = skill_gem['GrantedEffectsKey']

        gepl = []
        for row in self.rr['GrantedEffectsPerLevel.dat']:
            if row['GrantedEffectsKey'] == ge:
                gepl.append(row)

        if not gepl:
            console('No level progression found for "%s". Skipping.' %
                    base_item_type['Name'], msg=Msg.error)
            return False

        gepl.sort(key=lambda x:x['Level'])

        ae = ge['ActiveSkillsKey']

        max_level = len(exp_total)-1
        if ae:
            try:
                tf = self.tc[self.skill_stat_filter.skills[
                    ae['Id']].translation_file_path]
            except KeyError as e:
                warnings.warn('Missing active skill in stat filers: %s' % e.args[0])
                tf = self.tc['skill_stat_descriptions.txt']
        else:
            tf = self.tc['gem_stat_descriptions.txt']

        stat_ids = []
        stat_indexes = []
        for index, stat in enumerate(gepl[0]['StatsKeys']):
            stat_ids.append(stat['Id'])
            stat_indexes.append(index+1)

        # reformat the datas we need
        level_data = []
        stat_key_order = {
            'stats': OrderedDict(),
            'qstats': OrderedDict(),
        }

        for i, row in enumerate(gepl):
            data = defaultdict()

            stats = [r['Id'] for r in row['StatsKeys']] + \
                    [r['Id'] for r in row['StatsKeys2']]
            values = row['StatValues'] + ([1, ] * len(row['StatsKeys2']))

            rminfos = self._skill_gem_stat_remove.get(base_item_type['Name'])
            if rminfos:
                for rminfo in rminfos:
                    index = stats.index(rminfo['id'])
                    if values[index] == rminfo['value']:
                        del stats[index]
                        del values[index]

            tr = tf.get_translation(
                tags=stats,
                values=values,
                full_result=True,
            )
            data['_tr'] = tr

            qtr = tf.get_translation(
                tags=[r['Id'] for r in row['Quality_StatsKeys']],
                # Offset Q1000
                values=[v/50 for v in row['Quality_Values']],
                full_result=True,
                use_placeholder=lambda i: "{%s}" % i,
            )
            data['_qtr'] = qtr

            data['stats'] = {}
            data['qstats'] = {}

            for result, key in (
                    (tr, 'stats'),
                    (qtr, 'qstats'),
            ):
                for j, stats in enumerate(result.found_ids):
                    k = '__'.join(stats)
                    stat_key_order[key][k] = None
                    data[key]['__'.join(stats)] = {
                        'line': result.found_lines[j],
                        'stats': stats,
                        'values': result.values[j],
                        'values_parsed': result.values_parsed[j],
                    }
                for stat, value in result.missing:
                    warnings.warn('Missing translation for %s' % stat)
                    stat_key_order[key][stat] = None
                    data[key][stat] = {
                        'line': '',
                        'stats': [stat, ],
                        'values': [value, ],
                    }

            for stat_dict in data['qstats'].values():
                for k in ('values', 'values_parsed'):
                    new = []
                    for v in stat_dict[k]:
                        v /= 20
                        if v.is_integer():
                            v = int(v)
                        new.append(v)
                    stat_dict[k] = new
                stat_dict['line'] = stat_dict['line'].format(
                    *stat_dict['values_parsed']
                )


            try:
                data['exp'] = exp_level[i]
                data['exp_total'] = exp_total[i]
            except IndexError:
                pass

            for column in self._cp_columns:
                data[column] = row[column]

            level_data.append(data)

        # Find static & dynamic stats..

        static = {
            'columns': set(self._cp_columns),
            'stats': OrderedDict(stat_key_order['stats']),
            'qstats': OrderedDict(stat_key_order['qstats']),
        }
        dynamic = {
            'columns': set(),
            'stats': OrderedDict(),
            'qstats': OrderedDict(),
        }
        last = level_data[0]
        for data in level_data[1:]:
            for key in list(static['columns']):
                if last[key] != data[key]:
                    static['columns'].remove(key)
                    dynamic['columns'].add(key)
            for stat_key in ('stats', 'qstats'):
                for key in list(static[stat_key]):
                    if key not in last[stat_key]:
                        continue
                    if key not in data[stat_key]:
                        continue

                    if last[stat_key][key]['values'] != data[stat_key][key][
                            'values']:
                        del static[stat_key][key]
                        dynamic[stat_key][key] = None
            last = data

        #
        # Output handling for gem infobox
        #

        # SkillGems.dat
        for attr_short, attr_long in self._attribute_map.items():
            if not skill_gem[attr_short]:
                continue
            infobox[attr_long.lower() + '_percent'] = skill_gem[attr_short]

        infobox['gem_tags'] = ', '.join(
            [gt['Tag'] for gt in skill_gem['GemTagsKeys'] if gt['Tag']]
        )

        if not ge['IsSupport']:
            infobox['cast_time'] = ge['CastTime'] / 1000

        # From ActiveSkills.dat
        if ae:
            infobox['gem_description'] = ae['Description']
            infobox['active_skill_name'] = ae['DisplayedName']
            if ae['WeaponRestriction_ItemClassesKeys']:
                # The class name may be empty for reason, causing issues
                infobox['item_class_restriction'] = ', '.join([
                    c['Name'] if c['Name'] else c['Id'] for c in
                    ae['WeaponRestriction_ItemClassesKeys']
                ])

        # From Projectile.dat if available
        key = self._skill_gem_to_projectile_map.get(base_item_type['Name'])
        if key:
            infobox['projectile_speed'] = self.rr['Projectiles.dat'].index[
                'Id']['Metadata/Projectiles/' + key]['ProjectileSpeed']

        # From GrantedEffects.dat

        infobox['skill_id'] = ge['Id']
        infobox['is_support_gem'] = ge['IsSupport']
        if ge['SupportGemLetter']:
            infobox['support_gem_letter'] = ge['SupportGemLetter']

        # GrantedEffectsPerLevel.dat
        infobox['required_level'] = level_data[0]['LevelRequirement']

        # Don't add columns that are zero/default
        for column, column_data in self._skill_column_map:
            if column not in static['columns']:
                continue

            default = column_data.get('default')
            if default is not None and gepl[0][column] == \
                    column_data['default']:
                continue

            df = column_data.get('default_cls')
            if df is not None and infobox['class'] in df:
                continue
            infobox['static_' + column_data['template']] = \
                column_data['format'](gepl[0][column])

        # Normal stats
        # TODO: Loop properly - some stats not available at level 0
        stats = []
        values = []
        lines = []
        for key in stat_key_order['stats']:
            if key in static['stats']:
                sdict = level_data[0]['stats'][key]
                line = sdict['line']
                stats.extend(sdict['stats'])
                values.extend(sdict['values'])
            elif key in dynamic['stats']:
                stat_dict = level_data[0]['stats'][key]
                stat_dict_max = level_data[max_level]['stats'][key]
                tr_values = []
                for j, value in enumerate(stat_dict['values']):
                    tr_values.append((value, stat_dict_max['values'][j]))

                # Should only be one
                line = tf.get_translation(stat_dict_max['stats'], tr_values)
                line = line[0] if line else ''

            if line:
                lines.append(line)

        self._write_stats(infobox, zip(stats, values), 'static_')

        # Add the attack damage stat from the game data
        if ae and 'Attack' in infobox['gem_tags']:
            values = (
                level_data[0]['DamageMultiplier'],
                level_data[max_level]['DamageMultiplier'],
            )
            # Account for default (0 = 100%)
            if values[0] != 0 or values[1] != 0:
                lines.insert(0, tf.get_translation(
                    tags=['active_skill_attack_damage_final_permyriad', ],
                    values=[values, ]
                )[0])

        infobox['stat_text'] = self._format_lines(lines)

        # Quality stats
        lines = []
        stats = []
        values = []
        for key in static['qstats']:
            stat_dict = level_data[0]['qstats'][key]
            lines.append(stat_dict['line'])
            stats.extend(stat_dict['stats'])
            values.extend(stat_dict['values'])

        infobox['quality_stat_text'] = self._format_lines(lines)
        self._write_stats(infobox, zip(stats, values), 'static_quality_')

        #
        # Output handling for progression
        #

        # Body
        map2 = {
            'Str': 'strength_requirement',
            'Int': 'intelligence_requirement',
            'Dex': 'dexterity_requirement',
            'ManaCost': 'mana_cost',
            'CriticalStrikeChance': 'critical_strike_chance',
            'ManaMultiplier': 'mana_multiplier',
        }

        if base_item_type['ItemClassesKey']['Name'] == 'Active Skill Gems':
            gtype = GemTypes.active
        elif base_item_type['ItemClassesKey']['Name'] == 'Support Skill Gems':
            gtype = GemTypes.support

        for i, row in enumerate(level_data):
            prefix = 'level%s' % (i + 1)
            infobox[prefix] = 'True'

            prefix += '_'

            infobox[prefix + 'level_requirement'] = row['LevelRequirement']

            for attr in ('Str', 'Dex', 'Int'):
                # +1 for gem levels starting at 1
                # +1 for being able to corrupt gems to +1 level
                if row['Level'] <= (max_level+2) and skill_gem[attr]:
                    try:
                        infobox[prefix + map2[attr]] = gem_stat_requirement(
                            level=row['LevelRequirement'],
                            gtype=gtype,
                            multi=skill_gem[attr],
                        )
                    except ValueError as e:
                        warnings.warn(str(e))

            # Column handling
            for column, column_data in self._skill_column_map:
                if column not in dynamic['columns']:
                    continue
                # Removed the check of defaults on purpose, makes sense
                # to add the info since it is dynamically changed
                infobox[prefix + column_data['template']] = \
                    column_data['format'](row[column])

            # Stat handling
            for stat_key, stat_prefix in (
                    ('stats', ''),
                    ('qstats', 'quality_'),
            ):
                lines = []
                values = []
                stats = []
                for key in stat_key_order[stat_key]:
                    if key not in dynamic[stat_key]:
                        continue

                    stat_dict = row[stat_key][key]
                    # Don't add empty lines
                    if stat_dict['line']:
                        lines.append(stat_dict['line'])
                    stats.extend(stat_dict['stats'])
                    values.extend(stat_dict['values'])

                if lines:
                    infobox[prefix + stat_prefix + 'stat_text'] = \
                        self._format_lines(lines)
                self._write_stats(
                    infobox, zip(stats, values), prefix + stat_prefix
                )

            try:
                infobox[prefix + 'experience'] = exp_total[i]
            except IndexError:
                pass

        return True

    def _type_level(self, infobox, base_item_type):
        infobox['required_level'] = base_item_type['DropLevel']

        return True

    _type_attribute = _type_factory(
        data_file='ComponentAttributeRequirements.dat',
        data_mapping=(
            ('ReqStr', {
                'template': 'required_strength',
                'condition': lambda v: v > 0,
            }),
            ('ReqDex', {
                'template': 'required_dexterity',
                'condition': lambda v: v > 0,
            }),
            ('ReqInt', {
                'template': 'required_intelligence',
                'condition': lambda v: v > 0,
            }),
        ),
        row_index=False,
    )

    _type_armour = _type_factory(
        data_file='ComponentArmour.dat',
        data_mapping=(
            ('Armour', {
                'template': 'armour',
                'condition': lambda v: v > 0,
            }),
            ('Evasion', {
                'template': 'evasion',
                'condition': lambda v: v > 0,
            }),
            ('EnergyShield', {
                'template': 'energy_shield',
                'condition': lambda v: v > 0,
            }),
        ),
        row_index=False,
    )

    _type_shield = _type_factory(
        data_file='ShieldTypes.dat',
        data_mapping=(
            ('Block', {
                'template': 'block',
            }),
        ),
        row_index=True,
    )

    def _apply_flask_buffs(self, infobox, base_item_type, flasks):
        for i, value in enumerate(flasks['BuffStatValues'], start=1):
            infobox['buff_value%s' % i] = value

        if flasks['BuffDefinitionsKey']:
            stats = [s['Id'] for s in flasks['BuffDefinitionsKey']['StatsKeys']]
            tr = self.tc['stat_descriptions.txt'].get_translation(
                stats, flasks['BuffStatValues'], full_result=True
            )
            infobox['buff_stat_text'] = '<br>'.join([
                make_inter_wiki_links(line) for line in tr.lines
            ])


    #TODO: BuffDefinitionsKey, BuffStatValues
    _type_flask = _type_factory(
        data_file='Flasks.dat',
        data_mapping=(
            ('LifePerUse', {
                'template': 'flask_life',
                'condition': lambda v: v > 0,
            }),
            ('ManaPerUse', {
                'template': 'flask_mana',
                'condition': lambda v: v > 0,
            }),
            ('RecoveryTime', {
                'template': 'flask_duration',
                'condition': lambda v: v > 0,
                'format': lambda v: '{0:n}'.format(v / 10),
            }),
            ('BuffDefinitionsKey', {
                'template': 'buff_id',
                'condition': lambda v: v is not None,
                'format': lambda v: v['Id'],
            }),
        ),
        row_index=True,
        function=_apply_flask_buffs,
    )

    _type_flask_charges = _type_factory(
        data_file='ComponentCharges.dat',
        data_mapping=(
            ('MaxCharges', {
                'template': 'charges_max',
            }),
            ('PerCharge', {
                'template': 'charges_per_use',
            }),
        ),
        row_index=False,
    )

    _type_weapon = _type_factory(
        data_file='WeaponTypes.dat',
        data_mapping=(
            ('Critical', {
                'template': 'critical_strike_chance',
                'format': lambda v: '{0:n}'.format(v / 100),
            }),
            ('Speed', {
                'template': 'attack_speed',
                'format': lambda v: '{0:n}'.format(round(1000 / v, 2)),
            }),
            ('DamageMin', {
                'template': 'damage_min',
            }),
            ('DamageMax', {
                'template': 'damage_max',
            }),
            ('RangeMax', {
                'template': 'range',
            }),
        ),
        row_index=True,
    )

    def _currency_extra(self, infobox, base_item_type, currency):
        # Add the "shift click to unstack" stuff to currency-ish items
        if currency['Stacks'] > 1 and infobox['class'] not in \
                ('Microtransactions', ):
            if 'help_text' in infobox:
                infobox['help_text'] += '<br>'
            else:
                infobox['help_text'] = ''

            infobox['help_text'] += self.rr['ClientStrings.dat'].index[
                'Id']['ItemDisplayStackDescription']['Text']

        return True

    _type_currency = _type_factory(
        data_file='CurrencyItems.dat',
        data_mapping=(
            ('Stacks', {
                'template': 'stack_size',
                'condition': None,
            }),
            ('Description', {
                'template': 'description',
                'condition': lambda v: v,
            }),
            ('Directions', {
                'template': 'help_text',
                'condition': lambda v: v,
            }),
            ('CurrencyTab_StackSize', {
                'template': 'stack_size_currency_tab',
                'condition': lambda v: v > 0,
            }),
            ('CosmeticTypeName', {
                'template': 'cosmetic_type',
                'condition': lambda v: v,
            }),
        ),
        row_index=True,
        function=_currency_extra,
    )

    _master_hideout_doodad_map = (
        ('NPCMasterKey', {
            'template': 'master',
            'format': lambda v: v['NPCsKey']['Name'],
            #'condition': lambda v: v is not None,
        }),
        ('MasterLevel', {
            'template': 'master_level_requirement',
        }),
        ('FavourCost', {
            'template': 'master_favour_cost',
        }),
    )

    def _apply_master_map(self, infobox, base_item_type, hideout):
        if not hideout['IsNonMasterDoodad']:
            _apply_column_map(infobox, self._master_hideout_doodad_map,
                                   hideout)

    _type_hideout_doodad = _type_factory(
        data_file='HideoutDoodads.dat',
        data_mapping=(
            ('IsNonMasterDoodad', {
                'template': 'is_master_doodad',
                'format': lambda v: not v,
            }),
            ('Variation_AOFiles', {
                'template': 'variation_count',
                'format': lambda v: len(v),
            }),
        ),
        row_index=True,
        function=_apply_master_map,
    )

    _type_map = _type_factory(
        data_file='Maps.dat',
        data_mapping=(
            ('Tier', {
                'template': 'map_tier',
            }),
            ('Regular_GuildCharacter', {
                'template': 'map_guild_character',
                'condition': lambda v: v,
            }),
            ('Regular_WorldAreasKey', {
                'template': 'map_area_id',
                'format': lambda v: v['Id'],
            }),
            ('Regular_WorldAreasKey', {
                'template': 'map_area_level',
                'format': lambda v: v['MonsterLevel'],
            }),
            ('Unique_GuildCharacter', {
                'template': 'unique_map_guild_character',
                'condition': lambda v: v != '',
            }),
            ('Unique_WorldAreasKey', {
                'template': 'unique_map_area_id',
                'format': lambda v: v['Id'],
                'condition': lambda v: v is not None,
            }),
            ('Unique_WorldAreasKey', {
                'template': 'unique_map_area_level',
                'format': lambda v: v['MonsterLevel'],
                'condition': lambda v: v is not None,
            }),
        ),
        row_index=True,
    )

    def _essence_extra(self, infobox, base_item_type, essence):
        infobox['is_essence'] = True

        # ClientString is outdated. They're building the description from the
        # mod keys it seems.

        if essence['ClientStringsKey']:
            infobox['description'] += '<br />' + essence['ClientStringsKey'][
                'Text'].replace('\n', '<br />').replace('\r', '')

        return True

    _type_essence = _type_factory(
        data_file='Essences.dat',
        data_mapping=(
            ('DropLevelMinimum', {
                'template': 'drop_level',
            }),
            ('DropLevelMaximum', {
                'template': 'drop_level_maximum',
                'condition': lambda v: v > 0,
            }),
            ('ItemLevelRestriction', {
                'template': 'essence_level_restriction',
                'condition': lambda v: v > 0,
            }),
            ('Tier', {
                'template': 'essence_tier',
                'condition': lambda v: v > 0,
            }),
            ('Monster_ModsKeys', {
                'template': 'essence_monster_modifier_ids',
                'format': lambda v: ', '.join([m['Id'] for m in v]),
                'condition': lambda v: v,
            }),
        ),
        row_index=True,
        function=_essence_extra,
        fail_condition=True,
    )

    _type_labyrinth_trinket = _type_factory(
        data_file='LabyrinthTrinkets.dat',
        data_mapping=(
            ('Buff_BuffDefinitionsKey', {
                'template': 'description',
                'format': lambda v: v['Description'],
            }),
        ),
        row_index=True
    )

    _cls_map = {
        # Armour types
        'Gloves': (_type_level, _type_attribute, _type_armour, ),
        'Boots': (_type_level, _type_attribute, _type_armour, ),
        'Body Armours': (_type_level, _type_attribute, _type_armour, ),
        'Helmets': (_type_level, _type_attribute, _type_armour, ),
        'Shields': (_type_level, _type_attribute, _type_armour, _type_shield),
        # Weapons
        'Claws': (_type_level, _type_attribute, _type_weapon, ),
        'Daggers': (_type_level, _type_attribute, _type_weapon, ),
        'Wands': (_type_level, _type_attribute, _type_weapon, ),
        'One Hand Swords': (_type_level, _type_attribute, _type_weapon, ),
        'Thrusting One Hand Swords': (
            _type_level, _type_attribute, _type_weapon,
        ),
        'One Hand Axes': (_type_level, _type_attribute, _type_weapon, ),
        'One Hand Maces': (_type_level, _type_attribute, _type_weapon, ),
        'Bows': (_type_level, _type_attribute, _type_weapon, ),
        'Staves': (_type_level, _type_attribute, _type_weapon, ),
        'Two Hand Swords': (_type_level, _type_attribute, _type_weapon, ),
        'Two Hand Axes': (_type_level, _type_attribute, _type_weapon, ),
        'Two Hand Maces': (_type_level, _type_attribute, _type_weapon, ),
        'Sceptres': (_type_level, _type_attribute, _type_weapon, ),
        'Fishing Rods': (_type_level, _type_attribute, _type_weapon, ),
        # Flasks
        'Life Flasks': (_type_level, _type_flask, _type_flask_charges),
        'Mana Flasks': (_type_level, _type_flask, _type_flask_charges),
        'Hybrid Flasks': (_type_level, _type_flask, _type_flask_charges),
        'Utility Flasks': (_type_level, _type_flask, _type_flask_charges),
        'Critical Utility Flasks': (_type_level, _type_flask,
                                    _type_flask_charges),
        # Gems
        'Active Skill Gems': (_skill_gem, ),
        'Support Skill Gems': (_skill_gem, ),
        # Currency-like items
        'Currency': (_type_currency, ),
        'Stackable Currency': (_type_currency, _type_essence),
        'Hideout Doodads': (_type_currency, _type_hideout_doodad),
        'Microtransactions': (_type_currency, ),
        # Labyrinth stuff
        #'Labyrinth Item': (),
        'Labyrinth Trinket': (_type_labyrinth_trinket, ),
        #'Labyrinth Map Item': (),
        # Misc
        'Maps': (_type_map,),
        #'Map Fragments': (_type_,),
        'Quest Items': (),
    }

    _conflict_boots_map = {
        'Metadata/Items/Armours/Boots/BootsAtlas1':
            ' (Cold and Lightning Resistance)',
        'Metadata/Items/Armours/Boots/BootsAtlas2':
            ' (Fire and Cold Resistance)',
        'Metadata/Items/Armours/Boots/BootsAtlas3':
            ' (Fire and Lightning Resistance)',
    }

    def _conflict_boots(self, infobox, base_item_type):
        appendix = self._conflict_boots_map.get(
            base_item_type['Id'])
        if appendix is None:
            return
        else:
            infobox['inventory_icon'] = base_item_type['Name'] + appendix
            return base_item_type['Name'] + appendix

    _conflict_amulet_id_map = {
        'Metadata/Items/Amulets/Talismans/Talisman2_6_1':
            ' (Fire Damage taken as Cold Damage)',
        'Metadata/Items/Amulets/Talismans/Talisman2_6_2':
            ' (Fire Damage taken as Lightning Damage)',
        'Metadata/Items/Amulets/Talismans/Talisman2_6_3':
            ' (Cold Damage taken as Fire Damage)',
        'Metadata/Items/Amulets/Talismans/Talisman2_6_4':
            ' (Cold Damage taken as Lightning Damage)',
        'Metadata/Items/Amulets/Talismans/Talisman2_6_5':
            ' (Lightning Damage taken as Cold Damage)',
        'Metadata/Items/Amulets/Talismans/Talisman2_6_6':
            ' (Lightning Damage taken as Fire Damage)',
        'Metadata/Items/Amulets/Talismans/Talisman3_6_1':
            '  (Power Charge on Kill)',
        'Metadata/Items/Amulets/Talismans/Talisman3_6_2':
            '  (Frenzy Charge on Kill)',
        'Metadata/Items/Amulets/Talismans/Talisman3_6_3':
            '  (Endurance Charge on Kill)',
    }

    def _conflict_amulets(self, infobox, base_item_type):
        appendix = self._conflict_amulet_id_map.get(base_item_type['Id'])
        if appendix is None:
            return base_item_type['Name']
        else:
            return base_item_type['Name'] + appendix

    _conflict_active_skill_gems_map = {
        'Metadata/Items/Gems/SkillGemArcticArmour': True,
        'Metadata/Items/Gems/SkillGemPhaseRun': True,
    }

    def _conflict_active_skill_gems(self, infobox, base_item_type):
        appendix = self._conflict_active_skill_gems_map.get(
            base_item_type['Id'])
        if appendix is None:
            return
        else:
            return base_item_type['Name']

    _conflict_quest_item_id_map = {
        'Metadata/Items/QuestItems/SkillBooks/Book-a1q6':
            ' (The Marooned Mariner)',
        'Metadata/Items/QuestItems/SkillBooks/Book-a1q7':
            ' (The Dweller of the Deep)',
        'Metadata/Items/QuestItems/SkillBooks/Book-a1q8':
            ' (A Dirty Job)',
        'Metadata/Items/QuestItems/SkillBooks/Book-a1q9':
            ' (The Way Forward)',
        'Metadata/Items/QuestItems/SkillBooks/Book-a2q5':
            ' (Through Sacred Ground)',
        'Metadata/Items/QuestItems/SkillBooks/Book-a3q9':
            ' (Piety\'s Pets)',
        #'Metadata/Items/QuestItems/SkillBooks/Book-a3q11v0':
        #    ' (6)',
        #'Metadata/Items/QuestItems/SkillBooks/Book-a3q11v1':
        #    ' (7)',
        'Metadata/Items/QuestItems/SkillBooks/Book-a3q11v2':
            ' (Victario\'s Secrets)',
        'Metadata/Items/QuestItems/Act4/Book-a4q6':
            ' (An Indomitable Spirit)',
        'Metadata/Items/QuestItems/SkillBooks/Descent2_1':
            ' (Descent 1)',
        'Metadata/Items/QuestItems/SkillBooks/Descent2_2':
            ' (Descent 2)',
        'Metadata/Items/QuestItems/SkillBooks/Descent2_3':
            ' (Descent 3)',
        'Metadata/Items/QuestItems/SkillBooks/Descent2_4':
            ' (Descent 4)',
        'Metadata/Items/QuestItems/SkillBooks/BanditRespecEramir':
            ' (Eramir)',
        'Metadata/Items/QuestItems/SkillBooks/BanditRespecAlira':
            ' (Alira)',
        'Metadata/Items/QuestItems/SkillBooks/BanditRespecOak':
            ' (Oak)',
        'Metadata/Items/QuestItems/SkillBooks/BanditRespecKraityn':
            ' (Kraityn)',
        'Metadata/Items/QuestItems/GoldenPages/Page1':
            ' (1 of 4)',
        'Metadata/Items/QuestItems/GoldenPages/Page2':
            ' (2 of 4)',
        'Metadata/Items/QuestItems/GoldenPages/Page3':
            ' (3 of 4)',
        'Metadata/Items/QuestItems/GoldenPages/Page4':
            ' (4 of 4)',
        'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier8_1':
            ' (1 of 2)',
        'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier8_2':
            ' (2 of 2)',
        'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier9_1':
            ' (1 of 3)',
        'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier9_2':
            ' (2 of 3)',
        'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier9_3':
            ' (3 of 3)',
        'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier10_1':
            ' (1 of 3)',
        'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier10_2':
            ' (2 of 3)',
        'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier10_3':
            ' (3 of 3)',
    }

    def _conflict_quest_items(self, infobox, base_item_type):
        appendix = self._conflict_quest_item_id_map.get(base_item_type['Id'])
        if appendix is None:
            return
        else:
            if not base_item_type['Id'].startswith('Metadata/Items/QuestItems/'
                                                   'MapUpgrades/'):
                infobox['inventory_icon'] = base_item_type['Name'] + appendix
            return base_item_type['Name'] + appendix

    def _conflict_hideout_doodad(self, infobox, base_item_type):
        try:
            ho = self.rr['HideoutDoodads.dat'].index[
                'BaseItemTypesKey'][base_item_type.rowid]
        except KeyError:
            return

        # This is not perfect, but works currently.
        if ho['NPCMasterKey']:
            if base_item_type['Id'].startswith('Metadata/Items/Hideout/Hideout'
                                               'Wounded'):
                return '%s (%s %s decoration, %s)' % (
                    base_item_type['Name'],
                    ho['NPCMasterKey']['NPCsKey']['ShortName'],
                    ho['MasterLevel'],
                    base_item_type['Id'].replace('Metadata/Items/Hideout/Hideout'
                                                 'Wounded', '')
                )

            return '%s (%s %s decoration)' % (
                base_item_type['Name'],
                ho['NPCMasterKey']['NPCsKey']['ShortName'],
                ho['MasterLevel']
            )
        elif base_item_type['Id'].startswith(
                'Metadata/Items/Hideout/HideoutTotemPole'):
            # Ingore the test doodads on purpose
            if base_item_type['Id'].endswith('Test'):
                return

            match = re.search(
                '(?<=in the )(.*)(?= Leagues)', infobox['help_text']
            )

            if match:
                league = match.group(0)
                if league.endswith('Challenge'):
                    league = league.replace(' Challenge', '')

                return '%s (%s)' % (base_item_type['Name'], league)

    def _conflict_maps(self, infobox, base_item_type):
        id = base_item_type['Id'].replace('Metadata/Items/Maps/Map', '')
        name = None
        # Legacy maps
        if id.startswith('T'):
            name = '%s (pre 2.0)' % base_item_type['Name']
        # 2.0 maps
        elif id.startswith('2'):
            name = '%s (pre 2.4)' % base_item_type['Name']
        elif id.startswith('Atlas'):
            return base_item_type['Name']

        # Each iteration of maps has it's own art
        if name is not None:
            infobox['inventory_icon'] = name
            infobox['drop_enabled'] = False
            return name

    _conflict_microtransactions_map = {
        'Metadata/Items/MicrotransactionCurrency/MysteryBox1x1':
            ' 1x1',
        'Metadata/Items/MicrotransactionCurrency/MysteryBox1x2':
            ' 1x2',
        'Metadata/Items/MicrotransactionCurrency/MysteryBox1x3':
            ' 1x3',
        'Metadata/Items/MicrotransactionCurrency/MysteryBox1x4':
            ' 1x4',
        'Metadata/Items/MicrotransactionCurrency/MysteryBox2x1':
            ' 2x1',
        'Metadata/Items/MicrotransactionCurrency/MysteryBox2x2':
            ' 2x2',
        'Metadata/Items/MicrotransactionCurrency/MysteryBox2x3':
            ' 2x3',
        'Metadata/Items/MicrotransactionCurrency/MysteryBox2x4':
            ' 2x4',
        'Metadata/Items/MicrotransactionCurrency/MysteryBox3x2':
            ' 3x2',
        'Metadata/Items/MicrotransactionCurrency/MysteryBox3x3':
            ' 3x3',
    }

    def _conflict_microtransactions(self, infobox, base_item_type):
        appendix = self._conflict_microtransactions_map.get(
            base_item_type['Id'])
        if appendix is None:
            return
        else:
            infobox['inventory_icon'] = base_item_type['Name'] + appendix
            return base_item_type['Name'] + appendix

    _conflict_resolver_map = {
        'Boots': _conflict_boots,
        'Amulets': _conflict_amulets,
        'Active Skill Gems': _conflict_active_skill_gems,
        'Quest Items': _conflict_quest_items,
        'Hideout Doodads': _conflict_hideout_doodad,
        'Maps': _conflict_maps,
        'Microtransactions': _conflict_microtransactions,
    }

    def _write_stats(self, infobox, stats_and_values, global_prefix):
        for i, val in enumerate(stats_and_values):
            prefix = '%sstat%s_' % (global_prefix, (i + 1))
            infobox[prefix + 'id'] = val[0]
            infobox[prefix + 'value'] = val[1]

    def export(self, parsed_args):
        # Pre processing filters
        valid_classes = [row['Name'] for row in self.rr['ItemClasses.dat']]

        invalid = False
        if parsed_args.item_class:
            for cls in list(parsed_args.item_class):
                if cls not in valid_classes:
                    invalid = True
                    parsed_args.item_class.remove(cls)
                    console('Invalid filter item class: %s' % cls, Msg.error)
        if invalid:
            console('Invalid filters were specified. Search may yield '
                    'unintended results.', Msg.warning)

        itemkey = 'Id' if parsed_args.is_metadata_id else 'Name'

        # Create item list
        items = []
        names = defaultdict(list)
        for row in self.rr['BaseItemTypes.dat']:
            names[row['Name']].append(row)
            # catch exception in case item class was not specified
            try:
                if row['ItemClassesKey'][itemkey] not in parsed_args.item_class:
                    continue
            except TypeError:
                pass

            if row[itemkey] in parsed_args.item:
                items.append(row)

        if not items:
            console('No items found. Exiting...')
            sys.exit(-1)
        else:
            console('Found %s items with matching names' % len(items))

        console('Additional files may be loaded. Processing information - this '
                'may take a while...')

        ggpk = None
        if parsed_args.store_images:
            try:
                import brotli
            except ImportError:
                console(
                    'Brotli was not found. Image extraction will be skipped!',
                    msg=Msg.error,
                )
                parsed_args.store_images = False
            else:
                console(
                    'Images are flagged for extraction. Loading content.ggpk '
                    '...'
                )
                ggpk = GGPKFile()
                ggpk.read(get_content_ggpk_path())
                ggpk.directory_build()
                console('content.ggpk has been loaded.')

        r = ExporterResult()

        for base_item_type in items:
            name = base_item_type['Name']
            cls = base_item_type['ItemClassesKey']['Name']

            infobox = OrderedDict()

            infobox['rarity'] = 'Normal'

            # BaseItemTypes.dat
            infobox['name'] = name
            infobox['class'] = cls
            infobox['size_x'] = base_item_type['Width']
            infobox['size_y'] = base_item_type['Height']
            if base_item_type['FlavourTextKey']:
                infobox['flavour_text'] = base_item_type['FlavourTextKey'][
                    'Text'].replace('\n', '<br>').replace('\r', '')

            if cls not in self._IGNORE_DROP_LEVEL_CLASSES and \
                    name not in self._IGNORE_DROP_LEVEL_ITEMS:
                infobox['drop_level'] = base_item_type['DropLevel']
            try:
                ot = self.ot[base_item_type['Id'] + '.ot']
            except FileNotFoundError:
                ot = self.ot[base_item_type['InheritsFrom'] + '.ot']

            if 'enable_rarity' in ot['Mods']:
                infobox['drop_rarities'] = ', '.join([
                    n[0].upper() + n[1:] for n in ot['Mods']['enable_rarity']
                ])

            tags = [t['Id'] for t in base_item_type['TagsKeys']]
            infobox['tags'] = ', '.join(list(ot['Base']['tag']) + tags)

            infobox['metadata_id'] = base_item_type['Id']

            help_text = ot['Base'].get('description_text')
            if help_text:
                infobox['help_text'] = self.rr['ClientStrings.dat'].index['Id'][
                    help_text]['Text']

            for i, mod in enumerate(base_item_type['Implicit_ModsKeys']):
                infobox['implicit%s' % (i+1)] = mod['Id']

            if base_item_type['IsTalisman']:
                infobox['is_talisman'] = base_item_type['IsTalisman']

            funcs = self._cls_map.get(cls)
            if funcs:
                fail = False
                for f in funcs:
                    if not f(self, infobox, base_item_type):
                        fail = True
                        console(
                            'Required extra info for item "%s" with class "%s"'
                            ' not found. Skipping.' % (name, cls),
                            msg=Msg.error)
                        break
                if fail:
                    continue

            # handle items with duplicate name entries
            if len(names[name]) > 1:
                resolver = self._conflict_resolver_map.get(cls)

                if resolver:
                    name = resolver(self, infobox, base_item_type)
                    if name is None:
                        console(
                            'Unresolved ambiguous item "%s" with name "%s". '
                            'Skipping' %
                            (base_item_type['Id'], infobox['name']),
                            msg=Msg.error
                        )
                        continue
                else:
                    console('No name conflict handler defined for item class '
                            '"%s"' % cls, msg=Msg.error)
                    continue

            # putting this last since it's usually manually added
            if base_item_type['IsTalisman'] or \
                    base_item_type['Name'] in self._DROP_DISABLED_ITEMS:
                infobox['drop_enabled'] = False


            cond = WikiCondition(
                data=infobox,
                cmdargs=parsed_args,
            )

            r.add_result(
                text=cond,
                out_file='item_%s.txt' % name,
                wiki_page=[
                    {
                        'page': name,
                        'condition': cond,
                    }
                ],
                wiki_message='Item exporter',
            )

            if parsed_args.store_images and ggpk:
                if not base_item_type['ItemVisualIdentityKey']['DDSFile']:
                    warnings.warn(
                        'Missing 2d art inventory icon for item "%s"' %
                        base_item_type['Name']
                    )
                    continue

                filepath = os.path.join(self.base_path, 'img')
                if not os.path.exists(filepath):
                    os.makedirs(filepath)

                filepath = os.path.join(filepath, (
                    infobox.get('inventory_icon') or name) +
                    ' inventory icon.dds'
                )

                with open(filepath, 'wb') as f:
                    f.write(extract_dds(
                        ggpk[base_item_type['ItemVisualIdentityKey'][
                            'DDSFile']].record.extract().read(),
                        path_or_ggpk=ggpk,
                    ))

                console('Wrote "%s"' % filepath)

                if not parsed_args.convert_images:
                    continue

                os.system('magick convert "%s" "%s"' % (
                    filepath, filepath.replace('.dds', '.png'),
                ))
                os.remove(filepath)

                console('Converted "%s" to png' % filepath)

        return r

    _conflict_resolver_prophecy_map = {
        'MapExtraHaku': ' (Haku)',
        'MapExtraTora': ' (Tora)',
        'MapExtraCatarina': ' (Catarina)',
        'MapExtraVagan': ' (Vagan)',
        'MapExtraElreon': ' (Elreon)',
        'MapExtraVorici': ' (Vorici)',
        'MapExtraZana': ' (Zana)',
        # The other one is disabled, should be fine
        'MapSpawnRogueExiles': '',
        'MysteriousInvadersFire': ' (Fire)',
        'MysteriousInvadersCold': ' (Cold)',
        'MysteriousInvadersLightning': ' (Lightning)',
        'MysteriousInvadersPhysical': ' (Physical)',
        'MysteriousInvadersChaos': ' (Chaos)',
    }

    def prophecy(self, parsed_args):
        prophecies = []
        names = defaultdict(list)
        for prophecy in self.rr['Prophecies.dat']:
            name = prophecy['Name']
            names[name].append(prophecy)
            if name not in parsed_args.name:
                continue

            if not prophecy['IsEnabled'] and not parsed_args.allow_disabled:
                console(
                    'Propehcy "%s" is disabled - skipping.' % name,
                    msg=Msg.error
                )
                continue

            prophecies.append(prophecy)

        r = ExporterResult()
        for prophecy in prophecies:
            name = prophecy['Name']

            infobox = OrderedDict()

            infobox['rarity'] = 'Normal'
            infobox['name'] = name
            infobox['class'] = 'Stackable Currency'
            infobox['base_item'] = 'Prophecy'
            infobox['flavour_text'] = prophecy['FlavourText']
            infobox['prophecy_id'] = prophecy['Id']
            infobox['prediction_text'] = prophecy['PredictionText']
            infobox['seal_cost_normal'] = prophecy['SealCost_Normal']
            infobox['seal_cost_cruel'] = prophecy['SealCost_Cruel']
            infobox['seal_cost_merciless'] = prophecy['SealCost_Merciless']

            if not prophecy['IsEnabled']:
                infobox['drop_enabled'] = False

            # handle items with duplicate name entries
            if len(names[name]) > 1:
                extra = self._conflict_resolver_prophecy_map.get(prophecy['Id'])
                if extra is None:
                    console('Unresolved ambiguous item name "%s" / id "%s". '
                            'Skipping' % (prophecy['Name'], prophecy['Id']),
                            msg=Msg.error)
                    continue
                name += extra
            cond = WikiCondition(
                data=infobox,
                cmdargs=parsed_args,
            )

            r.add_result(
                text=cond,
                out_file='item_%s.txt' % name,
                wiki_page=[
                    {'page': name, 'condition': cond},
                    {'page': name + ' (prophecy)', 'condition': cond},
                ],
                wiki_message='Prophecy exporter',
            )

        return r
