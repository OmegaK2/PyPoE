"""
Path     PyPoE/cli/exporter/wiki/mods.py
Name     Wiki mods exporter
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO


http://pathofexile.gamepedia.com


AGREEMENT

See PyPoE/LICENSE


TODO

FIX the jewel generator
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
from glob import glob

# Self
from PyPoE.poe.file.dat import DatFile
from PyPoE.poe.file.translations import DescriptionFile

# =============================================================================
# Globals
# =============================================================================

# =============================================================================
# Classes
# =============================================================================

class ModParser(object):
    dropdata = {
            0: 'Any other item',
            5: 'Bow',
            9: 'Wand',
            10: 'Staff',
            11: 'Mace',
            12: 'Sword',
            13: 'Dagger',
            14: 'Claw',
            15: 'Axe',
            29: 'Crimson' , # STR
            30: 'Viridian', # DEX
            31: 'Cobalt', # INT
            143: 'Weapon Mod?',
            144: 'Two-Hand',
            145: 'Dual-Wield',
            146: 'Shield',
            147: '(2H/Dual/Shield???)',
            148: '(Claw/Dagger/Wand/1h)',
            #149: 'Melee?',
        }
    #affix_wiki = '|-\n| %(Name)s\n| %(Description)s\n| %(Group)s \n| %(0)s || %(29)s || %(30)s || %(31)s || %(5)s || %(9)s || %(10)s || %(11)s || %(12)s || %(13)s || %(14)s || %(15)s  || %(143)s || %(144)s || %(145)s || %(146)s || %(147)s || %(148)s'
    affix_wiki = '|-\n| %(Name)s\n| %(Description)s\n| %(Group)s \n| %(0)s \n| %(29)s \n| %(30)s \n| %(31)s \n| %(GroupWeight)s'

    def __init__(self, path):
        data_path = os.path.join(path, 'Data')
        self.desc_path = os.path.join(path, 'Metadata')

        self.mods = DatFile('Mods.dat', read_file=data_path)
        self.stats = DatFile('Stats.dat', read_file=data_path)

        self.descriptions = DescriptionFile(self.desc_path + '/stat_descriptions.txt')
        #self.stat_descriptions = DescriptionFile(glob(desc_path + '/*_descriptions.txt'))

    def _get_stats(self, mod):
        stats = []
        for i in range(1, 5):
            key = mod['StatsKey%s' % i]
            if key != -1:
                stats.append(self.stats.table_data[key])

        effects = []
        for i in range(0, len(stats)):
            stat = stats[i]
            j = i + 1
            values = [mod['Stat%sMin' % j], mod['Stat%sMax' % j]]

            t = self.descriptions.get_translation(stat['Id'], (values, ))
            if t:
                effects.append('%s' % t[0])
            else:
                if len(values) == 1:
                    values = values[0]
                effects.append('%s %s' % (stat['Id'], values))

        return effects

    def map(self):
        #self.descriptions.merge(DescriptionFile(self.desc_path + '/map_stat_descriptions.txt'))

        mods = []
        for mod in self.mods.table_data:
            if mod['Domain'] != 5:
                continue
            if mod['GenerationType'] not in (1, 2):
                continue
            mods.append(mod)

        for mod in mods:
            try:
                effects = self._get_stats(mod)
                print(mod['Name'], effects)
            except:
                pass


    def tempest(self):
        # Filter by tempest mods

        mods = []
        for mod in self.mods.table_data:
            if mod['CorrectGroup'] == 'MapEclipse':
                mods.append(mod)


        data = []
        for mod in mods:
            if 'of' not in mod['Name']:
                continue
            stats = []
            for i in range(1, 5):
                key = mod['StatsKey%s' % i]
                if key != -1:
                    stats.append(self.stats.table_data[key])

            info = {}
            info['name'] = mod['Name']
            effects = ['The area gets the following modifiers:']
            for i in range(0, len(stats)):
                stat = stats[i]
                j = i + 1
                values = [mod['Stat%sMin' % j], mod['Stat%sMax' % j]]
                if values[0] == values[1]:
                    values.pop(1)
                t= self.descriptions.get_translation([stat['Id'], ], values)
                if t:
                    effects.append('* %s' % t[0])
                else:
                    if len(values) == 1:
                        values = values[0]
                    effects.append('* %s %s' % (stat['Id'], values))
            info['effect'] = '\n'.join(effects)
            data.append(info)

        data.sort(key=lambda info: info['name'])

        for info in data:
            print('|-')
            print('| %s' % info['name'])
            print('| %s' % info['effect'])
            print('| ')

    def jewel(self, type='prefix'):
        data = []
        tset = set()
        for mod in self.mods.table_data:
            # not a jewel
            if mod['Domain'] != 11:
                continue
            if type == 'prefix' and mod['GenerationType'] != 1:
                continue
            elif type == 'suffix' and mod['GenerationType'] != 2:
                continue
            elif type == 'corrupted' and mod['GenerationType'] != 5:
                continue

            listformat = {
                'Name': mod['Name'],
                'Description': '\n'.join(self._get_stats(mod)),
                'Group': mod['Data0'],
                'GroupWeight': [],
            }
            # Jewels: Strange...
            lg = len(mod['SpawnWeight_TagsKeys'])

            #
            for v in mod['SpawnWeight_TagsKeys']:
                tset.add(v)
            if lg == 1:
                listformat['0'] = mod['SpawnWeight_Values'][0]
            else:
                # Last two entries are reversed for no apparent reason other then to confuse us
                listformat[str(mod['SpawnWeight_TagsKeys'][-1])] = str(mod['SpawnWeight_Values'][-2])
                listformat[str(mod['SpawnWeight_TagsKeys'][-2])] = str(mod['SpawnWeight_Values'][-1])
                # These seem to be in order..
                for i in range(0, lg-2):
                    group_id = mod['SpawnWeight_TagsKeys'][i]
                    weight = mod['SpawnWeight_Values'][i]
                    if group_id in (0, 29, 30, 31):
                        listformat[str(group_id)] = weight
                    else:
                        listformat['GroupWeight'].append((group_id,  weight))
            disabled = True
            for item in self.dropdata:
                item = str(item)
                if item not in listformat:
                    listformat[item] = ''
                elif int(listformat[item]) != 0:
                    disabled = False

            if disabled:
                continue

            listformat['GroupWeight'].sort(key=lambda x: x[0])
            for i in range(0, len(listformat['GroupWeight'])):
                listformat['GroupWeight'][i] = '%s: %s' % listformat['GroupWeight'][i]
            listformat['GroupWeight'] = '<br>\n'.join(listformat['GroupWeight'])
            data.append(listformat)
        # Sort my name
        data.sort(key=lambda lf: lf['Name'])

        #print(tset)
        for lf in data:
            print(self.affix_wiki % lf)

if __name__ == '__main__':
    path = 'C:/Temp'
    m = ModParser(path)
    m.jewel('suffix')
    #m.map()