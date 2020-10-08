"""
Wiki lua exporter

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/wiki/parsers/skill.py                         |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

This small script reads the data from quest rewards and exports it to a lua
table for use on the unofficial Path of Exile wiki located at:
http://pathofexile.gamepedia.com

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
import warnings
import traceback
from collections import OrderedDict, defaultdict

# Self
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter import config
from PyPoE.cli.exporter.wiki.handler import ExporterHandler, ExporterResult
from PyPoE.cli.exporter.wiki import parser
from PyPoE.poe.file.stat_filters import StatFilterFile

# =============================================================================
# Globals
# =============================================================================

__all__ = ['SkillHandler']


# =============================================================================
# Functions
# =============================================================================

# =============================================================================
# Classes
# =============================================================================


class SkillHandler(ExporterHandler):
    def __init__(self, sub_parser):
        self.parser = sub_parser.add_parser('skill', help='Skill data Exporter')
        self.parser.set_defaults(func=lambda args: self.parser.print_help())
        skill_sub = self.parser.add_subparsers()

        s_id = skill_sub.add_parser(
            'by_id',
            help='Extract skill information by id.',
        )
        self.add_default_parsers(
            parser=s_id,
            cls=SkillParser,
            func=SkillParser.by_id,
        )
        s_id.add_argument(
            'skill_id',
            help='Id of the area, can be specified multiple times.',
            nargs='+',
        )

        # by row ID
        s_rid = skill_sub.add_parser(
            'by_row',
            help='Extract areas by rowid.'
        )
        self.add_default_parsers(
            parser=s_rid,
            cls=SkillParser,
            func=SkillParser.by_rowid,
        )
        s_rid.add_argument(
            'start',
            help='Starting index',
            nargs='?',
            type=int,
            default=0,
        )
        s_rid.add_argument(
            'end',
            nargs='?',
            help='Ending index',
            type=int,
        )

    def add_default_parsers(self, *args, **kwargs):
        super().add_default_parsers(*args, **kwargs)
        self.add_format_argument(kwargs['parser'])
        self.add_image_arguments(kwargs['parser'])
        kwargs['parser'].add_argument(
            '--allow-skill-gems',
            action='store_true',
            help='Disable the check that prevents skill gems skill from being '
                 'exported.',
            dest='allow_skill_gems',
        )


class WikiCondition(parser.WikiCondition):
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
        'skill_screenshot',
        'skill_screenshot_file',
    )

    NAME = 'Skill'
    INDENT = 40
    ADD_INCLUDE = False


class SkillParserShared(parser.BaseParser):
    _files = [
        # pretty much chain loads everything we need
        'ActiveSkills.dat',
        'GrantedEffects.dat',
        'GrantedEffectsPerLevel.dat',
        'GrantedEffectQualityStats.dat',
    ]

    _GEPL_COPY = (
        'Level', 'LevelRequirement', 'ManaMultiplier', 'CriticalStrikeChance',
        'ManaCost', 'DamageMultiplier', 'VaalSouls', 'VaalStoredUses',
        'VaalSoulGainPreventionTime', 'Cooldown', 'StoredUses',
        'DamageEffectiveness', 'DamageMultiplier', 'AttackSpeedMultiplier',
        'BaseDuration',
    )

    _SKILL_COLUMN_MAP = (
        ('ManaCost', {
            'template': 'mana_cost',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v),
        }),
        ('ManaMultiplier', {
            'template': 'mana_multiplier',
            'format': lambda v: '{0:n}'.format(v),
            'skip_active': True,
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
        ('VaalSoulGainPreventionTime', {
            'template': 'vaal_soul_gain_prevention_time',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v/1000),
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
        ('AttackSpeedMultiplier', {
            'template': 'attack_speed_multiplier',
            'format': lambda v: '{0:n}'.format(v+100),
        }),
        ('BaseDuration', {
            'template': 'duration',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v / 1000),
        }),
    )

    # Values without the Metadata/Projectiles/ prefix
    _SKILL_ID_TO_PROJECTILE_MAP = {
        'ArcticBreath': 'ArcticBreath',
        'BallLightning': 'BallLightningPlayer',
        'BurningArrow': 'BurningArrow',
        'EtherealKnives': 'ShadowProjectile',
        'FlameTotem': 'TotemFireSpray',
        'FreezingPulse': 'FreezingPulse',
        'ExplosiveArrow': 'FuseArrow',
        'FrostBlades': 'IceStrikeProjectile',
        'FrostBolt': 'FrostBolt',
        'Fireball': 'Fireball',
        'IceShot': 'IceArrow',
        'IceSpear': 'IceSpear',
        'Incinerate': 'Flamethrower1',
        'LightningArrow': 'LightningArrow',
        'LightningTrap': 'LightningTrap',
        'MoltenStrike': 'FireMortar',
        # CausticArrow
        'PoisonArrow': 'CausticArrow',
        'Power Siphon': 'Siphon',
        'ShrapnelShot': 'ShrapnelShot',
        'SiegeBallista': 'CrossbowSnipeProjectile',
        'Spark': 'Spark',
        'SplitArrow': 'SplitArrowDefault',
        #Spectral Throw
        'ThrownWeapon': 'ThrownWeapon',
        'Tornado Shot': 'TornadoShotArrow',
        # TornadoShotSecondaryArrow,
        'VaalBurningArrow': 'VaalBurningArrow',
        'WildStrike': 'ElementalStrikeColdProjectile',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            self._skill_stat_filters.read(self.file_system.get_file(
                'Metadata/StatDescriptions/skillpopup_stat_filters.txt'
            ))
            #TODO remove once fixed
            #self._skill_stat_filters.skills['spirit_offering'] = SkillEntry(skill_id='spirit_offering', translation_file_path='Metadata/StatDescriptions/offering_skill_stat_descriptions.txt', stats=[])

        return self._skill_stat_filters

    def _write_stats(self, infobox, stats_and_values, global_prefix):
        for i, val in enumerate(stats_and_values):
            prefix = '%sstat%s_' % (global_prefix, (i + 1))
            infobox[prefix + 'id'] = val[0]
            infobox[prefix + 'value'] = val[1]

    def _skill(self, ge, infobox, parsed_args, max_level=None, msg_name=None):
        if msg_name is None:
            msg_name = ge['Id']

        gepl = []
        for row in self.rr['GrantedEffectsPerLevel.dat']:
            if row['GrantedEffectsKey'] == ge:
                gepl.append(row)

        if not gepl:
            console('No level progression found for "%s". Skipping.' %
                    msg_name, msg=Msg.error)
            return False

        gepl.sort(key=lambda x: x['Level'])
        if max_level is None:
            max_level = len(gepl)-1

        ae = ge['ActiveSkillsKey']
        if ae:
            try:
                tf = self.tc[self.skill_stat_filter.skills[
                    ae['Id']].translation_file_path]
            except KeyError as e:
                warnings.warn('Missing active skill in stat filers: %s' % e.args[0])
                tf = self.tc['skill_stat_descriptions.txt']

            if parsed_args.store_images and ae['Icon_DDSFile']:
                self._write_dds(
                    data=self.file_system.get_file(ae['Icon_DDSFile']),
                    out_path=os.path.join(
                        self._img_path,
                        '%s skill icon.dds' % msg_name
                    ),
                    parsed_args=parsed_args,
                )
        else:
            tf = self.tc['gem_stat_descriptions.txt']

        # reformat the datas we need
        level_data = []
        stat_key_order = {
            'stats': OrderedDict(),
        }

        for i, row in enumerate(gepl):
            data = defaultdict()

            stats = [r['Id'] for j, r in enumerate(row['StatsKeys'])
                     if j < len(row['StatValues'])] + \
                    [r['Id'] for r in row['StatsKeys2']]
            values = row['StatValues'] + ([1, ] * len(row['StatsKeys2']))

            # Remove 0 (unused) stats
            remove_ids = [
                stat for stat, value in zip(stats, values) if value == 0
            ]
            for stat_id in remove_ids:
                index = stats.index(stat_id)
                if values[index] == 0:
                    del stats[index]
                    del values[index]

            tr = tf.get_translation(
                tags=stats,
                values=values,
                full_result=True,
                lang=config.get_option('language'),
            )
            data['_tr'] = tr

            data['stats'] = {}

            for j, stats in enumerate(tr.found_ids):
                values = list(tr.values[j])
                stats = list(stats)
                values_parsed = list(tr.values_parsed[j])
                # Skip zero stats again, since some translations might
                # provide them
                while True:
                    try:
                        index = values.index(0)
                    except ValueError:
                        break

                    try:
                        del values[index]
                    except IndexError:
                        pass

                    try:
                        del values_parsed[index]
                    except IndexError:
                        pass

                    try:
                        del stats[index]
                    except IndexError:
                        pass
                if tr.values[j] == 0:
                    continue
                k = '__'.join(stats)
                stat_key_order['stats'][k] = None
                data['stats']['__'.join(stats)] = {
                    'line': tr.found_lines[j],
                    'stats': stats,
                    'values': values,
                    'values_parsed': values_parsed,
                }
            for stat, value in tr.missing:
                warnings.warn('Missing translation for %s' % stat)
                stat_key_order['stats'][stat] = None
                data['stats'][stat] = {
                    'line': '',
                    'stats': [stat, ],
                    'values': [value, ],
                    'values_parsed': [value, ],
                }

            for column in self._GEPL_COPY:
                data[column] = row[column]

            level_data.append(data)

        # Find static & dynamic stats..

        static = {
            'columns': set(self._GEPL_COPY),
            'stats': OrderedDict(stat_key_order['stats']),
        }
        dynamic = {
            'columns': set(),
            'stats': OrderedDict(),
        }
        last = level_data[0]
        for data in level_data[1:]:
            for key in list(static['columns']):
                if last[key] != data[key]:
                    static['columns'].remove(key)
                    dynamic['columns'].add(key)
            for key in list(static['stats']):
                if key not in last['stats']:
                    continue
                if key not in data['stats']:
                    continue

                if last['stats'][key]['values'] != data['stats'][key][
                        'values']:
                    del static['stats'][key]
                    dynamic['stats'][key] = None
            last = data

        #
        # Output handling for gem infobox
        #

        # From ActiveSkills.dat
        if ae:
            infobox['gem_description'] = ae['Description']
            infobox['active_skill_name'] = ae['DisplayedName']
            if ae['WeaponRestriction_ItemClassesKeys']:
                infobox['item_class_id_restriction'] = ', '.join([
                    c['Id'] for c in ae['WeaponRestriction_ItemClassesKeys']
                ])

        # From Projectile.dat if available
        # TODO - remap
        key = self._SKILL_ID_TO_PROJECTILE_MAP.get(ge['Id'])
        if key:
            infobox['projectile_speed'] = self.rr['Projectiles.dat'].index[
                'Id']['Metadata/Projectiles/' + key]['ProjectileSpeed']

        # From GrantedEffects.dat

        infobox['skill_id'] = ge['Id']
        if ge['SupportGemLetter']:
            infobox['support_gem_letter'] = ge['SupportGemLetter']

        if not ge['IsSupport']:
            infobox['cast_time'] = ge['CastTime'] / 1000

        # GrantedEffectsPerLevel.dat
        infobox['required_level'] = level_data[0]['LevelRequirement']


        #
        # Quality stats
        #
        geq = []
        for row in self.rr['GrantedEffectQualityStats.dat']:
            if row['GrantedEffectsKey'] == ge:
                geq.append(row)

        geq.sort(key=lambda row: row['SetId'])

        for row in geq:
            prefix = 'quality_type%s_' % \
                     (row['SetId'] + 1)
            infobox[prefix + 'weight'] = row['Weight']

            # Quality stat data
            stat_ids = [r['Id'] for r in row['StatsKeys']]
            qtr = tf.get_translation(
                tags=stat_ids,
                # Offset Q1000
                values=[v // 50 for v in row['StatsValuesPermille']],
                full_result=True,
                lang=config.get_option('language'),
            )

            lines = []
            for i, ts in enumerate(qtr.string_instances):
                values = []
                for stat_id in qtr.found_ids[i]:
                    try:
                        index = stat_ids.index(stat_id)
                    except ValueError:
                        values.append(0)
                    else:
                        values.append(
                            row['StatsValuesPermille'][index] / 1000
                        )
                lines.append(ts.format_string(
                    values=values,
                    is_range=[False, ] * len(values),
                )[0])

            infobox[prefix + 'stat_text'] = '<br>'.join(lines)

            self._write_stats(
                infobox,
                zip(stat_ids, row['StatsValuesPermille']),
                prefix,
            )

        #
        # GrantedEffectsPerLevel.dat
        #

        # Don't add columns that are zero/default
        for column, column_data in self._SKILL_COLUMN_MAP:
            if column not in static['columns']:
                continue

            default = column_data.get('default')
            if default is not None and gepl[0][column] == \
                    column_data['default']:
                continue

            df = column_data.get('skip_active')
            if df is not None and not ge['IsSupport']:
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
                try:
                    sdict = level_data[0]['stats'][key]
                except:
                    sdict = level_data[-1]['stats'][key]
                line = sdict['line']
                stats.extend(sdict['stats'])
                values.extend(sdict['values'])
            elif key in dynamic['stats']:
                try:
                    stat_dict_max = level_data[max_level]['stats'][key]
                except KeyError:
                    maxerr = True
                else:
                    maxerr = False

                # Stat was 0
                try:
                    stat_dict = level_data[0]['stats'][key]
                except KeyError:
                    minerr = True
                else:
                    minerr = False

                if not maxerr and not minerr:
                    stat_ids = stat_dict['stats']
                elif maxerr and not minerr:
                    stat_ids = stat_dict['stats']
                    stat_dict_max = {'values': [0] * len(stat_ids)}
                elif not maxerr and minerr:
                    stat_ids = stat_dict_max['stats']
                    stat_dict = {'values': [0] * len(stat_ids)}
                elif maxerr and minerr:
                    console('Neither min or max skill available. Investigate.',
                            msg=Msg.error)
                    return

                tr_values = []
                for j, value in enumerate(stat_dict['values']):
                    tr_values.append((value, stat_dict_max['values'][j]))

                # Should only be one
                line = tf.get_translation(stat_ids, tr_values,
                                          lang=config.get_option('language'))
                line = line[0] if line else ''

            if line:
                lines.append(line)

        self._write_stats(infobox, zip(stats, values), 'static_')

        # Add the attack damage stat from the game data
        if ae:
            field_stats = (
                (
                    ('DamageMultiplier', ),
                    ('active_skill_attack_damage_final_permyriad', ),
                ),
                (
                    ('BaseDuration', ),
                    ('base_skill_effect_duration', ),
                )
            )
            added = []
            for value_keys, tags in field_stats:
                values = [
                    (level_data[0][key], level_data[max_level][key])
                    for key in value_keys
                ]
                # Account for default (0 = 100%)
                if values[0] != 0 or values[1] != 0:
                    added.extend(tf.get_translation(
                        tags=tags,
                        values=values,
                        lang=config.get_option('language'),
                    ))

            if added:
                lines = added + lines

        infobox['stat_text'] = self._format_lines(lines)

        #
        # Output handling for progression
        #

        # Body
        for i, row in enumerate(level_data):
            prefix = 'level%s' % (i + 1)
            infobox[prefix] = 'True'

            prefix += '_'

            infobox[prefix + 'level_requirement'] = row['LevelRequirement']

            # Column handling
            for column, column_data in self._SKILL_COLUMN_MAP:
                if column not in dynamic['columns']:
                    continue
                # Removed the check of defaults on purpose, makes sense
                # to add the info since it is dynamically changed
                infobox[prefix + column_data['template']] = \
                    column_data['format'](row[column])

            # Stat handling
            lines = []
            values = []
            stats = []
            for key in stat_key_order['stats']:
                if key not in dynamic['stats']:
                    continue

                try:
                    stat_dict = row['stats'][key]
                # No need to add stat that don't exist at specific levels
                except KeyError:
                    continue
                # Don't add empty lines
                if stat_dict['line']:
                    lines.append(stat_dict['line'])
                stats.extend(stat_dict['stats'])
                values.extend(stat_dict['values'])
            if lines:
                infobox[prefix + 'stat_text'] = \
                    self._format_lines(lines)
            self._write_stats(
                infobox, zip(stats, values), prefix
            )

        return True


class SkillParser(SkillParserShared):
    def by_id(self, parsed_args):
        return self.export(
            parsed_args,
            self._column_index_filter(
                dat_file_name='GrantedEffects.dat',
                column_id='Id',
                arg_list=parsed_args.skill_id,
            ),
        )

    def by_rowid(self, parsed_args):
        return self.export(
            parsed_args,
            self.rr['GrantedEffects.dat'][parsed_args.start:parsed_args.end],
        )

    def export(self, parsed_args, skills):
        self._image_init(parsed_args=parsed_args)
        console('Found %s skills, parsing...' % len(skills))
        self.rr['SkillGems.dat'].build_index('GrantedEffectsKey')
        r = ExporterResult()
        for skill in skills:
            if not parsed_args.allow_skill_gems and skill in \
                    self.rr['SkillGems.dat'].index['GrantedEffectsKey']:
                console(
                    'Skipping skill gem skill "%s"' % skill['Id'],
                    msg=Msg.warning)
                continue
            data = OrderedDict()

            try:
                self._skill(ge=skill, infobox=data, parsed_args=parsed_args)
            except Exception as e:
                console(
                    'Error when parsing skill "%s":' % skill['Id'],
                    msg=Msg.error)
                console(traceback.format_exc(), msg=Msg.error)

            cond = WikiCondition(
                data=data,
                cmdargs=parsed_args,
            )

            r.add_result(
                text=cond,
                out_file='skill_%s.txt' % data['skill_id'],
                wiki_page=[
                    {
                        'page': 'Skill:' + self._format_wiki_title(
                            data['skill_id']),
                        'condition': cond,
                    },
                ],
                wiki_message='Skill updater',
            )

        return r