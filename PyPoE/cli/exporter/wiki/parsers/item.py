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
from PyPoE.poe.file.stat_filters import StatFilterFile, SkillEntry
from PyPoE.poe.sim.formula import gem_stat_requirement, GemTypes
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter.wiki.handler import *
from PyPoE.cli.exporter.wiki.parser import *

# =============================================================================
# Classes
# =============================================================================

class ItemsWikiHandler(WikiHandler):
    # This only works as long there aren't nested templates inside the infobox
    regex_search = re.compile(
        '\{\{Item\n'
        '(?P<data>[^\}]*)'
        '\n\}\}',
        re.UNICODE | re.IGNORECASE | re.MULTILINE | re.DOTALL
    )

    regex_infobox_split = re.compile(
        '\|(?P<key>[\S]+)[\s]*=[\s]*(?P<value>[^|]*)',
        re.UNICODE | re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    COPY_KEYS = (
        'radius',
        'has_percentage_mana_cost',
        'has_reservation_mana_cost',
        'drop_enabled',
        'name_list',
    )

    def _find_page(self, page_name):
        page = self.pws.pywikibot.Page(self.site, page_name)
        itembox = self.regex_search.search(page.text)

        if itembox:
            return page, itembox
        else:
            console('Failed to find the item page on wiki page "%s"' % page_name, msg=Msg.warning)
            return None, None

    def handle_page(self, *a, row):
        page_name = row['wiki_page']
        console('Editing gem "%s"...' % page_name)
        page, itembox = self._find_page(page_name)
        if page is None:
            if row['infobox']['class'] == 'Support Skill Gems':
                page, itembox = self._find_page('%s (support gem)' % page_name)

        if page is None:
            console('Can\'t find working wikipage. Skipping.', Msg.error)
            return

        for match in self.regex_infobox_split.finditer(itembox.group('data')):
            k = match.group('key')
            if k in self.COPY_KEYS:
                row['infobox'][k] = match.group('value').strip('\n\r ')

        infobox_text = format_result_rows(
            parsed_args=self.cmdargs,
            template_name='Item',
            indent=33,
            ordered_dict=row['infobox'],
        )

        # I need the +1 offset or it adds a space everytime for some reason.
        new_text = page.text[:itembox.start()] + ''.join(infobox_text) + \
                   page.text[itembox.end()+1:]

        self.save_page(
            page=page,
            text=new_text,
            message='Item export',
        )


class ItemsHandler(ExporterHandler):
    def __init__(self, sub_parser, *args, **kwargs):
        super(ItemsHandler, self).__init__(self, sub_parser, *args, **kwargs)
        self.parser = sub_parser.add_parser('items', help='Items Exporter')
        self.parser.set_defaults(func=lambda args: self.parser.print_help())
        sub = self.parser.add_subparsers()

        parser = sub.add_parser(
            'export',
            help='Extracts the item information'
        )
        self.add_default_parsers(
            parser=parser,
            cls=ItemsParser,
            func=ItemsParser.export,
            wiki_handler=ItemsWikiHandler(name='Item Export'),
        )

        add_format_argument(parser)

        parser.add_argument(
            '-ft-c', '--filter-class',
            help='Filter by item class(es). Case sensitive.',
            nargs='*',
            dest='item_class',
        )

        parser.add_argument(
            'item',
            help='Name of the item; can be specified multiple times',
            nargs='+',
        )


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

    _cp_columns = (
        'Level', 'LevelRequirement', 'ManaMultiplier', 'CriticalStrikeChance',
        'ManaCost', 'DamageMultiplier', 'VaalSouls', 'VaalStoredUses',
        'Cooldown', 'StoredUses', 'DamageEffectiveness'
    )

    _skill_column_map = OrderedDict((
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
    ))

    _currency_column_map = OrderedDict((
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
    ))

    _flask_charges_column_map = OrderedDict((
        ('MaxCharges', {
            'template': 'charges_max',
        }),
        ('PerCharge', {
            'template': 'charges_per_use',
        }),
    ))

    _flask_column_map = OrderedDict((
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
    ))

    _attribute_requirements_column_map = OrderedDict((
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
    ))

    _armour_column_map = OrderedDict((
        ('Armour', {
            'template': 'armour',
            'condition': lambda v: v > 0,
        }),
        ('Evasion', {
            'template': 'evasion',
            'condition': lambda v: v > 0,
        }),
        ('EnergyShield', {
            'template': 'enery_shield',
            'condition': lambda v: v > 0,
        }),
    ))

    _shield_column_map = OrderedDict((
        ('Block', {
            'template': 'block',
        }),
    ))

    _weapon_column_map = OrderedDict((
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
    ))

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
                self.base_path, 'Metadata', 'skillpopup_stat_filters.txt'
            ))
            #TODO remove once fixed
            self._skill_stat_filters.skills['spirit_offering'] = SkillEntry(skill_id='spirit_offering', translation_file_path='Metadata/offering_skill_stat_descriptions.txt', stats=[])

        return self._skill_stat_filters

    def _apply_column_map(self, infobox, column_map, list_object):
        for k, data in column_map.items():
            value = list_object[k]
            if data.get('condition') and not data['condition'](value):
                continue

            if data.get('format'):
                value = data['format'](value)
            infobox[data['template']] = value

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

        ae = gepl[0]['ActiveSkillsKey']

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

        # From ActiveSkills.dat
        if ae:
            infobox['cast_time'] = ae['CastTime'] / 1000
            infobox['gem_description'] = ae['Description']
            infobox['active_skill_name'] = ae['DisplayedName']
            if ae['WeaponRestriction_ItemClassesKeys']:
                # The class name may be empty for reason, causing issues
                infobox['item_class_restriction'] = ', '.join([
                    c['Name'] if c['Name'] else c['Id'] for c in
                    ae['WeaponRestriction_ItemClassesKeys']
                ])

        # From GrantedEffects.dat

        infobox['skill_id'] = ge['Id']
        infobox['is_support_gem'] = ge['IsSupport']
        if ge['SupportGemLetter']:
            infobox['support_gem_letter'] = ge['SupportGemLetter']

        # GrantedEffectsPerLevel.dat
        infobox['required_level'] = level_data[0]['LevelRequirement']

        # Don't add columns that are zero/default
        for column, column_data in self._skill_column_map.items():
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

        infobox['stat_text'] = '<br>'.join(lines)
        self._write_stats(infobox, zip(stats, values), 'static_')

        # Quality stats
        lines = []
        stats = []
        values = []
        for key in static['qstats']:
            stat_dict = level_data[0]['qstats'][key]
            lines.append(stat_dict['line'])
            stats.extend(stat_dict['stats'])
            values.extend(stat_dict['values'])

        infobox['quality_stat_text'] = '<br>'.join(lines)
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
            for column, column_data in self._skill_column_map.items():
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
                        '<br>'.join(lines)
                self._write_stats(
                    infobox, zip(stats, values), prefix + stat_prefix
                )

            try:
                infobox[prefix + 'experience'] = exp_total[i]
            except IndexError:
                pass

        return True

    def _type_attribute(self, infobox, base_item_type):
        try:
            requirements = self.rr['ComponentAttributeRequirements.dat'].index[
                'BaseItemTypesKey'][base_item_type['Id']]
        except KeyError:
            warnings.warn('Missing attribute for "%s"' % base_item_type['Name'])
            return False

        self._apply_column_map(
            infobox, self._attribute_requirements_column_map, requirements
        )

        return True

    def _type_armour(self, infobox, base_item_type):
        try:
            armour = self.rr['ComponentArmour.dat'].index[
                'BaseItemTypesKey'][base_item_type['Id']]
        except KeyError:
            warnings.warn(
                'Missing armor info for "%s"' % base_item_type['Name']
            )
            return False

        self._apply_column_map(infobox, self._armour_column_map, armour)

        return True

    def _type_shield(self, infobox, base_item_type):
        try:
            shields = self.rr['ShieldTypes.dat'].index[
                'BaseItemTypesKey'][base_item_type.rowid]
        except KeyError:
            warnings.warn(
                'Missing shield info for "%s"' % base_item_type['Name']
            )
            return False

        self._apply_column_map(infobox, self._shield_column_map, shields)

        return True

    def _type_flask(self, infobox, base_item_type):
        try:
            flask_charges = self.rr['ComponentCharges.dat'].index[
                'BaseItemTypesKey'][base_item_type['Id']]
            flasks = self.rr['Flasks.dat'].index['BaseItemTypesKey'][
                base_item_type.rowid]
        except KeyError:
            warnings.warn(
                'Missing flask info for "%s"' % base_item_type['Name']
            )
            return False

        self._apply_column_map(
            infobox, self._flask_charges_column_map, flask_charges
        )
        self._apply_column_map(infobox, self._flask_column_map, flasks)

        #TODO: BuffDefinitionsKey, BuffStatValues

        return True

    def _type_weapon(self, infobox, base_item_type):
        try:
            weapons = self.rr['WeaponTypes.dat'].index[
                'BaseItemTypesKey'][base_item_type.rowid]
        except KeyError:
            warnings.warn(
                'Missing weapon info for "%s"' % base_item_type['Name']
            )
            return False

        self._apply_column_map(infobox, self._weapon_column_map, weapons)

        return True

    def _type_currency(self, infobox, base_item_type):
        try:
            currency = self.rr['CurrencyItems.dat'].index('BaseItemTypesKey')[
                base_item_type.rowid]
        except KeyError:
            warnings.warn(
                'Missing currency info for "%s"' % base_item_type['Name']
            )
            return False

        self._apply_column_map(infobox, self._currency_column_map, currency)

        return True

    def _type_level(self, infobox, base_item_type):
        infobox['required_level'] = base_item_type['DropLevel']

        return True

    _cls_map = {
        # Armour types
        'Gloves': (_type_level, _type_attribute, _type_armour, ),
        'Boots': (_type_level, _type_attribute, _type_armour, ),
        'Body Armours': (_type_level, _type_attribute, _type_armour, ),
        'Helments': (_type_level, _type_attribute, _type_armour, ),
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
        'Life Flasks': (_type_level, _type_flask, ),
        'Mana Flasks': (_type_level, _type_flask, ),
        'Hybrid Flasks': (_type_level, _type_flask, ),
        'Utility Flasks': (_type_level, _type_flask, ),
        'Critical Utility Flasks': (_type_level, _type_flask, ),
        # Gems
        'Active Skill Gems': (_skill_gem, ),
        'Support Skill Gems': (_skill_gem, ),
        # Currency-like items
        'Currency': (_type_currency, ),
        'Stackable Currency': (_type_currency, ),
        'Hideout Doodads': (_type_currency, ),
        'Microtransactions': (_type_currency, ),
        # Misc
        #'Maps': (_type_,),
        #'Map Fragments': (_type_,),
    }

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

        # Create item lsit
        items = []
        for row in self.rr['BaseItemTypes.dat']:
            # catch exception in case item class was not specified
            try:
                if row['ItemClassesKey']['Name'] not in parsed_args.item_class:
                    continue
            except TypeError:
                pass

            if row['Name'] in parsed_args.item:
                items.append(row)

        if not items:
            console('No items found. Exiting...')
            sys.exit(-1)
        else:
            console('Found %s items with matching names' % len(items))

        console('Additional files may be loaded. Processing information - this '
                'may take a while...')

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
            infobox['drop_level'] = base_item_type['DropLevel']
            if base_item_type['FlavourTextKey']:
                infobox['flavour_text'] = base_item_type['FlavourTextKey'][
                    'Text'].replace('\n', '<br>')

            ot = self.ot[base_item_type['InheritsFrom'] + '.ot']

            tags = [t['Id'] for t in base_item_type['TagsKeys']]
            infobox['tags'] = ', '.join(list(ot['Base']['tag']) + tags)

            infobox['metadata_id'] = base_item_type['Id']

            for i, mod in enumerate(base_item_type['Implicit_ModsKeys']):
                infobox['mod%s' % (i+1)] = mod['Id']

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

            format_result_rows(
                parsed_args=parsed_args,
                template_name='Item',
                indent=33,
                ordered_dict=infobox,
            )

            r.add_result(
                lines=format_result_rows(
                    parsed_args=parsed_args,
                    template_name='Item',
                    indent=33,
                    ordered_dict=infobox,
                ),
                out_file='item_%s.txt' % name,
                wiki_page=name,
                infobox=infobox,
            )

        return r

    def _write_stats(self, infobox, stats_and_values, global_prefix):
        for i, val in enumerate(stats_and_values):
            prefix = '%sstat%s_' % (global_prefix, (i + 1))
            infobox[prefix + 'id'] = val[0]
            infobox[prefix + 'value'] = val[1]