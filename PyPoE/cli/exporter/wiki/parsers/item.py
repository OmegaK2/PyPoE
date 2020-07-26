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

# TODO
Kishara's Star (item)
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
import warnings
import os
from collections import OrderedDict, defaultdict
from functools import partialmethod

# Self
from PyPoE.poe.constants import RARITY
from PyPoE.poe.file.dat import RelationalReader
from PyPoE.poe.file.ot import OTFile
from PyPoE.poe.sim.formula import gem_stat_requirement, GemTypes
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter import config
from PyPoE.cli.exporter.wiki.handler import ExporterHandler, ExporterResult
from PyPoE.cli.exporter.wiki import parser
from PyPoE.cli.exporter.wiki.parsers.skill import SkillParserShared

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


def _simple_conflict_factory(data):
    def _conflict_handler(self, infobox, base_item_type):
        appendix = data.get(base_item_type['Id'])
        if appendix is None:
            return base_item_type['Name']
        else:
            return base_item_type['Name'] + appendix

    return _conflict_handler

# =============================================================================
# Classes
# =============================================================================


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
        #
        # all items
        #
        'name_list',
        'quality',

        # Icons
        'inventory_icon',
        'alternate_art_inventory_icons',

        # Drop restrictions
        'drop_enabled',
        'drop_leagues',
        'drop_areas',
        'drop_text',
        'drop_monsters',
        'upgraded_from_disabled',

        # Item flags
        'is_corrupted',
        'is_relic',
        'can_not_be_traded_or_modified',
        'suppress_improper_modifiers_category',

        # Version information
        'release_version',
        'removal_version',

        # prophecies
        'prophecy_objective',
        'prophecy_reward',
    )
    COPY_MATCH = re.compile(
        r'^(upgraded_from_set|implicit[0-9]+_(?:text|random_list)).*'
        , re.UNICODE)

    NAME = 'Base item'
    INDENT = 40
    ADD_INCLUDE = False


class ItemWikiCondition(WikiCondition):
    NAME = 'Base item'


class MapItemWikiCondition(WikiCondition):
    NAME = 'Base item'


class UniqueMapItemWikiCondition(MapItemWikiCondition):
    NAME = 'Item'
    COPY_MATCH = re.compile(
        r'^(upgraded_from_set|(ex|im)plicit[0-9]+_(?:text|random_list)).*'
        , re.UNICODE)


class ProphecyWikiCondition(WikiCondition):
    NAME = 'Item'


class ItemsHandler(ExporterHandler):
    def __init__(self, sub_parser, *args, **kwargs):
        super().__init__(self, sub_parser, *args, **kwargs)
        self.parser = sub_parser.add_parser('items', help='Items Exporter')
        self.parser.set_defaults(func=lambda args: self.parser.print_help())
        core_sub = self.parser.add_subparsers()

        #
        # Generic base item export
        #
        item_parser = core_sub.add_parser('item', help='Regular item export')
        item_parser.set_defaults(func=lambda args: parser.print_help())
        sub = item_parser.add_subparsers()

        self.add_default_subparser_filters(sub, cls=ItemsParser, type='item')

        item_filter_parser = sub.add_parser(
            'by_filter',
            help='Extracts all items matching various filters',
        )

        self.add_default_parsers(
            parser=item_filter_parser,
            cls=ItemsParser,
            func=ItemsParser.by_filter,
            type='item',
        )
        item_filter_parser.add_argument(
            '-ft-n', '--filter-name',
            help='Filter by item name using regular expression.',
            dest='re_name',
        )

        item_filter_parser.add_argument(
            '-ft-id', '--filter-id', '--filter-metadata-id',
            help='Filter by item metadata id using regular expression',
            dest='re_id',
        )

        #
        # Prophecies
        #
        parser = core_sub.add_parser('prophecy', help='Prophecy export')
        parser.set_defaults(func=lambda args: parser.print_help())
        sub = parser.add_subparsers()
        self.add_default_subparser_filters(sub, cls=ProphecyParser,
                                           type='prophecy')

        #
        # Betrayal and later map series
        #
        parser = core_sub.add_parser(
            'maps', help='Map export (Betrayal and later)')
        parser.set_defaults(func=lambda args: parser.print_help())

        self.add_default_parsers(
            parser=parser,
            cls=ItemsParser,
            func=ItemsParser.export_map,
        )
        self.add_image_arguments(parser)
        self.add_map_series_parsers(parser)

        parser.add_argument(
            'name',
            help='Visible name (i.e. the name you see in game). Can be '
                 'specified multiple times.',
            nargs='*',
        )

        #
        # Atlas nodes
        #

        parser = core_sub.add_parser(
            'atlas_icons', help='Atlas icons export')
        parser.set_defaults(func=lambda args: parser.print_help())

        self.add_default_parsers(
            parser=parser,
            cls=ItemsParser,
            func=ItemsParser.export_map_icons,
        )
        self.add_image_arguments(parser)
        self.add_map_series_parsers(parser)

    def add_map_series_parsers(self, parser):
        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument(
            '-ms', '--map-series', '--filter-map-series',
            help='Filter by map series name (localized)',
            dest='map_series',
        )

        group.add_argument(
            '-msid', '--map-series-id', '--filter-map-series-id',
            help='Filter by internal map series id',
            dest='map_series_id',
        )

    def add_default_parsers(self, *args, type=None, **kwargs):
        super().add_default_parsers(*args, **kwargs)
        parser = kwargs['parser']
        self.add_format_argument(parser)
        parser.add_argument(
            '--disable-english-file-links',
            help='Disables putting english file links in inventory icon for non'
                 ' English languages',
            action='store_false',
            dest='english_file_link',
            default=True,
        )

        if type == 'item':
            parser.add_argument(
                '-ft-c', '--filter-class',
                help='Filter by item class(es). Case sensitive.',
                nargs='*',
                dest='item_class',
            )

            parser.add_argument(
                '-ft-cid', '--filter-class-id',
                help='Filter by item class id(s). Case sensitive.',
                nargs='*',
                dest='item_class_id',
            )

            self.add_image_arguments(parser)
        elif type == 'prophecy':
            parser.add_argument(
                '--allow-disabled',
                help='Allows disabled prophecies to be exported',
                action='store_true',
                dest='allow_disabled',
                default=False,
            )


class ProphecyParser(parser.BaseParser):
    _files = [
        'Prophecies.dat',
    ]

    _LANG = {
        'English': {
            'prophecy': ' (prophecy)',
        },
        'Russian': {
            'prophecy': ' (пророчество)',
        },
        'German': {
            'prophecy': ' (Prophezeiung)',
        },
    }

    _conflict_resolver_prophecy_map = {
        'English': {
            'MapExtraHaku': ' (Haku)',
            'MapExtraTora': ' (Tora)',
            'MapExtraCatarina': ' (Catarina)',
            'MapExtraVagan': ' (Vagan)',
            'MapExtraElreon': ' (Elreon)',
            'MapExtraVorici': ' (Vorici)',
            'MapExtraZana': ' (Zana)',
            'MapExtraEinhar': ' (Einhar)',
            'MapExtraAlva': ' (Alva)',
            'MapExtraNiko': ' (Niko)',
            'MapExtraJun': ' (Jun)',
            # The other one is disabled, should be fine
            'MapSpawnRogueExiles': '',
            'MysteriousInvadersFire': ' (Fire)',
            'MysteriousInvadersCold': ' (Cold)',
            'MysteriousInvadersLightning': ' (Lightning)',
            'MysteriousInvadersPhysical': ' (Physical)',
            'MysteriousInvadersChaos': ' (Chaos)',

            'AreaAllRaresAreCloned': ' (prophecy)',
            'HillockDropsTheAnvil': ' (prophecy)',
        },
        'Russian': {
            'MapExtraHaku': ' (Хаку)',
            'MapExtraTora': ' (Тора)',
            'MapExtraCatarina': ' (Катарина)',
            'MapExtraVagan': ' (Ваган)',
            'MapExtraElreon': ' (Элреон)',
            'MapExtraVorici': ' (Воричи)',
            'MapExtraZana': ' (Зана)',
            'MapExtraEinhar': ' (Эйнар)',
            'MapExtraAlva': ' (Альва)',
            'MapExtraNiko': ' (Нико)',
            'MapExtraJun': ' (Джун)',
            # The other one is disabled, should be fine
            'MapSpawnRogueExiles': '',
            'MysteriousInvadersFire': ' (огонь)',
            'MysteriousInvadersCold': ' (холод)',
            'MysteriousInvadersLightning': ' (молния)',
            'MysteriousInvadersPhysical': ' (физический)',
            'MysteriousInvadersChaos': ' (хаос)',

            'AreaAllRaresAreCloned': ' (пророчество)',
            'HillockDropsTheAnvil': ' (пророчество)',
        },
        'German': {
            'MapExtraHaku': ' (Haku)',
            'MapExtraTora': ' (Tora)',
            'MapExtraCatarina': ' (Catarina)',
            'MapExtraVagan': ' (Vagan)',
            'MapExtraElreon': ' (Elreon)',
            'MapExtraVorici': ' (Vorici)',
            'MapExtraZana': ' (Zana)',
            'MapExtraEinhar': ' (Einhar)',
            'MapExtraAlva': ' (Alva)',
            'MapExtraNiko': ' (Niko)',
            'MapExtraJun': ' (Jun)',
            # The other one is disabled, should be fine
            'MapSpawnRogueExiles': '',
            'MysteriousInvadersFire': ' (Feuer)',
            'MysteriousInvadersCold': ' (Kälte)',
            'MysteriousInvadersLightning': ' (Blitz)',
            'MysteriousInvadersPhysical': ' (Physisch)',
            'MysteriousInvadersChaos': ' (Chaos)',

            'AreaAllRaresAreCloned': ' (Prophezeiung)',
            'HillockDropsTheAnvil': ' (Prophezeiung)',
        },
    }

    _prophecy_column_index_filter = partialmethod(
        parser.BaseParser._column_index_filter,
        dat_file_name='Prophecies.dat',
        error_msg='Several prophecies have not been found:\n%s',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lang = config.get_option('language')

    def by_rowid(self, parsed_args):
        return self.export(
            parsed_args,
            self.rr['Prophecies.dat'][parsed_args.start:parsed_args.end],
        )

    def by_id(self, parsed_args):
        return self.export(parsed_args, self._prophecy_column_index_filter(
            column_id='Id', arg_list=parsed_args.id
        ))

    def by_name(self, parsed_args):
        return self.export(parsed_args, self._prophecy_column_index_filter(
            column_id='Name', arg_list=parsed_args.name
        ))

    def export(self, parsed_args, prophecies):
        final = []
        for prophecy in prophecies:
            if not prophecy['IsEnabled'] and not parsed_args.allow_disabled:
                console(
                    'Prophecy "%s" is disabled - skipping.' % prophecy['Name'],
                    msg=Msg.error
                )
                continue

            final.append(prophecy)

        self.rr['Prophecies.dat'].build_index('Name')

        r = ExporterResult()
        for prophecy in final:
            name = prophecy['Name']

            infobox = OrderedDict()

            infobox['rarity_id'] = 'normal'
            infobox['name'] = name
            infobox['class_id'] = 'StackableCurrency'
            infobox['base_item_id'] = \
                'Metadata/Items/Currency/CurrencyItemisedProphecy'
            infobox['flavour_text'] = prophecy['FlavourText']
            infobox['prophecy_id'] = prophecy['Id']
            infobox['prediction_text'] = prophecy['PredictionText']
            infobox['seal_cost'] = prophecy['SealCost']

            if not prophecy['IsEnabled']:
                infobox['drop_enabled'] = False

            # handle items with duplicate name entries
            if len(self.rr['Prophecies.dat'].index['Name'][name]) > 1:
                extra = self._conflict_resolver_prophecy_map[self.lang].get(
                    prophecy['Id'])
                if extra is None:
                    console('Unresolved ambiguous item name "%s" / id "%s". '
                            'Skipping' % (prophecy['Name'], prophecy['Id']),
                            msg=Msg.error)
                    continue
                name += extra
            cond = ProphecyWikiCondition(
                data=infobox,
                cmdargs=parsed_args,
            )

            r.add_result(
                text=cond,
                out_file='item_%s.txt' % name,
                wiki_page=[
                    {'page': name, 'condition': cond},
                    {
                        'page': name + self._LANG[self.lang]['prophecy'],
                        'condition': cond
                    },
                ],
                wiki_message='Prophecy exporter',
            )

        return r


class ItemsParser(SkillParserShared):
    _regex_format = re.compile(
        r'(?P<index>x|y|z)'
        r'(?:[\W]*)'
        r'(?P<tag>%|second)',
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

    _item_column_index_filter = partialmethod(
        SkillParserShared._column_index_filter,
        dat_file_name='BaseItemTypes.dat',
        error_msg='Several items have not been found:\n%s',
    )

    _MAP_COLORS = {
        'mid tier': '255,210,100',
        'high tier': '240,30,10',
    }

    _MAP_RELEASE_VERSION = {
        'Betrayal': '3.5.0',
        'Synthesis': '3.6.0',
        'Legion': '3.7.0',
        'Blight': '3.8.0',
        'Metamorphosis': '3.9.0',
        'Delirium': '3.10.0',
        'Harvest': '3.11.0',
    }

    _IGNORE_DROP_LEVEL_CLASSES = (
        'HideoutDoodad',
        'Microtransaction',
        'LabyrinthItem',
        'LabyrinthTrinket',
        'LabyrinthMapItem',
    )

    _IGNORE_DROP_LEVEL_ITEMS_BY_ID = {
        # Alchemy Shard
        'Metadata/Items/Currency/CurrencyUpgradeToRareShard',
        # Alteration Shard
        'Metadata/Items/Currency/CurrencyRerollMagicShard',
        'Metadata/Items/Currency/CurrencyLabyrinthEnchant',
        'Metadata/Items/Currency/CurrencyImprint',
        # Transmute Shard
        'Metadata/Items/Currency/CurrencyUpgradeToMagicShard',
        'Metadata/Items/Currency/CurrencyIdentificationShard'
    }

    _DROP_DISABLED_ITEMS_BY_ID = {
        'Metadata/Items/Quivers/Quiver1',
        'Metadata/Items/Quivers/Quiver2',
        'Metadata/Items/Quivers/Quiver3',
        'Metadata/Items/Quivers/Quiver4',
        'Metadata/Items/Quivers/Quiver5',
        'Metadata/Items/Quivers/QuiverDescent',
        'Metadata/Items/Rings/RingVictor1',
        # Eternal Orb
        'Metadata/Items/Currency/CurrencyImprintOrb',
        # Demigod items
        'Metadata/Items/Belts/BeltDemigods1',
        'Metadata/Items/Rings/RingDemigods1',
    }

    _NAME_OVERRIDE_BY_ID = {
        'English': {
            # =================================================================
            # One Hand Axes
            # =================================================================

            'Metadata/Items/Weapons/OneHandWeapons/OneHandAxes/OneHandAxe22':
                '',
            # =================================================================
            # Boots
            # =================================================================

            'Metadata/Items/Armours/Boots/BootsInt4': '',
            # Legion Boots
            'Metadata/Items/Armours/Boots/BootsStrInt7': '',
            'Metadata/Items/Armours/Boots/BootsAtlas1':
                ' (Cold and Lightning Resistance)',
            'Metadata/Items/Armours/Boots/BootsAtlas2':
                ' (Fire and Cold Resistance)',
            'Metadata/Items/Armours/Boots/BootsAtlas3':
                ' (Fire and Lightning Resistance)',
            # =================================================================
            # Gloves
            # =================================================================

            # Legion Gloves
            'Metadata/Items/Armours/Gloves/GlovesStrInt7': '',
            # =================================================================
            # Quivers
            # =================================================================

            'Metadata/Items/Quivers/QuiverDescent': ' (Descent)',
            # =================================================================
            # Rings
            # =================================================================

            'Metadata/Items/Rings/Ring12': " (ruby and topaz)",
            'Metadata/Items/Rings/Ring13': " (sapphire and topaz)",
            'Metadata/Items/Rings/Ring14': " (ruby and sapphire)",
            # =================================================================
            # Amulets
            # =================================================================
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
            # =================================================================
            # Hideout Doodads
            # =================================================================

            'Metadata/Items/Hideout/HideoutLightningCoil': " (hideout doodad)",
            # =================================================================
            # Piece
            # =================================================================

            'Metadata/Items/UniqueFragments/FragmentUniqueShield1_1':
                ' (1 of 4)',
            'Metadata/Items/UniqueFragments/FragmentUniqueShield1_2':
                ' (2 of 4)',
            'Metadata/Items/UniqueFragments/FragmentUniqueShield1_3':
                ' (3 of 4)',
            'Metadata/Items/UniqueFragments/FragmentUniqueShield1_4':
                ' (4 of 4)',
            'Metadata/Items/UniqueFragments/FragmentUniqueSword1_1':
                ' (1 of 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueSword1_2':
                ' (2 of 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueSword1_3':
                ' (3 of 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueStaff1_1':
                ' (1 of 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueStaff1_2':
                ' (2 of 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueStaff1_3':
                ' (3 of 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueBelt1_1':
                ' (1 of 2)',
            'Metadata/Items/UniqueFragments/FragmentUniqueBelt1_2':
                ' (2 of 2)',
            'Metadata/Items/UniqueFragments/FragmentUniqueQuiver1_1':
                ' (1 of 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueQuiver1_2':
                ' (2 of 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueQuiver1_3':
                ' (3 of 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueHelmet1_1':
                ' (1 of 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueHelmet1_2':
                ' (2 of 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueHelmet1_3':
                ' (3 of 3)',
            # =================================================================
            # MTX
            # =================================================================
            'Metadata/Items/MicrotransactionCurrency/MysteryBox1x1':
                ' (1x1)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox1x2':
                ' (1x2)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox1x3':
                ' (1x3)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox1x4':
                ' (1x4)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox2x1':
                ' (2x1)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox2x2':
                ' (2x2)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox2x3':
                ' (2x3)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox2x4':
                ' (2x4)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox3x2':
                ' (3x2)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox3x3':
                ' (3x3)',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'IronMaiden': '',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'InfernalAxe': ' (Weapon Skin)',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'ColossusSword': '',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'LegionBoots': ' (microtransaction)',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'LegionGloves': ' (microtransaction)',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'ScholarBoots': ' (microtransaction)',
            'Metadata/Items/Pets/DemonLion': ' (Pet)',
            # =================================================================
            # Quest items
            # =================================================================
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
        },
        'Russian': {
            # =================================================================
            # Active Skill Gems
            # =================================================================

            'Metadata/Items/Gems/SkillGemPortal':
                ' (камень умения)',
            # =================================================================
            # One Hand Axes
            # =================================================================

            'Metadata/Items/Weapons/OneHandWeapons/OneHandAxes/OneHandAxe22':
                '',
            # =================================================================
            # Boots
            # =================================================================

            'Metadata/Items/Armours/Boots/BootsInt4': '',
            # Legion Boots
            'Metadata/Items/Armours/Boots/BootsStrInt7': '',
            'Metadata/Items/Armours/Boots/BootsAtlas1':
                ' (сопротивление холоду и молнии)',
            'Metadata/Items/Armours/Boots/BootsAtlas2':
                ' (сопротивление огню и холоду)',
            'Metadata/Items/Armours/Boots/BootsAtlas3':
                ' (сопротивление огню и молнии)',
            # =================================================================
            # Gloves
            # =================================================================

            # Legion Gloves
            'Metadata/Items/Armours/Gloves/GlovesStrInt7': '',
            # =================================================================
            # Quivers
            # =================================================================

            'Metadata/Items/Quivers/QuiverDescent': ' (Спуск)',
            # =================================================================
            # Rings
            # =================================================================
            'Metadata/Items/Rings/Ring12':
                " (рубин и топаз)",
            'Metadata/Items/Rings/Ring13':
                " (сапфир и топаз)",
            'Metadata/Items/Rings/Ring14':
                " (рубин и сапфир)",
            # =================================================================
            # Amulets
            # =================================================================
            'Metadata/Items/Amulets/Talismans/Talisman2_6_1':
                ' (получаемый урон от огня становится уроном от холода)',
            'Metadata/Items/Amulets/Talismans/Talisman2_6_2':
                ' (получаемый урон от огня становится уроном от молнии)',
            'Metadata/Items/Amulets/Talismans/Talisman2_6_3':
                ' (получаемый урон от холода становится уроном от огня)',
            'Metadata/Items/Amulets/Talismans/Talisman2_6_4':
                ' (получаемый урон от холода становится уроном от молнии)',
            'Metadata/Items/Amulets/Talismans/Talisman2_6_5':
                ' (получаемый урон от молнии становится уроном от холода)',
            'Metadata/Items/Amulets/Talismans/Talisman2_6_6':
                ' (получаемый урон от молнии становится уроном от огня)',
            'Metadata/Items/Amulets/Talismans/Talisman3_6_1':
                ' (заряд энергии при убийстве)',
            'Metadata/Items/Amulets/Talismans/Talisman3_6_2':
                ' (заряд ярости при убийстве)',
            'Metadata/Items/Amulets/Talismans/Talisman3_6_3':
                ' (заряд выносливости при убийстве)',
            # =================================================================
            # Hideout Doodads
            # =================================================================

            'Metadata/Items/Hideout/HideoutMalachaiHeart':
                ' (предмет убежища)',
            'Metadata/Items/Hideout/HideoutVaalWhispySmoke':
                ' (предмет убежища)',
            'Metadata/Items/Hideout/HideoutChestVaal':
                ' (предмет убежища)',
            'Metadata/Items/Hideout/HideoutEncampmentFireplace':
                ' (предмет убежища)',
            'Metadata/Items/Hideout/HideoutEncampmentLetters':
                ' (предмет убежища)',
            'Metadata/Items/Hideout/HideoutIncaPyramid':
                ' (предмет убежища)',
            'Metadata/Items/Hideout/HideoutDarkSoulercoaster':
                ' (предмет убежища)',
            'Metadata/Items/Hideout/HideoutVaalMechanism':
                ' (предмет убежища)',
            'Metadata/Items/Hideout/HideoutCharredSkeleton':
                ' (предмет убежища)',
            'Metadata/Items/HideoutInteractables/DexIntCraftingBench':
                ' (предмет убежища)',
            # =================================================================
            # Piece
            # =================================================================

            'Metadata/Items/UniqueFragments/FragmentUniqueShield1_1':
                ' (1 из 4)',
            'Metadata/Items/UniqueFragments/FragmentUniqueShield1_2':
                ' (2 из 4)',
            'Metadata/Items/UniqueFragments/FragmentUniqueShield1_3':
                ' (3 из 4)',
            'Metadata/Items/UniqueFragments/FragmentUniqueShield1_4':
                ' (4 из 4)',
            'Metadata/Items/UniqueFragments/FragmentUniqueSword1_1':
                ' (1 из 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueSword1_2':
                ' (2 из 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueSword1_3':
                ' (3 из 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueStaff1_1':
                ' (1 из 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueStaff1_2':
                ' (2 из 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueStaff1_3':
                ' (3 из 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueBelt1_1':
                ' (1 из 2)',
            'Metadata/Items/UniqueFragments/FragmentUniqueBelt1_2':
                ' (2 из 2)',
            'Metadata/Items/UniqueFragments/FragmentUniqueQuiver1_1':
                ' (1 из 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueQuiver1_2':
                ' (2 из 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueQuiver1_3':
                ' (3 из 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueHelmet1_1':
                ' (1 из 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueHelmet1_2':
                ' (2 из 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueHelmet1_3':
                ' (3 из 3)',
            # =================================================================
            # MTX
            # =================================================================
            'Metadata/Items/MicrotransactionCurrency/MysteryBox1x1':
                ' (1x1)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox1x2':
                ' (1x2)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox1x3':
                ' (1x3)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox1x4':
                ' (1x4)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox2x1':
                ' (2x1)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox2x2':
                ' (2x2)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox2x3':
                ' (2x3)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox2x4':
                ' (2x4)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox3x2':
                ' (3x2)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox3x3':
                ' (3x3)',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'IronMaiden': '',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'InfernalAxe': ' (внешний вид оружия)',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'ColossusSword': '',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'LegionBoots': ' (микротранзакция)',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'LegionGloves': ' (микротранзакция)',
            'Metadata/Items/MicrotransactionItemEffects/MasterArmour1Boots':
                ' (микротранзакция)',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'SinFootprintsEffect': ' (микротранзакция)',
            'Metadata/Items/Pets/DemonLion': ' (питомец)',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'HeartWeapon2014': ' (2014)',
            # =================================================================
            # Quest items
            # =================================================================
            'Metadata/Items/QuestItems/GoldenPages/Page1':
                ' (1 из 4)',
            'Metadata/Items/QuestItems/GoldenPages/Page2':
                ' (2 из 4)',
            'Metadata/Items/QuestItems/GoldenPages/Page3':
                ' (3 из 4)',
            'Metadata/Items/QuestItems/GoldenPages/Page4':
                ' (4 из 4)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier8_1':
                ' (1 из 2)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier8_2':
                ' (2 из 2)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier9_1':
                ' (1 из 3)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier9_2':
                ' (2 из 3)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier9_3':
                ' (3 из 3)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier10_1':
                ' (1 из 3)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier10_2':
                ' (2 из 3)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier10_3':
                ' (3 из 3)',
            'Metadata/Items/QuestItems/RibbonSpool':
                ' (предмет)',
            'Metadata/Items/QuestItems/Act7/SilverLocket':
                ' (предмет)',
            'Metadata/Items/QuestItems/Act7/KisharaStar':
                ' (предмет)',
            'Metadata/Items/QuestItems/Act8/WingsOfVastiri':
                ' (предмет)',
            'Metadata/Items/QuestItems/Act9/StormSword':
                ' (предмет)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade1_1':
                ' (1 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade1_2':
                ' (2 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade1_3':
                ' (3 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade1_4':
                ' (4 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade1_5':
                ' (5 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade1_6':
                ' (6 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade1_7':
                ' (7 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade1_8':
                ' (8 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade2_1':
                ' (1 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade2_2':
                ' (2 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade2_3':
                ' (3 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade2_4':
                ' (4 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade2_5':
                ' (5 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade2_6':
                ' (6 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade2_7':
                ' (7 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade2_8':
                ' (8 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade3_1':
                ' (1 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade3_2':
                ' (2 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade3_3':
                ' (3 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade3_4':
                ' (4 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade3_5':
                ' (5 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade3_6':
                ' (6 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade3_7':
                ' (7 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade3_8':
                ' (8 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade4_1':
                ' (1 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade4_2':
                ' (2 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade4_3':
                ' (3 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade4_4':
                ' (4 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade4_5':
                ' (5 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade4_6':
                ' (6 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade4_7':
                ' (7 из 8)',
            'Metadata/Items/AtlasUpgrades/AtlasRegionUpgrade4_8':
                ' (8 из 8)',
        },
        'German': {
            # =================================================================
            # One Hand Axes
            # =================================================================

            'Metadata/Items/Weapons/OneHandWeapons/OneHandAxes/OneHandAxe22':
                '',
            # =================================================================
            # Boots
            # =================================================================

            'Metadata/Items/Armours/Boots/BootsInt4': '',
            # Legion Boots
            'Metadata/Items/Armours/Boots/BootsStrInt7': '',
            'Metadata/Items/Armours/Boots/BootsAtlas1':
                ' (Kälte und Blitz Resistenzen)',
            'Metadata/Items/Armours/Boots/BootsAtlas2':
                ' (Feuer und Kälte Resistenzen)',
            'Metadata/Items/Armours/Boots/BootsAtlas3':
                ' (Feuer und Blitz Resistenzen)',
            # =================================================================
            # Gloves
            # =================================================================

            # Legion Gloves
            'Metadata/Items/Armours/Gloves/GlovesStrInt7': '',
            # =================================================================
            # Quivers
            # =================================================================

            'Metadata/Items/Quivers/QuiverDescent': ' (Descent)',
            # =================================================================
            # Rings
            # =================================================================

            'Metadata/Items/Rings/Ring12': " (Rubin und Topas)",
            'Metadata/Items/Rings/Ring13': " (Saphir und Topas)",
            'Metadata/Items/Rings/Ring14': " (Rubin und Saphir)",
            # =================================================================
            # Amulets
            # =================================================================
            'Metadata/Items/Amulets/Talismans/Talisman2_6_1':
                ' (Feuerschaden erlitten als Kälteschaden)',
            'Metadata/Items/Amulets/Talismans/Talisman2_6_2':
                ' (Feuerschaden erlitten als Blitzschaden)',
            'Metadata/Items/Amulets/Talismans/Talisman2_6_3':
                ' (Kälteschaden erlitten als Feuerschaden)',
            'Metadata/Items/Amulets/Talismans/Talisman2_6_4':
                ' (Kälteschaden erlitten als Blitzschaden)',
            'Metadata/Items/Amulets/Talismans/Talisman2_6_5':
                ' (Blitzschaden erlitten als Kälteschaden)',
            'Metadata/Items/Amulets/Talismans/Talisman2_6_6':
                ' (Blitzschaden erlitten als Feuerschaden)',
            'Metadata/Items/Amulets/Talismans/Talisman3_6_1':
                ' (Energie-Ladung bei Tötung)',
            'Metadata/Items/Amulets/Talismans/Talisman3_6_2':
                ' (Raserei-Ladung bei Tötung)',
            'Metadata/Items/Amulets/Talismans/Talisman3_6_3':
                ' (Widerstands-Ladung bei Tötung)',
            # =================================================================
            # Hideout Doodads
            # =================================================================

            'Metadata/Items/Hideout/HideoutLightningCoil':
                " (Dinge fürs Versteck)",
            # =================================================================
            # Piece
            # =================================================================

            'Metadata/Items/UniqueFragments/FragmentUniqueShield1_1':
                ' (1 von 4)',
            'Metadata/Items/UniqueFragments/FragmentUniqueShield1_2':
                ' (2 von 4)',
            'Metadata/Items/UniqueFragments/FragmentUniqueShield1_3':
                ' (3 von 4)',
            'Metadata/Items/UniqueFragments/FragmentUniqueShield1_4':
                ' (4 von 4)',
            'Metadata/Items/UniqueFragments/FragmentUniqueSword1_1':
                ' (1 von 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueSword1_2':
                ' (2 von 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueSword1_3':
                ' (3 von 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueStaff1_1':
                ' (1 von 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueStaff1_2':
                ' (2 von 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueStaff1_3':
                ' (3 von 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueBelt1_1':
                ' (1 von 2)',
            'Metadata/Items/UniqueFragments/FragmentUniqueBelt1_2':
                ' (2 von 2)',
            'Metadata/Items/UniqueFragments/FragmentUniqueQuiver1_1':
                ' (1 von 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueQuiver1_2':
                ' (2 von 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueQuiver1_3':
                ' (3 von 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueHelmet1_1':
                ' (1 von 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueHelmet1_2':
                ' (2 von 3)',
            'Metadata/Items/UniqueFragments/FragmentUniqueHelmet1_3':
                ' (3 von 3)',
            # =================================================================
            # MTX
            # =================================================================
            'Metadata/Items/MicrotransactionCurrency/MysteryBox1x1':
                ' (1x1)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox1x2':
                ' (1x2)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox1x3':
                ' (1x3)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox1x4':
                ' (1x4)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox2x1':
                ' (2x1)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox2x2':
                ' (2x2)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox2x3':
                ' (2x3)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox2x4':
                ' (2x4)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox3x2':
                ' (3x2)',
            'Metadata/Items/MicrotransactionCurrency/MysteryBox3x3':
                ' (3x3)',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'IronMaiden': '',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'InfernalAxe': ' (Weapon Skin)',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'ColossusSword': '',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'LegionBoots': ' (Mikrotransaktion)',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'LegionGloves': ' (Mikrotransaktion)',
            'Metadata/Items/MicrotransactionItemEffects/Microtransaction'
            'ScholarBoots': ' (Mikrotransaktion)',
            'Metadata/Items/Pets/DemonLion': ' (Haustier)',
            # =================================================================
            # Quest items
            # =================================================================
            'Metadata/Items/QuestItems/GoldenPages/Page1':
                ' (1 von 4)',
            'Metadata/Items/QuestItems/GoldenPages/Page2':
                ' (2 von 4)',
            'Metadata/Items/QuestItems/GoldenPages/Page3':
                ' (3 von 4)',
            'Metadata/Items/QuestItems/GoldenPages/Page4':
                ' (4 von 4)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier8_1':
                ' (1 von 2)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier8_2':
                ' (2 von 2)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier9_1':
                ' (1 von 3)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier9_2':
                ' (2 von 3)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier9_3':
                ' (3 von 3)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier10_1':
                ' (1 von 3)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier10_2':
                ' (2 von 3)',
            'Metadata/Items/QuestItems/MapUpgrades/MapUpgradeTier10_3':
                ' (3 von 3)',

            # =================================================================
            # =================================================================
            # ==================== Germany only conflicts =====================
            # =================================================================
            # =================================================================
            # Schleifstein
            'Metadata/Items/Currency/CurrencyWeaponQuality': '',
            'Metadata/Items/HideoutInteractables/StrDexCraftingBench':
                ' (Dinge fürs Versteck)',
        },
    }

    _LANG = {
        'English': {
            'Low': 'Low Tier',
            'Mid': 'Mid Tier',
            'High': 'High Tier',
            'Uber': 'Max Tier',
            'decoration': '%s (%s %s decoration)',
            'decoration_wounded': '%s (%s %s decoration, Wounded)',
            'of': '%s of %s',
            'descent': 'Descent',
        },
        'German': {
            'Low': 'Niedrige Stufe',
            'Mid': 'Mittlere Stufe',
            'High': 'Hohe Stufe',
            'Uber': 'Maximale Stufe',
            'decoration': '%s (%s %s Dekoration)',
            'decoration_wounded': '%s (%s %s Dekoration, verletzt)',
            'of': '%s von %s',
            'descent': 'Descent',
        },
        'Russian': {
            'Low': 'низкий уровень',
            'Mid': 'средний уровень',
            'High': 'высокий уровень',
            'Uber': 'максимальный уровень',
            'decoration': '%s (%s %s предмет убежища)',
            'decoration_wounded': '%s (%s %s предмет убежища, Раненый)',
            'of': '%s из %s',
            'descent': 'Спуск',
        },
    }

    # Unreleased or disabled items to avoid exporting to the wiki
    _SKIP_ITEMS_BY_ID = {
        #
        # Active Skill Gems
        #
        'Metadata/Items/Gems/SkillGemBackstab',
        'Metadata/Items/Gems/SkillGemBladeTrap',
        'Metadata/Items/Gems/SkillGemBlitz',
        'Metadata/Items/Gems/SkillGemBloodWhirl',
        'Metadata/Items/Gems/SkillGemBoneArmour',
        'Metadata/Items/Gems/SkillGemCaptureMonster',
        'Metadata/Items/Gems/SkillGemCoilingAssault',
        'Metadata/Items/Gems/SkillGemComboStrike',
        'Metadata/Items/Gems/SkillGemDamageInfusion',
        'Metadata/Items/Gems/SkillGemDiscorectangleSlam',
        'Metadata/Items/Gems/SkillGemElementalProjectiles',
        'Metadata/Items/Gems/SkillGemFireWeapon',
        'Metadata/Items/Gems/SkillGemHeraldOfBlood',
        'Metadata/Items/Gems/SkillGemIceFire',
        'Metadata/Items/Gems/SkillGemIcefire',
        'Metadata/Items/Gems/SkillGemIgnite',
        'Metadata/Items/Gems/SkillGemInfernalSwarm',
        'Metadata/Items/Gems/SkillGemInfernalSweep',
        'Metadata/Items/Gems/SkillGemLightningChannel',
        'Metadata/Items/Gems/SkillGemLightningCircle',
        'Metadata/Items/Gems/SkillGemLightningTendrilsChannelled',
        'Metadata/Items/Gems/SkillGemNewBladeVortex',
        'Metadata/Items/Gems/SkillGemNewPunishment',
        'Metadata/Items/Gems/SkillGemNewShockNova',
        'Metadata/Items/Gems/SkillGemProjectilePortal',
        'Metadata/Items/Gems/SkillGemQuickBlock',
        'Metadata/Items/Gems/SkillGemRendingSteel',
        'Metadata/Items/Gems/SkillGemReplicate',
        'Metadata/Items/Gems/SkillGemRighteousLightning',
        'Metadata/Items/Gems/SkillGemRiptide',
        'Metadata/Items/Gems/SkillGemSerpentStrike',
        'Metadata/Items/Gems/SkillGemShadowBlades',
        'Metadata/Items/Gems/SkillGemSlashTotem',
        'Metadata/Items/Gems/SkillGemSliceAndDice',
        'Metadata/Items/Gems/SkillGemSnipe',
        'Metadata/Items/Gems/SkillGemSpectralSpinningWeapon',
        'Metadata/Items/Gems/SkillGemStaticTether',
        'Metadata/Items/Gems/SkillGemSummonSkeletonsChannelled',
        'Metadata/Items/Gems/SkillGemTouchOfGod',
        'Metadata/Items/Gems/SkillGemVaalFireTrap',
        'Metadata/Items/Gems/SkillGemVaalFleshOffering',
        'Metadata/Items/Gems/SkillGemVaalHeavyStrike',
        'Metadata/Items/Gems/SkillGemVaalSweep',
        'Metadata/Items/Gems/SkillGemVortexMine',
        'Metadata/Items/Gems/SkillGemWandTeleport',
        'Metadata/Items/Gems/SkillGemNewPhaseRun',
        'Metadata/Items/Gems/SkillGemNewArcticArmour',

        #
        # Support Skill Gems
        #
        'Metadata/Items/Gems/SupportGemCastLinkedCursesOnCurse',
        'Metadata/Items/Gems/SupportGemHandcastRapidFire',
        'Metadata/Items/Gems/SupportGemSplit',
        'Metadata/Items/Gems/SupportGemReturn',
        'Metadata/Items/Gems/SupportGemTemporaryForTutorial',
        'Metadata/Items/Gems/SupportGemVaalSoulHarvesting',

        #
        # MTX
        #
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionSpectralThrowEbony',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionFirstBlood',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionFirstBloodWeaponEffect',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionTitanPlate',
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionStatueSummonSkeletons2',
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionStatueSummonSkeletons3',
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionStatueSummonSkeletons4',
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionAlternatePortal',
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionBloodSlam',
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionNewRaiseSpectre',
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionNewRaiseZombie',
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionNewTotem',
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionPlinthWarp',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionWhiteWeapon',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionYellowWeapon',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionHeartWeapon2015',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionPortalSteam1',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionTestCharacterPortrait',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionTestCharacterPortrait2',
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionAuraEffect1',
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionAuraEffect2',
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionAuraEffect3',
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionAuraEffect4',
        'Metadata/Items/MicrotransactionSkillEffects/MicrotransactionBloodRavenSummonRagingSpirit',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionMarkOfThePhoenixPurple',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionWuqiWeaponEffect',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionBlackguardCape',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionDemonhandClaw',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionDivineShield',
        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionEldritchWings',

        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencent1Frame',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencent2Frame',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencent3Frame',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencent4Frame',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencent5Frame',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencent6Frame',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencent7Frame',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge1_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge1_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge1_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge1_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge1_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge1_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge1_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge2_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge2_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge2_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge2_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge2_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge2_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge2_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge3_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge3_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge3_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge3_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge3_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge3_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge3_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge4_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge4_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge4_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge4_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge4_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge4_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge4_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge5_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge5_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge5_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge5_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge5_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge5_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge5_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge6_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge6_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge6_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge6_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge6_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge6_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge6_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge7_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge7_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge7_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge7_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge7_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge7_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge7_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge8_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge8_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge8_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge8_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge8_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge8_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge8_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge9_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge9_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge9_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge9_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge9_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge9_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge9_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge10_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge10_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge10_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge10_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge10_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge10_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentBadge10_7',

        'Metadata/Items/MicrotransactionItemEffects/MicrotransactionTencentInfernalWeapon',
        'Metadata/Items/MicrotransactionCurrency/MicrotransactionTencentExpandInventory0to1',
        'Metadata/Items/MicrotransactionCurrency/MicrotransactionTencentExpandInventory1to2',
        'Metadata/Items/MicrotransactionCurrency/MicrotransactionTencentExpandInventory2to3',
        'Metadata/Items/MicrotransactionCurrency/MicrotransactionTencentExpandInventory3to4',
        'Metadata/Items/MicrotransactionCurrency/MicrotransactionTencentExpandInventory4to5',
        'Metadata/Items/MicrotransactionCurrency/MicrotransactionTencentExpandInventory5to6',

        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame1_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame1_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame1_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame1_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame1_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame1_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame1_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame2_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame2_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame2_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame2_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame2_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame2_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame2_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame3_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame3_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame3_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame3_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame3_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame3_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame3_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame4_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame4_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame4_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame4_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame4_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame4_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame4_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame5_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame5_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame5_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame5_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame5_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame5_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame5_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame6_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame6_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame6_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame6_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame6_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame6_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame6_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame7_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame7_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame7_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame7_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame7_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame7_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame7_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame8_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame8_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame8_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame8_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame8_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame8_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame8_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame9_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame9_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame9_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame9_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame9_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame9_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame9_7',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame10_1',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame10_2',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame10_3',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame10_4',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame10_5',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame10_6',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentGradingFrame10_7',

        'Metadata/Items/MicrotrransactionCharacterEffects/MicrotransactionTencentTopPlayerFrame',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentS3HideOutFrame',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentS3FashionFrame',
        'Metadata/Items/MicrotransactionCharacterEffects/MicrotransactionTencentS3BDMasterFrame',

        'Metadata/Items/MicrotransactionCurrency/TradeMarketTab',
        'Metadata/Items/MicrotransactionCurrency/TradeMarketBuyoutTab',

        #
        # Hideout Doodads
        #

        # Hideout totem test variants, not needed
        'Metadata/Items/Hideout/HideoutTotemPoleTest',
        'Metadata/Items/Hideout/HideoutTotemPole2Test',
        'Metadata/Items/Hideout/HideoutTotemPole3Test',
        'Metadata/Items/Hideout/HideoutTotemPole4Test',
        'Metadata/Items/Hideout/HideoutTotemPole5Test',
        'Metadata/Items/Hideout/HideoutTotemPole6Test',
        'Metadata/Items/Hideout/HideoutTotemPole7Test',
        'Metadata/Items/Hideout/HideoutTotemPole8Test',
        'Metadata/Items/Hideout/HideoutTotemPole9Test',
        'Metadata/Items/Hideout/HideoutTotemPole10Test',
        'Metadata/Items/Hideout/HideoutTotemPole11Test',
        'Metadata/Items/Hideout/HideoutTotemPole12Test',
        'Metadata/Items/Hideout/HideoutTotemPole13Test',
        'Metadata/Items/Hideout/HideoutTotemPole14Test',
        'Metadata/Items/Hideout/HideoutTotemPole15Test',

        #
        # Stackable currency
        #

        # Legacy variants of items before item stash tabs
        'Metadata/Items/Delve/DelveSocketableCurrencyUpgrade1',
        'Metadata/Items/Delve/DelveSocketableCurrencyUpgrade2',
        'Metadata/Items/Delve/DelveSocketableCurrencyUpgrade3',
        'Metadata/Items/Delve/DelveSocketableCurrencyUpgrade4',
        'Metadata/Items/Delve/DelveSocketableCurrencyReroll1',
        'Metadata/Items/Delve/DelveSocketableCurrencyReroll2',
        'Metadata/Items/Delve/DelveSocketableCurrencyReroll3',
        'Metadata/Items/Delve/DelveSocketableCurrencyReroll4',
        'Metadata/Items/MapFragments/VaalFragment1_1',
        'Metadata/Items/MapFragments/VaalFragment1_2',
        'Metadata/Items/MapFragments/VaalFragment1_3',
        'Metadata/Items/MapFragments/VaalFragment1_4',
        'Metadata/Items/MapFragments/VaalFragment2_1',
        'Metadata/Items/MapFragments/VaalFragment2_2',
        'Metadata/Items/MapFragments/VaalFragment2_3',
        'Metadata/Items/MapFragments/VaalFragment2_4',
        'Metadata/Items/MapFragments/ProphecyFragment1',
        'Metadata/Items/MapFragments/ProphecyFragment2',
        'Metadata/Items/MapFragments/ProphecyFragment3',
        'Metadata/Items/MapFragments/ProphecyFragment4',
        'Metadata/Items/MapFragments/ShaperFragment1',
        'Metadata/Items/MapFragments/ShaperFragment2',
        'Metadata/Items/MapFragments/ShaperFragment3',
        'Metadata/Items/MapFragments/ShaperFragment4',
        'Metadata/Items/MapFragments/FragmentPantheonFlask',
        'Metadata/Items/MapFragments/BreachFragmentFire',
        'Metadata/Items/MapFragments/BreachFragmentCold',
        'Metadata/Items/MapFragments/BreachFragmentLightning',
        'Metadata/Items/MapFragments/BreachFragmentPhysical',
        'Metadata/Items/MapFragments/BreachFragmentChaos',
        'Metadata/Items/Labyrinth/OfferingToTheGoddess',
    }

    _attribute_map = OrderedDict((
        ('Str', 'strength'),
        ('Dex', 'dexterity'),
        ('Int', 'intelligence'),
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parsed_args = None
        self._language = config.get_option('language')
        if self._language != 'English':
            self.rr2 = RelationalReader(
                path_or_ggpk=self.base_path,
                files=['BaseItemTypes.dat', 'Prophecies.dat'],
                read_options={
                    'use_dat_value': False,
                    'auto_build_index': True,
                },
                raise_error_on_missing_relation=False,
                language='English',
            )
        else:
            self.rr2 = None

    def _skill_gem(self, infobox, base_item_type):
        try:
            skill_gem = self.rr['SkillGems.dat'].index['BaseItemTypesKey'][
                base_item_type.rowid]
        except KeyError:
            return False

        # SkillGems.dat
        for attr_short, attr_long in self._attribute_map.items():
            if not skill_gem[attr_short]:
                continue
            infobox[attr_long + '_percent'] = skill_gem[attr_short]

        infobox['gem_tags'] = ', '.join(
            [gt['Tag'] for gt in skill_gem['GemTagsKeys'] if gt['Tag']]
        )

        # No longer used
        #

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
            console('No experience progression found for "%s" - assuming max '
                    'level 1' %
                    base_item_type['Name'], msg=Msg.error)
            exp_total = [0]

        max_level = len(exp_total)-1
        ge = skill_gem['GrantedEffectsKey']

        primary = OrderedDict()
        self._skill(ge=ge, infobox=primary, parsed_args=self._parsed_args,
                    msg_name=base_item_type['Name'], max_level=max_level)

        # Some skills have a secondary skill effect.
        #
        # Currently there is no great way of handling this in the wiki, so the
        # secondary effects are just added. Skills that have their own entry
        # are excluded so we don't get vaal skill gems here.
        second = False
        if skill_gem['GrantedEffectsKey2']:
            index = None
            try:
                index = self.rr['SkillGems.dat'].index['GrantedEffectsKey']
            except KeyError:
                self.rr['SkillGems.dat'].build_index('GrantedEffectsKey')
                index = self.rr['SkillGems.dat'].index['GrantedEffectsKey']

            if not index[skill_gem['GrantedEffectsKey2']]:
                # If there is no skill granting this it's probably fine to
                # include.
                second = True

        if second:
            secondary = OrderedDict()
            self._skill(
                ge=skill_gem['GrantedEffectsKey2'],
                infobox=secondary,
                parsed_args=self._parsed_args,
                msg_name=base_item_type['Name'],
                max_level=max_level
            )

            for k, v in list(primary.items()) + list(secondary.items()):
                # Just override the stuff if needs be.
                if 'stat' not in k:
                    infobox[k] = v

            for k in ('stat_text', 'quality_stat_text'):
                infobox[k] = '<br>'.join(
                    [x for x in (primary[k], secondary[k]) if x]
                )

            # Stat merging...
            def get_stat(i, prefix, data):
                return (data['%s_stat%s_id' % (prefix, i)],
                        data['%s_stat%s_value' % (prefix, i)])

            def set_stat(i, prefix, sid, sv):
                infobox['%s_stat%s_id' % (prefix, i)] = sid
                infobox['%s_stat%s_value' % (prefix, i)] = sv

            def cp_stats(prefix):
                i = 1
                while True:
                    try:
                        sid, sv = get_stat(i, prefix, primary)
                    except KeyError:
                        break
                    set_stat(i, prefix, sid, sv)
                    i += 1

                j = 1
                while True:
                    try:
                        sid, sv = get_stat(j, prefix, secondary)
                    except KeyError:
                        break
                    set_stat(j + i - 1, prefix, sid, sv)
                    j += 1

            cp_stats('static')
            lv = 1
            while True:
                prefix = 'level%s' % lv
                try:
                    primary[prefix]
                except KeyError:
                    break

                for k in ('_stat_text', ):
                    k = prefix + k
                    infobox[k] = '<br>'.join(
                        [x[k] for x in (primary, secondary) if k in x]
                    )
                cp_stats(prefix)

                lv += 1
        else:
            for k, v in primary.items():
                infobox[k] = v

        # some descriptions come from active skills which are parsed in above
        # function
        if 'gem_description' not in infobox:
            infobox['gem_description'] = skill_gem['Description'].replace(
                '\n', '<br>')

        #
        # Output handling for progression
        #

        # Body
        map2 = {
            'Str': 'strength_requirement',
            'Int': 'intelligence_requirement',
            'Dex': 'dexterity_requirement',
        }

        if base_item_type['ItemClassesKey']['Id'] == 'Active Skill Gem':
            gtype = GemTypes.active
        elif base_item_type['ItemClassesKey']['Id'] == 'Support Skill Gem':
            gtype = GemTypes.support

        # +1 for gem levels starting at 1
        # +1 for being able to corrupt gems to +1 level
        # +1 for python counting only up to, but not including the number
        for i in range(1, max_level+3):
            prefix = 'level%s_' % i
            for attr in ('Str', 'Dex', 'Int'):
                if skill_gem[attr]:
                    try:
                        infobox[prefix + map2[attr]] = gem_stat_requirement(
                            level=infobox[prefix + 'level_requirement'],
                            gtype=gtype,
                            multi=skill_gem[attr],
                        )
                    except ValueError as e:
                        warnings.warn(str(e))
                    except KeyError:
                        print(base_item_type['Id'], base_item_type['Name'])
                        raise
            try:
                # Index starts at 0 while levels start at 1
                infobox[prefix + 'experience'] = exp_total[i-1]
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

    def _type_amulet(self, infobox, base_item_type):
        match = re.search('Talisman([0-9])', base_item_type['Id'])
        if match:
            infobox['is_talisman'] = True
            infobox['talisman_tier'] = match.group(1)

        return True

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
            ('IncreasedMovementSpeed', {
                'template': 'movement_speed',
                'condition': lambda v: v != 0,
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
                stats, flasks['BuffStatValues'], full_result=True,
                lang=self._language,
            )
            infobox['buff_stat_text'] = '<br>'.join([
                parser.make_inter_wiki_links(line) for line in tr.lines
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
                'template': 'physical_damage_min',
            }),
            ('DamageMax', {
                'template': 'physical_damage_max',
            }),
            ('RangeMax', {
                'template': 'weapon_range',
            }),
        ),
        row_index=True,
    )

    def _currency_extra(self, infobox, base_item_type, currency):
        # Add the "shift click to unstack" stuff to currency-ish items
        if currency['Stacks'] > 1 and infobox['class_id'] not in \
                ('Microtransaction', ):
            if 'help_text' in infobox:
                infobox['help_text'] += '<br>'
            else:
                infobox['help_text'] = ''

            infobox['help_text'] += self.rr['ClientStrings.dat'].index[
                'Id']['ItemDisplayStackDescription']['Text']

        if infobox.get('description'):
            infobox['description'] = parser.parse_and_handle_description_tags(
                rr=self.rr,
                text=infobox['description'],
            )

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
        ('HideoutNPCsKey', {
            'template': 'master',
            'format': lambda v: v['Hideout_NPCsKey']['Name'],
            'condition': lambda v: v is not None,
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
            ('HideoutNPCsKey', {
                'template': 'master',
                'format': lambda v: v['Hideout_NPCsKey']['Name'],
                'condition': lambda v: v,
            }),
            ('FavourCost', {
                'template': 'master_favour_cost',
                #'condition': lambda v: v,
            }),
            ('MasterLevel', {
                'template': 'master_level_requirement',
                #'condition': lambda v: v,
            }),
            ('Variation_AOFiles', {
                'template': 'variation_count',
                'format': lambda v: len(v),
            }),
        ),
        row_index=True,
        function=_apply_master_map,
    )

    def _maps_extra(self, infobox, base_item_type, maps):
        if maps['Shaped_AreaLevel'] > 0:
            infobox['map_area_level'] = maps['Shaped_AreaLevel']
        else:
            infobox['map_area_level'] = maps['Regular_WorldAreasKey'][
                'AreaLevel']

        '''# Regular items are handled in the main function
        if maps['Tier'] < 17:
            self._process_purchase_costs(
                self.rr['MapPurchaseCosts.dat'].index['Tier'][maps['Tier']],
                infobox
            )'''

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
                'format': lambda v: v['AreaLevel'],
                'condition': lambda v: v is not None,
            }),
            ('MapSeriesKey', {
                'template': 'map_series',
                'format': lambda v: v['Name'],
            })
        ),
        row_index=True,
        function=_maps_extra,
    )

    def _map_fragment_extra(self, infobox, base_item_type, map_fragment_mods):
        if map_fragment_mods['ModsKeys']:
            i = 1
            while infobox.get('implicit%s' % i) is not None:
                i += 1
            for mod in map_fragment_mods['ModsKeys']:
                infobox['implicit%s' % i] = mod['Id']
                i += 1

    _type_map_fragment_mods = _type_factory(
        data_file='MapFragmentMods.dat',
        data_mapping={},
        row_index=True,
        function=_map_fragment_extra,
        fail_condition=True,
    )

    def _essence_extra(self, infobox, base_item_type, essence):
        infobox['is_essence'] = True

        #
        # Essence description
        #
        get_str = lambda k: self.rr['ClientStrings.dat'].index['Id'][
            'EssenceCategory%s' % k]['Text']

        essence_categories = OrderedDict((
            (None,
                ('OneHandWeapon', 'TwoHandWeapon'),
            ),
            ('MeleeWeapon',
                (),
            ),
            ('RangedWeapon',
                ('Wand', 'Bow'),
            ),
            ('Weapon',
                ('TwoHandMeleeWeapon', ),
            ),
            ('Armour',
                ('Gloves', 'Boots', 'BodyArmour', 'Helmet', 'Shield')
            ),
            ('Quiver',
                ()
            ),
            ('Jewellery',
                ('Amulet', 'Ring', 'Belt')
            ),
        ))

        out = []

        if essence['ItemLevelRestriction'] != 0:
            out.append(
                self.rr['ClientStrings.dat'].index['Id'][
                    'EssenceModLevelRestriction']['Text'].replace(
                    '%1%', str(essence['ItemLevelRestriction']))
            )
            out[-1] += '<br />'

        def add_line(text, mod):
            nonlocal out
            out.append('%s: %s' % (
                text, ''.join(self._get_stats(mod=mod))
            ))

        item_mod = essence['Display_Items_ModsKey']

        for category, rows in essence_categories.items():
            if category is None:
                category_mod = None
            else:
                category_mod = essence['Display_%s_ModsKey' % category]

            cur = len(out)
            for row_key in rows:
                mod = essence['Display_%s_ModsKey' % row_key]
                if mod is None:
                    continue
                if mod == category_mod:
                    continue
                if mod == item_mod:
                    continue

                add_line(get_str(row_key), mod)

            if category_mod is not None and category_mod != item_mod:
                text = get_str(category)
                if cur != len(out):
                    text = get_str('Other').replace('%1%', text)
                add_line(text, category_mod)

        if item_mod:
            # TODO: Can't find items in clientstrings
            add_line(get_str('Other').replace('%1%', 'Items'), item_mod)

        infobox['description'] +='<br />' +  '<br />'.join(out)

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
            ('Level', {
                'template': 'essence_level',
                'condition': lambda v: v > 0,
            }),
            ('EssenceTypeKey', {
                'template': 'essence_type',
                'format': lambda v: v['EssenceType'],
            }),
            ('EssenceTypeKey', {
                'template': 'essence_category',
                'format': lambda v: v['WordsKey']['Text'],
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

    _type_blight_item = _type_factory(
        data_file='BlightCraftingItems.dat',
        data_mapping=(
            ('Tier', {
                'template': 'blight_item_tier',
            }),
        ),
        row_index=True,
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

    _type_incubator = _type_factory(
        data_file='Incubators.dat',
        data_mapping=(
            ('Description', {
                'template': 'incubator_effect',
                'format': lambda v: v,
            }),
        ),
        row_index=True
    )

    def _harvest_seed_extra(self, infobox, base_item_type, harvest_object):

        if not self.rr['HarvestSeedTypes.dat'].index.get('HarvestObjectsKey'):
            self.rr['HarvestSeedTypes.dat'].build_index('HarvestObjectsKey')

        harvest_seed = self.rr['HarvestSeedTypes.dat'].index[
            'HarvestObjectsKey'][harvest_object.rowid]

        _apply_column_map(infobox, (
                ('Text', {
                    'template': 'seed_effect',
                }),
                ('Tier', {
                    'template': 'seed_tier',
                }),
                ('GrowthCycles', {
                    'template': 'seed_growth_cycles',
                }),
                ('RequiredNearbySeed_Tier', {
                    'template': 'seed_required_nearby_seed_tier',
                    'condition': lambda v: v > 0,
                }),
                ('RequiredNearbySeed_Amount', {
                    'template': 'seed_required_nearby_seed_amount',
                    'condition': lambda v: v > 0,
                }),
                ('WildLifeforceConsumedPercentage', {
                    'template': 'seed_consumed_wild_lifeforce_percentage',
                    'condition': lambda v: v > 0,
                }),
                ('VividLifeforceConsumedPercentage', {
                    'template': 'seed_consumed_vivid_lifeforce_percentage',
                    'condition': lambda v: v > 0,
                }),
                ('PrimalLifeforceConsumedPercentage', {
                    'template': 'seed_consumed_primal_lifeforce_percentage',
                    'condition': lambda v: v > 0,
                }),
                ('HarvestCraftOptionsKeys', {
                    'template': 'seed_granted_craft_option_ids',
                    'format': lambda v: ','.join([k['Id'] for k in v]),
                    'condition': lambda v: v,
                }),
            ), harvest_seed)

        return True

    _type_harvest_seed =_type_factory(
        data_file='HarvestObjects.dat',
        data_mapping=(
            ('ObjectType', {
                'template': 'seed_type_id',
                'format': lambda v: v.name.lower(),
            }),
        ),
        function=_harvest_seed_extra,
        #fail_condition=True,
        row_index=True,
    )

    def _harvest_plant_booster_extra(self, infobox, base_item_type,
                                     harvest_object):

        if not self.rr['HarvestSeedTypes.dat'].index.get('HarvestObjectsKey'):
            self.rr['HarvestSeedTypes.dat'].build_index('HarvestObjectsKey')

        harvest_plant_booster = self.rr['HarvestPlantBoosters.dat'].index[
            'HarvestObjectsKey'][harvest_object.rowid]

        _apply_column_map(infobox, (
                ('Radius', {
                    'template': 'plant_booster_radius',
                }),
                ('Lifeforce', {
                    'template': 'plant_booster_lifeforce',
                    'condition': lambda v: v > 0,
                }),
                ('AdditionalCraftingOptionsChance', {
                    'template': 'plant_booster_additional_crafting_options',
                    'condition': lambda v: v > 0,
                }),
                ('RareExtraChances', {
                    'template': 'plant_booster_extra_chances',
                    'condition': lambda v: v > 0,
                }),
            ), harvest_plant_booster)

        return True

    _type_harvest_plant_booster =_type_factory(
        data_file='HarvestObjects.dat',
        data_mapping=(
        ),
        function=_harvest_plant_booster_extra,
        #fail_condition=True,
        row_index=True,
    )

    _cls_map = {
        # Jewellery
        'Amulet': (_type_amulet, ),
        # Armour types
        'Gloves': (_type_level, _type_attribute, _type_armour, ),
        'Boots': (_type_level, _type_attribute, _type_armour, ),
        'Body Armour': (_type_level, _type_attribute, _type_armour, ),
        'Helmet': (_type_level, _type_attribute, _type_armour, ),
        'Shield': (_type_level, _type_attribute, _type_armour, _type_shield),
        # Weapons
        'Claw': (_type_level, _type_attribute, _type_weapon, ),
        'Dagger': (_type_level, _type_attribute, _type_weapon, ),
        'Rune Dagger': (_type_level, _type_attribute, _type_weapon,),
        'Wand': (_type_level, _type_attribute, _type_weapon, ),
        'One Hand Sword': (_type_level, _type_attribute, _type_weapon, ),
        'Thrusting One Hand Sword': (
            _type_level, _type_attribute, _type_weapon,
        ),
        'One Hand Axe': (_type_level, _type_attribute, _type_weapon, ),
        'One Hand Mace': (_type_level, _type_attribute, _type_weapon, ),
        'Sceptre': (_type_level, _type_attribute, _type_weapon,),

        'Bow': (_type_level, _type_attribute, _type_weapon, ),
        'Staff': (_type_level, _type_attribute, _type_weapon, ),
        'Two Hand Sword': (_type_level, _type_attribute, _type_weapon, ),
        'Two Hand Axe': (_type_level, _type_attribute, _type_weapon, ),
        'Two Hand Mace': (_type_level, _type_attribute, _type_weapon, ),
        'Warstaff': (_type_level, _type_attribute, _type_weapon,),
        'FishingRod': (_type_level, _type_attribute, _type_weapon, ),
        # Flasks
        'LifeFlask': (_type_level, _type_flask, _type_flask_charges),
        'ManaFlask': (_type_level, _type_flask, _type_flask_charges),
        'HybridFlask': (_type_level, _type_flask, _type_flask_charges),
        'UtilityFlask': (_type_level, _type_flask, _type_flask_charges),
        'UtilityFlaskCritical': (_type_level, _type_flask,
                                    _type_flask_charges),
        # Gems
        'Active Skill Gem': (_skill_gem, ),
        'Support Skill Gem': (_skill_gem, ),
        # Currency-like items
        'Currency': (_type_currency, ),
        'StackableCurrency': (_type_currency, _type_essence, _type_blight_item),
        'DelveSocketableCurrency': (_type_currency, ),
        'DelveStackableSocketableCurrency': (_type_currency,),
        'HideoutDoodad': (_type_currency, _type_hideout_doodad),
        'Microtransaction': (_type_currency, ),
        'DivinationCard': (_type_currency, ),
        'Incubator': (_type_currency, _type_incubator),
        'HarvestSeed': (_type_currency, _type_harvest_seed),
        'HarvestPlantBooster': (_type_currency, _type_harvest_plant_booster),
        # Labyrinth stuff
        #'LabyrinthItem': (),
        'LabyrinthTrinket': (_type_labyrinth_trinket, ),
        #'LabyrinthMapItem': (),
        # Misc
        'Map': (_type_map,),
        'MapFragment': (_type_map_fragment_mods,),
        'QuestItem': (),
        'AtlasRegionUpgradeItem': (),
        'MetamorphosisDNA': (),
    }

    _conflict_active_skill_gems_map = {
        'Metadata/Items/Gems/SkillGemArcticArmour': True,
        'Metadata/Items/Gems/SkillGemPhaseRun': True,
        'Metadata/Items/Gems/SkillGemLightningTendrils': True,
    }

    def _conflict_active_skill_gems(self, infobox, base_item_type, rr,
                                    language):
        appendix = self._conflict_active_skill_gems_map.get(
            base_item_type['Id'])
        if appendix is None:
            return
        else:
            return base_item_type['Name']

    def _conflict_quest_items(self, infobox, base_item_type, rr, language):
        qid = base_item_type['Id'].replace('Metadata/Items/QuestItems/', '')
        match = re.match(r'(?:SkillBooks|Act[0-9]+)/Book-(?P<id>.*)', qid)
        if match:
            qid = match.group('id')
            ver = re.findall(r'v[0-9]$', qid)
            # Only need one of the skill books from "choice" quets
            if ver:
                if ver[0] != 'v0':
                    return
                qid = qid.replace(ver[0], '')

            try:
                return base_item_type['Name'] + ' (%s)' % \
                       rr['Quest.dat'].index['Id'][qid]['Name']
            except KeyError:
                console('Quest %s not found' % qid, msg=Msg.error)
        else:
            # Descent skill books
            match = re.match(r'SkillBooks/Descent2_(?P<id>[0-9]+)', qid)
            if match:
                return base_item_type['Name'] + ' (%s %s)' % (
                    self._LANG[language]['descent'], match.group('id')
                )
            else:
                # Bandit respec
                match = re.match(r'SkillBooks/BanditRespec(?P<id>.+)', qid)
                if match:
                    return base_item_type['Name'] + ' (%s)' % match.group('id')
                else:
                    match = re.match(
                        r'Metadata/Items/QuestItems/Act7/Firefly(?P<id>[0-9]+)$',
                        base_item_type['Id']
                    )
                    if match:
                        pageid = '%s (%s)' % (
                            base_item_type['Name'],
                             self._LANG[language]['of'] % (
                                 match.group('id'), 7
                             ),
                        )
                        infobox['inventory_icon'] = pageid
                        return pageid

        return

    def _conflict_hideout_doodad(self, infobox, base_item_type, rr, language):
        try:
            ho = rr['HideoutDoodads.dat'].index[
                'BaseItemTypesKey'][base_item_type.rowid]
        except KeyError:
            return

        # This is not perfect, but works currently.
        if ho['HideoutNPCsKey']:
            if base_item_type['Id'].startswith('Metadata/Items/Hideout/Hideout'
                                               'Wounded'):
                name_fmt = self._LANG[self._language]['decoration_wounded']
            else:
                name_fmt = self._LANG[self._language]['decoration']
            name = name_fmt % (
                base_item_type['Name'],
                ho['HideoutNPCsKey']['Hideout_NPCsKey']['ShortName'],
                ho['MasterLevel']
            )
            infobox['inventory_icon'] = name
            return name
        elif base_item_type['Id'].startswith(
                'Metadata/Items/Hideout/HideoutTotemPole'):
            # Ingore the test doodads on purpose
            if base_item_type['Id'].endswith('Test'):
                return

            return base_item_type['Name']

    def _conflict_maps(self, infobox, base_item_type, rr, language):
        id = base_item_type['Id'].replace('Metadata/Items/Maps/', '')
        # Legacy maps
        map_series = None
        for row in rr['MapSeries.dat']:
            if not id.startswith(row['Id']):
                continue
            map_series = row

        name = self._format_map_name(base_item_type, map_series)

        # Each iteration of maps has it's own art
        infobox['inventory_icon'] = name
        # For betrayal map conflict handling is not used, so setting this to
        # false here should be fine
        infobox['drop_enabled'] = False

        return name

    def _conflict_map_fragments(self, infobox, base_item_type, rr, language):
        return base_item_type['Name']

    def _conflict_divination_card(self, infobox, base_item_type, rr, language):
        return '%s (%s)' % (
            base_item_type['Name'],
            base_item_type['ItemClassesKey']['Name'].lower()
        )

    def _conflict_labyrinth_map_item(self, infobox, base_item_type, rr,
                                     language):
        return base_item_type['Name']

    def _conflict_misc_map_item(self, infobox, base_item_type, rr, language):
        return base_item_type['Name']

    def _conflict_delve_socketable_currency(
            self, infobox, base_item_type, rr, language):
        return

    def _conflict_delve_stackable_socketable_currency(
            self, infobox, base_item_type, rr, language):
        return base_item_type['Name']

    def _conflict_atlas_region_upgrade(
            self, infobox, base_item_type, rr, language):
        return base_item_type['Name']

    _conflict_resolver_map = {
        'Active Skill Gem': _conflict_active_skill_gems,
        'QuestItem': _conflict_quest_items,
        'HideoutDoodad': _conflict_hideout_doodad,
        'Map': _conflict_maps,
        'MapFragment': _conflict_map_fragments,
        'DivinationCard': _conflict_divination_card,
        'LabyrinthMapItem': _conflict_labyrinth_map_item,
        'MiscMapItem': _conflict_misc_map_item,
        'DelveSocketableCurrency': _conflict_delve_socketable_currency,
        'DelveStackableSocketableCurrency':
            _conflict_delve_stackable_socketable_currency,
        'AtlasRegionUpgradeItem': _conflict_atlas_region_upgrade,
    }

    def _parse_class_filter(self, parsed_args):
        if parsed_args.item_class_id:
            return [self.rr['ItemClasses.dat'].index['Id'][cls]['Name']
                    for cls in parsed_args.item_class_id]
        elif parsed_args.item_class:
            self.rr['ItemClasses.dat'].build_index('Name')
            return [self.rr['ItemClasses.dat'].index['Name'][cls][0]['Name']
                   for cls in parsed_args.item_class]
        else:
            return []

    def _process_purchase_costs(self, source, infobox):
        for rarity in RARITY:
            if rarity.id >= 5:
                break
            for i, (item, cost) in enumerate(
                    source[rarity.name_upper + 'Purchase'],
                    start=1):
                prefix = 'purchase_cost_%s%s' % (rarity.name_lower, i)
                infobox[prefix + '_name'] = item['Name']
                infobox[prefix + '_amount'] = cost

    def by_rowid(self, parsed_args):
        return self._export(
            parsed_args,
            self.rr['BaseItemTypes.dat'][parsed_args.start:parsed_args.end],
        )

    def by_id(self, parsed_args):
        return self._export(parsed_args, self._item_column_index_filter(
            column_id='Id', arg_list=parsed_args.id
        ))

    def by_name(self, parsed_args):
        return self._export(parsed_args, self._item_column_index_filter(
            column_id='Name', arg_list=parsed_args.name
        ))

    def by_filter(self, parsed_args):
        if parsed_args.re_name:
            parsed_args.re_name = re.compile(parsed_args.re_name,
                                             flags=re.UNICODE)
        if parsed_args.re_id:
            parsed_args.re_id = re.compile(parsed_args.re_id, flags=re.UNICODE)

        items = []

        for item in self.rr['BaseItemTypes.dat']:

            if parsed_args.re_name and not \
                    parsed_args.re_name.match(item['Name']):
                continue

            if parsed_args.re_id and not \
                    parsed_args.re_id.match(item['Id']):
                continue

            items.append(item)

        return self._export(parsed_args, items)

    def _process_base_item_type(self, base_item_type, infobox,
                                not_new_map=True):
            m_id = base_item_type['Id']

            infobox['rarity_id'] = 'normal'

            # BaseItemTypes.dat
            infobox['name'] = base_item_type['Name']
            infobox['class_id'] = base_item_type['ItemClassesKey']['Id']
            infobox['size_x'] = base_item_type['Width']
            infobox['size_y'] = base_item_type['Height']
            if base_item_type['FlavourTextKey']:
                infobox['flavour_text'] = \
                    parser.parse_and_handle_description_tags(
                        rr=self.rr,
                        text=base_item_type['FlavourTextKey']['Text'],
                    )

            if base_item_type['ItemClassesKey']['Id'] not in \
                    self._IGNORE_DROP_LEVEL_CLASSES and \
                    m_id not in self._IGNORE_DROP_LEVEL_ITEMS_BY_ID:
                infobox['drop_level'] = base_item_type['DropLevel']

            base_ot = OTFile(parent_or_base_dir_or_ggpk=self.base_path)
            base_ot.read(
                self.base_path + '/' + base_item_type['InheritsFrom'] + '.ot')
            try:
                ot = self.ot[m_id + '.ot']
            except FileNotFoundError:
                pass
            else:
                base_ot.merge(ot)
            finally:
                ot = base_ot

            if 'enable_rarity' in ot['Mods']:
                infobox['drop_rarities_ids'] = ', '.join(ot['Mods']['enable_rarity'])

            tags = [t['Id'] for t in base_item_type['TagsKeys']]
            infobox['tags'] = ', '.join(tags + list(ot['Base']['tag']))

            if not_new_map:
                infobox['metadata_id'] = m_id

            description = ot['Stack'].get('function_text')
            if description:
                infobox['description'] = self.rr['ClientStrings.dat'].index[
                    'Id'][description]['Text']

            help_text = ot['Base'].get('description_text')
            if help_text:
                infobox['help_text'] = self.rr['ClientStrings.dat'].index['Id'][
                    help_text]['Text']

            for i, mod in enumerate(base_item_type['Implicit_ModsKeys']):
                infobox['implicit%s' % (i+1)] = mod['Id']

    def _process_name_conflicts(self, infobox, base_item_type, language):
        rr = self.rr2 if language != self._language else self.rr
        # Get the base item of other language
        base_item_type = rr['BaseItemTypes.dat'][base_item_type.rowid]

        name = base_item_type['Name']
        cls_id = base_item_type['ItemClassesKey']['Id']
        m_id = base_item_type['Id']
        appendix = self._NAME_OVERRIDE_BY_ID[language].get(m_id)


        if appendix is not None:
            name += appendix
            infobox['inventory_icon'] = name
        elif cls_id == 'Map' or \
                len(rr['BaseItemTypes.dat'].index['Name'][name] +
                    rr['Prophecies.dat'].index['Name'][name]) > 1:
            resolver = self._conflict_resolver_map.get(cls_id)

            if resolver:
                name = resolver(self, infobox, base_item_type, rr, language)
                if name is None:
                    console(
                        'Unresolved ambiguous item "%s" with name "%s". '
                        'Skipping' %
                        (m_id, infobox['name']),
                        msg=Msg.error
                    )
                    return
            else:
                console(
                        'Unresolved ambiguous item "%s" with name "%s". '
                        'Skipping' %
                        (m_id, infobox['name']),
                        msg=Msg.error
                    )
                console('No name conflict handler defined for item class id'
                        ' "%s"' % cls_id, msg=Msg.error)
                return

        return name

    def _export(self, parsed_args, items):
        classes = self._parse_class_filter(parsed_args)
        if classes:
            items = [item for item in items if item['ItemClassesKey']['Name']
                     in classes]

        self._parsed_args = parsed_args
        console('Found %s items. Removing disabled items...' % len(items))
        items = [
            base_item_type for base_item_type in items
            if base_item_type['Id'] not in self._SKIP_ITEMS_BY_ID
        ]
        console('%s items left for processing.' % len(items))

        console('Loading additional files - this may take a while...')
        self._image_init(parsed_args)

        r = ExporterResult()
        self.rr['BaseItemTypes.dat'].build_index('Name')
        self.rr['Prophecies.dat'].build_index('Name')
        self.rr['MapPurchaseCosts.dat'].build_index('Tier')

        if self._language != 'English' and parsed_args.english_file_link:
            self.rr2['BaseItemTypes.dat'].build_index('Name')
            self.rr2['Prophecies.dat'].build_index('Name')

        console('Processing item information...')

        for base_item_type in items:
            name = base_item_type['Name']
            cls_id = base_item_type['ItemClassesKey']['Id']
            m_id = base_item_type['Id']

            infobox = OrderedDict()
            self._process_base_item_type(base_item_type, infobox)
            self._process_purchase_costs(base_item_type, infobox)

            funcs = self._cls_map.get(cls_id)
            if funcs:
                fail = False
                for f in funcs:
                    if not f(self, infobox, base_item_type):
                        fail = True
                        console(
                            'Required extra info for item "%s" with class id '
                            '"%s" not found. Skipping.' % (name, cls_id),
                            msg=Msg.error)
                        break
                if fail:
                    continue

            # handle items with duplicate name entries
            # Maps must be handled in any case due to unique naming style of
            # pages
            page = self._process_name_conflicts(
                infobox, base_item_type, self._language
            )
            if page is None:
                continue
            if self._language != 'English' and parsed_args.english_file_link:
                icon = self._process_name_conflicts(
                    infobox, base_item_type, 'English'
                )
                if cls_id == 'DivinationCard':
                    key = 'card_art'
                else:
                    key = 'inventory_icon'

                if icon:
                    infobox[key] = icon
                else:
                    infobox[key] = \
                        self.rr2['BaseItemTypes.dat'][base_item_type.rowid][
                            'Name']

            # putting this last since it's usually manually added
            if m_id in self._DROP_DISABLED_ITEMS_BY_ID:
                infobox['drop_enabled'] = False

            cond = ItemWikiCondition(
                data=infobox,
                cmdargs=parsed_args,
            )

            r.add_result(
                text=cond,
                out_file='item_%s.txt' % page,
                wiki_page=[
                    {
                        'page': page,
                        'condition': cond,
                    }
                ],
                wiki_message='Item exporter',
            )

            if parsed_args.store_images and self.ggpk:
                if not base_item_type['ItemVisualIdentityKey']['DDSFile']:
                    warnings.warn(
                        'Missing 2d art inventory icon for item "%s"' %
                        base_item_type['Name']
                    )
                    continue

                self._write_dds(
                    data=self.ggpk[base_item_type['ItemVisualIdentityKey'][
                        'DDSFile']].record.extract().read(),
                    out_path=os.path.join(self._img_path, (
                        infobox.get('inventory_icon') or page) +
                        ' inventory icon.dds',
                    ),
                    parsed_args=parsed_args,
                )

        return r

    def _format_map_name(self, base_item_type, map_series, language=None):
        if language is None:
            language = self._language
        if 'Harbinger' in base_item_type['Id']:
            return '%s (%s) (%s)' % (
                base_item_type['Name'],
                self._LANG[language][re.sub(r'^.*Harbinger', '', base_item_type['Id'])],
                map_series['Name']
            )
        else:
            return '%s (%s)' % (
                base_item_type['Name'],
                map_series['Name']
            )

    def _get_map_series(self, parsed_args):
        self.rr['MapSeries.dat'].build_index('Id')
        self.rr['MapSeries.dat'].build_index('Name')
        if parsed_args.map_series_id is not None:
            try:
                map_series = self.rr['MapSeries.dat'].index['Id'][
                    parsed_args.map_series_id]
            except IndexError:
                console(
                    'Invalid map series id',
                    msg=Msg.error)
                return False
        elif parsed_args.map_series is not None:
            try:
                map_series = self.rr['MapSeries.dat'].index['Name'][
                    parsed_args.map_series][0]
            except IndexError:
                console(
                    'Invalid map series name',
                    msg=Msg.error)
                return False
        else:
            map_series = self.rr['MapSeries.dat'][-1]
            console(
                'No map series specified. Using latest series "%s".' % (
                    map_series['Name'],
                ), msg=Msg.warning
            )

        return map_series

    def export_map_icons(self, parsed_args):
        r = ExporterResult()

        if not parsed_args.store_images or not parsed_args.convert_images:
            console(
                'Image storage options must be specified for this function',
                msg=Msg.error,
            )
            return r

        map_series = self._get_map_series(parsed_args)
        if map_series is False:
            return r

        # base images
        self._image_init(parsed_args)
        base_ico = os.path.join(self._img_path, 'Base.dds')

        self._write_dds(
            data=self.ggpk[map_series['BaseIcon_DDSFile']].record.extract().read(),
            out_path=base_ico,
            parsed_args=parsed_args,
        )

        for atlas_node in self.rr['AtlasNode.dat']:
            if not atlas_node['ItemVisualIdentityKey']['DDSFile']:
                warnings.warn(
                   'Missing 2d art inventory icon at index %s' %
                    atlas_node.index,
                )
                continue

            name = atlas_node['WorldAreasKey']['Name']

            ico = os.path.join(self._img_path, name + '.dds')

            self._write_dds(
                data=self.ggpk[atlas_node['ItemVisualIdentityKey'][
                    'DDSFile']].record.extract().read(),
                out_path=ico,
                parsed_args=parsed_args,
            )

            if 'Unique' not in atlas_node['WorldAreasKey']['Id']:
                ico = ico.replace('.dds', '.png')
                for name, color in self._MAP_COLORS.items():
                    #-tint
                    os.system(
                        '''magick convert "%s" -fill rgb(%s) -tint 100 "%s"''' % (
                            ico, color, ico.replace('.png', ' %s.png' % name)
                        ))

        return r

    def export_map(self, parsed_args):
        r = ExporterResult()

        map_series = self._get_map_series(parsed_args)
        if map_series is False:
            return r

        if map_series.rowid <= 3:
            console(
                'Only Betrayal and newer map series are supported by this '
                'function',
                    msg=Msg.error)
            return r

        # Store whether this is the latest map series to determine later whether
        # atlas info should be stored
        latest = map_series == self.rr['MapSeries.dat'][-1]

        self.rr['AtlasNode.dat'].build_index('MapsKey')
        names = set(parsed_args.name)
        map_series_tiers = {}
        for row in self.rr['MapSeriesTiers.dat']:
            maps = row['MapsKey']
            for atlas_node in self.rr['AtlasNode.dat'].index['MapsKey'][maps]:
                # This excludes the unique maps
                if atlas_node['ItemVisualIdentityKey'][
                        'IsAtlasOfWorldsMapIcon']:
                    break
            else:
                # Maps that are no longer on the atlas such as guardian maps
                # or harbinger
                atlas_node = None
            if names and maps['BaseItemTypesKey']['Name'] in names or \
                    not names:
                map_series_tiers[row] = atlas_node

        if parsed_args.store_images:
            if not parsed_args.convert_images:
                console(
                    'Map images need to be processed and require conversion '
                    'option to be enabled.',
                        msg=Msg.error)
                return r

            self._image_init(parsed_args)
            base_ico = os.path.join(self._img_path, 'Map base icon.dds')

            self._write_dds(
                data=self.ggpk[map_series['BaseIcon_DDSFile']].record.extract().read(),
                out_path=base_ico,
                parsed_args=parsed_args,
            )

            base_ico = base_ico.replace('.dds', '.png')

        #
        self.rr['MapSeriesTiers.dat'].build_index('MapsKey')
        self.rr['MapPurchaseCosts.dat'].build_index('Tier')
        self.rr['UniqueMaps.dat'].build_index('ItemVisualIdentityKey')

        for row, atlas_node in map_series_tiers.items():
            maps = row['MapsKey']
            base_item_type = maps['BaseItemTypesKey']
            name = self._format_map_name(
                base_item_type,
                map_series
            )
            tier = row['%sTier' % map_series['Id']]

            # Base info
            infobox = OrderedDict()
            self._process_base_item_type(base_item_type, infobox,
                                         not_new_map=False)
            self._type_map(infobox, base_item_type)

            # Overrides
            infobox['map_tier'] = tier
            infobox['map_area_level'] = 67 + tier
            # Map start dropping at one tier lower, with the exception of
            # tier 1 maps which can drop rather early
            infobox['drop_level'] = 66 + tier if tier > 1 else 58
            infobox['unique_map_area_level'] = 67 + tier
            infobox['map_series'] = map_series['Name']
            infobox['inventory_icon'] = name

            if self._language != 'English' and parsed_args.english_file_link:
                infobox['inventory_icon'] = self._format_map_name(
                    self.rr2['BaseItemTypes.dat'][base_item_type.rowid],
                    self.rr2['MapSeries.dat'][map_series.rowid],
                    'English',
                )
            else:
                infobox['inventory_icon'] = name

            if atlas_node:
                if latest:
                    infobox['atlas_x'] = atlas_node['X']
                    infobox['atlas_y'] = atlas_node['Y']
                    infobox['atlas_region_id'] = atlas_node['AtlasRegionsKey'][
                        'Id']

                    minimum = 0
                    connections = defaultdict(
                        lambda: ['False' for i in range(0, 5)])
                    for i in range(0, 5):
                        tier = atlas_node['Tier%s' % i]
                        infobox['atlas_x%s' % i] = atlas_node['X%s' % i]
                        infobox['atlas_y%s' % i] = atlas_node['Y%s' % i]
                        infobox['atlas_map_tier%s' % i] = tier
                        if tier:
                            if minimum == 0:
                                minimum = i

                        for atlas_node2 in atlas_node['AtlasNodeKeys%s' % i]:
                            ivi = atlas_node2['ItemVisualIdentityKey']
                            if ivi['IsAtlasOfWorldsMapIcon']:
                                key = self._format_map_name(
                                    atlas_node2['MapsKey']['BaseItemTypesKey'],
                                    map_series,
                                )
                            else:
                                key = '%s (%s)' % (
                                    self.rr['UniqueMaps.dat'].index[
                                        'ItemVisualIdentityKey'][ivi][
                                        'WordsKey']['Text'],
                                    map_series['Name']
                                )
                            connections[key][i] = 'True'

                    infobox['atlas_region_minimum'] = minimum
                    for i, (k, v) in enumerate(connections.items(), start=1):
                        infobox['atlas_connection%s_target' % i] = k
                        infobox['atlas_connection%s_tier' % i] = ', '.join(v)

                infobox['flavour_text'] = \
                    atlas_node['FlavourTextKey']['Text'].replace('\n', '<br>')\
                    .replace('\r', '')

            if 0 < tier < 17:
                self._process_purchase_costs(
                    self.rr['MapPurchaseCosts.dat'].index['Tier'][tier],
                    infobox
                )

            '''if maps['UpgradedFrom_MapsKey']:
                infobox['upgeaded_from_set1_group1_page'] = '%s (%s)' % (
                    maps['UpgradedFrom_MapsKey']['BaseItemTypesKey']['Name'],
                    map_series['Name']
                )
                infobox['upgraded_from_set1_group1_amount'] = 3'''

            infobox['release_version'] = self._MAP_RELEASE_VERSION[
                map_series['Id']]

            if not latest:
                infobox['drop_enabled'] = 'False'

            cond = MapItemWikiCondition(
                data=infobox,
                cmdargs=parsed_args,
            )

            r.add_result(
                text=cond,
                out_file='map_%s.txt' % name,
                wiki_page=[
                    {
                        'page': name,
                        'condition': cond,
                    }
                ],
                wiki_message='Map exporter',
            )

            if parsed_args.store_images and self.ggpk:
                if atlas_node is None or \
                        not atlas_node['ItemVisualIdentityKey']['DDSFile']:
                    warnings.warn(
                        'Missing 2d art inventory icon for item "%s"' %
                        base_item_type['Name']
                    )
                    continue

                ico = os.path.join(self._img_path, name + ' inventory icon.dds')

                self._write_dds(
                    data=self.ggpk[atlas_node['ItemVisualIdentityKey'][
                        'DDSFile']].record.extract().read(),
                    out_path=ico,
                    parsed_args=parsed_args,
                )

                ico = ico.replace('.dds', '.png')

                color = None
                if 5 < tier <= 10:
                    color = self._MAP_COLORS['mid tier']
                elif 10 < tier <= 15:
                    color = self._MAP_COLORS['high tier']
                if color:
                    os.system(
                        '''magick convert "%s" -fill rgb(%s) -colorize 100 "%s"''' % (
                        ico, color, ico
                    ))

                os.system(
                    'magick composite -gravity center "%s" "%s" "%s"' % (
                    ico, base_ico, ico
                ))

        return r

    def export_unique_map(self):
        pass
