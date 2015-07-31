"""
Path     PyPoE/cli/exporter/wiki/warbands.py
Name     Wiki mods exporter
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO


http://pathofexile.gamepedia.com


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os

# 3rd Party
from graphviz import Digraph

# Self
from PyPoE.poe.file.dat import DatFile

# =============================================================================
# Classes
# =============================================================================

class WarbandsParser(object):
    def __init__(self, path):
        self.out_path = path
        data_path = os.path.join(path, 'Data')
        desc_path = os.path.join(path, 'Metadata')

        #self.mods = DatFile('Mods.dat', read_file=data_path)
        #self.stats = DatFile('Stats.dat', read_file=data_path)
        self.monster_packs = DatFile('MonsterPacks.dat', read_file=data_path)
        self.monster_varieties = DatFile('MonsterVarieties.dat', read_file=data_path)

        self.warbands_graph = DatFile('WarbandsGraph.dat', read_file=data_path)
        self.warbands_map_graph = DatFile('WarbandsMapGraph.dat', read_file=data_path)
        self.warbands_pack_monsters = DatFile('WarbandsPackMonsters.dat', read_file=data_path)
        self.warbands_pack_numbers = DatFile('WarbandsPackNumbers.dat', read_file=data_path)

        self.world_areas = DatFile('WorldAreas.dat', read_file=data_path)

    def warbands(self):
        for warband in self.warbands_pack_monsters.table_data:
            print(warband['Name'])
            print('')

            '''for key in warband['Data0']:
                mob = self.monster_varieties.table_data[key]
                print(mob['Name'])'''


            for i in range(0, 4):
                ix = 4 - i
                print('Tier %s: %s' % (ix, warband['Tier%sName' % ix ]))
                for key in warband['Data%s' % i]:
                    mob = self.monster_varieties.table_data[key]
                    print(mob['Name'], mob.rowid)
                    #print(mob)
                    #break
                print('')

            print('-' * 80)

    def graph(self, type='normal'):
        if type == 'map':
            dat_file = self.warbands_map_graph
            out_file = 'warbands_map_graph.cv'
        elif type == 'normal':
            dat_file = self.warbands_graph
            out_file = 'warbands_graph.cv'
        else:
            raise ValueError(type)
        dot = Digraph(comment='Warbands Graph', engine='dot')
        for row in dat_file:
            world_area = self.world_areas.table_data[row['WorldAreasKey']]
            dot.node(str(row.rowid), world_area['Name'])
            for node in row['Connections']:
                dot.edge(str(row.rowid), str(node))
        dot.render(os.path.join(self.out_path, out_file), view=True)


if __name__ == '__main__':
    path = 'C:/Temp'
    m = WarbandsParser(path)
    #m.warbands()
    m.graph('map')
    #print(m.warbands_pack_numbers.export_to_html())