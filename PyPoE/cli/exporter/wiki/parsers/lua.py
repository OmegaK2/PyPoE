"""
Wiki lua exporter

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/wiki/parsers/lua.py                           |
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
import warnings
from collections import namedtuple

# Self
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter.wiki.handler import *
from PyPoE.cli.exporter.wiki.parser import BaseParser

# =============================================================================
# Globals
# =============================================================================

__all__= ['QuestRewardReader', 'LuaHandler']

rarities = {
    1: 'Normal',
    2: 'Magic',
    3: 'Rare',
    5: 'Unique',
}

# TODO find a better way
# TODO Break with updates
item_map = {
    # Though Scared Ground, Normal
    423: "Survival Instincts", # Veridian
    424: "Survival Skills", # Crimson
    425: "Survival Secrets", # Cobalt
    # Though Scared Ground, Cruel
    454: "Poacher's Aim", # Verdian
    455: "Warlord's Reach ", # Crimson
    456: "Assassin's Haste", # Cobalt
    # Though Scared Ground, Merciless
    457: "Conqueror's Efficiency", # crimson
    458: "Conqueror's Potency", # cobalt
    459: "Conqueror's Longevity", #viridian
}

two_stone_map = {
    'Ring12': "Two-Stone Ring (ruby and topaz)",
    'Ring13': "Two-Stone Ring (sapphire and topaz)",
    'Ring14': "Two-Stone Ring (ruby and sapphire)",
}

item_format_order = [
    'reward', 'type', 'class_name', 'difficulty', 'quest', 'quest_id', 'npc',
    'act', 'itemlevel', 'rarity', 'sockets', 'page_link'
]

out_key_map = {
    'class_name': 'class',
}

# =============================================================================
# Classes
# =============================================================================

# class factory
RewardDataTuple = namedtuple('RewardDataTuple', [
    'quest', 'quest_id', 'act', 'type', 'class_name', 'class_id', 'rarity',
    'difficulty', 'sockets', 'page_link', 'itemlevel', 'reward'
])
VendorRewardDataTuple = namedtuple('VendorRewardDataTuple', [
    'quest', 'quest_id', 'act', 'reward', 'type', 'class_name', 'class_id',
    'npc'
])


class LuaHandler(ExporterHandler):
    def __init__(self, sub_parser):
        self.parser = sub_parser.add_parser('lua', help='Lua Exporter')
        self.parser.set_defaults(func=lambda args: self.parser.print_help())
        lua_sub = self.parser.add_subparsers()

        parser = lua_sub.add_parser(
            'quest_rewards',
            help='Extract quest rewards into lua.'
        )
        self.add_default_parsers(
            parser=parser,
            cls=QuestRewardReader,
            func=QuestRewardReader.read_quest_rewards,
        )

        parser = lua_sub.add_parser(
            'vendor_rewards',
            help='Extract quest vendor rewards into lua.',
        )
        self.add_default_parsers(
            parser=parser,
            cls=QuestRewardReader,
            func=QuestRewardReader.read_vendor_rewards,
        )


class QuestRewardReader(BaseParser):
    # Load the files we need
    _files = [
        'BaseItemTypes.dat',
        'Characters.dat',
        'Difficulties.dat',
        'NPCs.dat',
        'Quest.dat',
        'QuestStates.dat',
        'QuestRewards.dat',
        'QuestVendorRewards.dat',
    ]

    def _write_lua(self, outdata, data_type):
        if data_type == 'vendor':
            subpage = 'vendor_reward_data'
        else:
            subpage = 'data'

        # Pre-sort
        outdata.sort(key=lambda x: x.class_id)
        outdata.sort(key=lambda x: x.reward)
        outdata.sort(key=lambda x: x.quest_id)
        outdata.sort(key=lambda x: x.act)
        if data_type != 'vendor':
            outdata.sort(key=lambda x: x.difficulty)

        out = []
        out.append('local rewards = {\n')
        for data in outdata:
            out.append('\t{\n')
            for item in item_format_order:
                if not hasattr(data, item):
                    continue
                value = getattr(data, item)
                if value is None:
                    continue

                if isinstance(value, int):
                    f = '\t\t%s=%s,\n'
                else:
                    f = '\t\t%s="%s",\n'

                try:
                    outkey = out_key_map[item]
                except KeyError:
                    outkey = item
                out.append(f % (outkey, value))
            out.append('\t},\n')
        out.append('\n}')
        out.append('\n')
        out.append('return rewards')

        r = ExporterResult()
        r.add_result(
            lines=out,
            out_file='%s_rewards.txt' % data_type,
            wiki_page='Module:QuestReward/%s' % subpage,
        )

        return r

    def read_quest_rewards(self, args):
        outdata = set()
        for row in self.rr['QuestRewards.dat']:
            # Find the corresponding keys
            item = row['BaseItemTypesKey']
            quest = row['QuestKey']
            character = row['CharactersKey']
            difficulty = row['Difficulty']
            itemcls = item['ItemClassesKey']['Name']

            # Format the data
            data = {}

            data['quest'] = quest['Title']
            data['quest_id'] = quest['Id']
            # Quest not implemented or buggy or master stuff
            if not data['quest']:
                continue
            # Any of the quest branches gives the reward and disables the other
            if data['quest'] == 'Victario\'s Secrets':
                if data['quest_id'] != 'a3q11':
                    continue
            data['act'] = quest['Act']

            if itemcls in ['Active Skill Gems', 'Support Skill Gems']: # Skills
                item_type = 'skill'
            elif itemcls == 'Hideout Doodads': # can be ignored I guess
                item_type = 'hideout'
            else:
                item_type = 'item'

            # Item is default class
            if item_type != 'item':
                data['type'] = item_type

            # TODO: Unused class_id atm, only for sorting
            if character is None:
                data['class_name'] = 'All'
                data['class_id'] = -1
            else:
                data['class_name'] = character['Name']
                data['class_id'] = character.rowid

            r = row['Rarity']
            rarity = rarities[r] if r in rarities else '???'

            # Start counting at 1 for some reason...

            data['difficulty'] = difficulty
            #data['difficulty'] = difficulties.table_data[difficulty_id-1]['Id']

            sockets = row['SocketGems']
            if sockets:
                data['sockets'] = sockets

            name = item['Name']

            # Some of unique items follow special rules
            if itemcls == 'Quest Items' and name.startswith('Book of'):
                data['page_link'] = '%s (%s)' % (name, data['quest'])
            # Non non quest items or skill gems have their rarity added
            if itemcls not in {'Active Skill Gems', 'Support Skill Gems', 'Quest Items'}:
                data['itemlevel'] = row['ItemLevel']
                data['rarity'] = rarity
                # Unique and not a quest item or gem
                if rarity == 'Unique':
                    uid = row['Key0']
                    if uid in item_map:
                        name = item_map[uid]
                    else:
                        warnings.warn('Uncaptured unique item. %s %s %s %s' % (uid, data['quest'], data['difficulty'], name))

            data['reward'] = name

            if name == 'Two-Stone Ring':
                itemid = item['ItemVisualIdentityKey']['Id']
                if itemid in two_stone_map:
                    data['page_link'] = two_stone_map[itemid]
                else:
                    warnings.warn('Fix ItemID for two-stones')

            for field in RewardDataTuple._fields:
                if field not in data:
                    data[field] = None

            # Add to formatting list
            outdata.add(RewardDataTuple(**data))
        return self._write_lua(list(outdata), 'quest')

    def read_vendor_rewards(self, args):
        outdata = set()
        eternal_nightmare_quest = None
        for row in self.rr['Quest.dat']:
            if row['Id'] == 'a4q1':
                eternal_nightmare_quest = row
                break

        if eternal_nightmare_quest is None:
            console('Could not find the Eternal Nightmare quest. Stopping',
                    msg=Msg.error)


        for row in self.rr['QuestVendorRewards.dat']:
            # Find the corresponding keys
            quests = []
            quest_state_key = row['QuestState']

            for quest_state_row in self.rr['QuestStates.dat']:
                if quest_state_key not in quest_state_row['QuestStates']:
                    continue

                quests.append(quest_state_row['QuestKey'])

            # Fix for eternal night mare...
            if not quests and quest_state_key == 698:
                quests.append(eternal_nightmare_quest)

            if not quests:
                warnings.warn('Row %s: Quest vendor rewardwith no quests...?' % row.rowid)
                continue

            items = row['BaseItemTypesKeys']

            if not items:
                warnings.warn('Row %s: No corressponding items found for given item ids' % row.rowid)
                continue

            classes = row['CharactersKeys']

            # Format the data:

            for cls in classes:
                for quest in quests:
                    for item in items:
                        data = {}

                        data['quest'] = quest['Title']
                        data['quest_id'] = quest['Id']
                        data['act'] = quest['Act']
                        data['reward'] = item['Name']
                        # Pretty sure they are all skills...
                        data['type'] = 'skill'
                        data['class_name'] = cls['Name']
                        data['class_id'] = cls.rowid
                        data['npc'] = row['NPCKey']['Name']

                        outdata.add(VendorRewardDataTuple(**data))
        return self._write_lua(list(outdata), 'vendor')
