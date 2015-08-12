"""
Path     PyPoE/cli/exporter/wiki/lua.py
Name     Wiki lua exporter
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

This small script reads the data from quest rewards and exports it to a lua
table for use on the unofficial Path of Exile wiki located at:
http://pathofexile.gamepedia.com


AGREEMENT

See PyPoE/LICENSE


TODO

CLI interface/args
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import warnings

# Self
from PyPoE.poe.file.dat import DatFile
from PyPoE.cli.exporter.wiki.handler import ExporterHandler

# =============================================================================
# Globals
# =============================================================================

__all__= ['QuestRewardReader', 'LuaHandler']

class_map = {
    -1: "All",
    0: "Marauder",
    1: "Witch",
    2: "Scion",
    3: "Ranger",
    4: "Duelist",
    5: "Shadow",
    6: "Templar",
}

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
    # Two Stone Rings
    # TODO actually no idea which one is actually which
    641: "Two-Stone_Ring_(ruby_and_sapphire)",
    642: "Two-Stone Ring (sapphire and topaz)",
    643: "Two-Stone Ring (ruby and topaz)",
}

item_format_order = [
    'reward', 'type', 'class', 'difficulty', 'quest', 'quest_id', 'npc', 'act',
    'itemlevel', 'rarity', 'sockets', 'page_link'
]

# =============================================================================
# Classes
# =============================================================================

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
            outfile='quest_rewards.lua',
        )

        parser = lua_sub.add_parser(
            'vendor_rewards',
            help='Extract quest vendor rewards into lua.',
        )
        self.add_default_parsers(
            parser=parser,
            cls=QuestRewardReader,
            func=QuestRewardReader.read_vendor_rewards,
            outfile='vendor_rewards.lua',
        )

class QuestRewardReader(object):
    def __init__(self, data_path, desc_path):
        opt = {
            'use_dat_value': False,
        }

        self.base_item_types = DatFile('BaseItemTypes.dat', read_file=data_path, options=opt).reader

        self.difficulties = DatFile('Difficulties.dat', read_file=data_path, options=opt).reader

        #base_item_classes = DatFile('ItemClassesDisplay.dat')
        #base_item_classes.read_from_file(path)

        self.npcs = DatFile('NPCs.dat', read_file=data_path, options=opt).reader

        self.quests = DatFile('Quest.dat', read_file=data_path, options=opt).reader

        self.quest_states = DatFile('QuestStates.dat', read_file=data_path, options=opt).reader

        self.quest_rewards = DatFile('QuestRewards.dat', read_file=data_path, options=opt).reader

        self.quest_vendor_rewards = DatFile('QuestVendorRewards.dat', read_file=data_path, options=opt).reader

    def _write_lua(self, outdata, data_type):
        # Pre-sort
        outdata.sort(key=lambda x: x['class_id'])
        outdata.sort(key=lambda x: x['reward'])
        outdata.sort(key=lambda x: x['quest_id'])
        outdata.sort(key=lambda x: x['act'])
        if data_type != 'vendor':
            outdata.sort(key=lambda x: x['difficulty'])

        out = []
        out.append('local rewards = {\n')
        for data in outdata:
            out.append('\t{\n')
            for item in item_format_order:
                if item not in data:
                    continue
                value = data[item]
                if isinstance(value, int):
                    f = '\t\t%s=%s,\n'
                else:
                    f = '\t\t%s="%s",\n'
                out.append(f % (item, value))
            out.append('\t},\n')
        out.append('\n}')
        out.append('\n')
        out.append('return rewards')

        return out

    def read_quest_rewards(self, args):
        outdata = []
        for row in self.quest_rewards.table_data:
            # Find the corressponding keys
            itemid = row['BaseItemTypesKey']
            for item in self.base_item_types.table_data:
                if item.rowid == itemid:
                    break

            questid = row['QuestKey']
            for quest in self.quests.table_data:
                if quest.rowid == questid:
                    break

            # Format the data
            data = {}

            data['quest'] = quest['Title']
            data['quest_id'] = quest['UniqueId']
            # Quest not implemented or buggy or master stuff
            if not data['quest']:
                continue
            # Any of the quest branches gives the reward and disables the other
            if data['quest'] == 'Victario\'s Secrets':
                if data['quest_id'] != 'a3q11':
                    continue
            data['act'] = quest['Act']

            itemcls_n = item['ItemClass']
            if itemcls_n in (19, 20): # Skills
                itemcls = 'skill'
            elif itemcls_n == 40: # can be ignored I guess
                itemcls = 'hideout'
            else: #item
                itemcls = 'item'

            # Item is default class
            if itemcls != 'item':
                data['type'] = itemcls

            data['class'] = class_map[row['CharactersKey']]
            # TODO: Unused atm, only for sorting
            data['class_id'] = row['CharactersKey']

            r = row['Rarity']
            rarity = rarities[r] if r in rarities else '???'

            # Start counting at 1 for some reason...
            difficulty_id = row['Difficulty']
            data['difficulty'] = difficulty_id
            #data['difficulty'] = difficulties.table_data[difficulty_id-1]['Id']

            sockets = row['SocketGems']
            if sockets:
                data['sockets'] = sockets

            name = item['Name']

            # Some of unique items follow special rules
            if itemcls_n == 32 and name.startswith('Book of'):
                data['page_link'] = '%s (%s)' % (name, data['quest'])
            # Non non quest items or skill gems have their rarity added
            if itemcls_n not in (19, 20, 32):
                data['itemlevel'] = row['ItemLevel']
                data['rarity'] = rarity
                # Unique and not a quest item or gem
                if rarity == 'Unique':
                    uid = row['UniqueId']
                    if uid in item_map:
                        name = item_map[uid]
                    else:
                        warnings.warn('Uncaptured unique item. %s %s %s %s' % (uid, data['quest'], data['difficulty'], name))

            data['reward'] = name

            if name == 'Two-Stone Ring':
                itemid = item['ItemVisualIdentityKey']
                if itemid in item_map:
                    data['page_link'] = item_map[itemid]
                else:
                    warnings.warn('Fix ItemID for two-stones')

            # Add to formatting list
            outdata.append(data)
        return self._write_lua(outdata, 'quest')

    def read_vendor_rewards(self, args):
        outdata = []
        for row in self.quest_vendor_rewards.table_data:
            # Find the corresponding keys
            quest_keys = []
            quest_state_key = row['QuestState']

            for quest_state_row in self.quest_states.table_data:
                if quest_state_key not in quest_state_row['QuestStates']:
                    continue

                quest_keys.append(quest_state_row['QuestKey'])

            quests = []
            # Fix for eternal night mare...
            if not quest_keys and quest_state_key == 698:
                quest_keys.append(38)


            for quest in self.quests.table_data:
                for quest_key in quest_keys:
                    if quest.rowid == quest_key:
                        quests.append(quest)
                        break

            if not quests:
                warnings.warn('Row %s: Quest vendor rewardwith no quests...?' % row.rowid)
                continue

            items = []
            item_keys = row['BaseItemTypesKeys']
            for item in self.base_item_types.table_data:
                for key in item_keys:
                    if key == item.rowid:
                        items.append(item)
                        item_keys.remove(key)
                        break

            if not items:
                warnings.warn('Row %s: No corressponding items found for given item ids' % row.rowid)
                continue

            classes = row['CharactersKeys']

            for npc in self.npcs.table_data:
                if npc.rowid == row['NPCKey']:
                    break

            # Format the data:

            for cls in classes:
                for quest in quests:
                    for item in items:
                        data = {}

                        data['quest'] = quest['Title']
                        data['quest_id']  = quest['UniqueId']
                        data['act'] = quest['Act']
                        data['reward'] = item['Name']
                        # Pretty sure they are all skills...
                        data['type'] = 'skill'
                        data['class'] = class_map[cls]
                        data['class_id'] = cls
                        data['npc'] = npc['Name']

                        outdata.append(data)
        return self._write_lua(outdata, 'vendor')