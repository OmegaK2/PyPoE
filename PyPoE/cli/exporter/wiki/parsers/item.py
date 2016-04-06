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
from PyPoE.poe.file.stat_filters import StatFilterFile
from PyPoE.poe.sim.formula import gem_stat_requirement, GemTypes
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter.wiki.handler import *
from PyPoE.cli.exporter.wiki.parser import BaseParser

# =============================================================================
# Data
# =============================================================================

_LINE_FORMAT = '|{0: <33}= {1}\n'

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
        'radius', 'has_percentage_mana_cost', 'has_reservation_mana_cost'
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
            if row['infobox'] == 'Support Skill Gems':
                page, itembox = self._find_page('%s (support gem)' % page_name)

        if page is None:
            console('Can\'t find working wikipage. Skipping.', Msg.error)
            return

        for match in self.regex_infobox_split.finditer(itembox.group('data')):
            k = match.group('key')
            if k in self.COPY_KEYS:
                row['infobox'][k] = match.group('value').strip('\n\r ')

        infobox_text = ['{{Item\n', ]
        for k, v in row['infobox'].items():
            infobox_text.append(_LINE_FORMAT.format(k, v))
        infobox_text.append('}}')

        new_text = page.text[:itembox.start()] + ''.join(infobox_text) + \
                   page.text[itembox.end():]

        self.save_page(
            page=page,
            text=new_text,
            message='Item export',
        )


class ItemsHandler(ExporterHandler):
    def __init__(self, sub_parser):
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

        parser.add_argument(
            '--format',
            help='Output format',
            choices=['template', 'module'],
            default='template',
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

    _column_map = OrderedDict((
        ('ManaCost', {
            'template': 'mana_cost',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v),
        }),
        ('ManaMultiplier', {
            'template': 'mana_multiplier',
            'default': 100,
            'format': lambda v: '{0:n}'.format(v),
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
            'default': None,
            'format': lambda v: '{0:n}'.format(v/100),
        }),
        ('DamageEffectiveness', {
            'template': 'damage_effectiveness',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v+100),
        }),
        ('DamageMultiplier', {
            'template': 'damage_multiplier',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v/100+100),
        }),
    ))

    _attribute_map = {
        'Str': 'Strength',
        'Dex': 'Dexterity',
        'Int': 'Intelligence',
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
        return self._skill_stat_filters

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
                warnings.warn('Missing active skill: %s' % e.args[0])
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

            tr = tf.get_translation(
                tags=[r['Id'] for r in row['StatsKeys']],
                values=row['StatValues'],
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
                new = []
                for v in stat_dict['values']:
                    v /= 20
                    if v.is_integer():
                        v = int(v)
                    new.append(v)
                stat_dict['values'] = new
                stat_dict['line'] = stat_dict['line'].format(
                    *stat_dict['values']
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

        # Remove columns that are zero/default
        for key in list(static['columns']):
            if level_data[0][key] == 0:
                static['columns'].remove(key)

        #
        # Output handling for gem infobox
        #


        #TODO: Implicit_ModsKeys

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

        # From GrantedEffects.dat

        infobox['skill_id'] = ge['Id']
        infobox['is_support_gem'] = ge['IsSupport']
        if ge['SupportGemLetter']:
            infobox['support_gem_letter'] = ge['SupportGemLetter']

        # GrantedEffectsPerLevel.dat
        infobox['required_level'] = level_data[0]['LevelRequirement']


        for column, column_data in self._column_map.items():
            if column not in static['columns']:
                continue
            if gepl[0][column] == column_data['default']:
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
            for column, column_data in self._column_map.items():
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

    _cls_map = {
        'Active Skill Gems': _skill_gem,
        'Support Skill Gems': _skill_gem,
    }

    def export(self, parsed_args):
        items = [r for r in self.rr['BaseItemTypes.dat'] if r['Name']
                 in parsed_args.item]

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

            f = self._cls_map.get(cls)
            if f and not f(self, infobox, base_item_type):
                console('Required extra info for item "%s" with class "%s" not'
                        'found. Skipping.' % (name, cls), msg=Msg.error)
                continue

            if parsed_args.format == 'template':
                out = ['{{Item\n']
                for k, v in infobox.items():
                    out.append(_LINE_FORMAT.format(k, v))
                out.append('}}\n')
            elif parsed_args.format == 'module':
                out = ['{']
                for k, v in infobox.items():
                    out.append('{0} = "{1}", '.format(k, v))
                out.append('}')

            r.add_result(
                lines=out,
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