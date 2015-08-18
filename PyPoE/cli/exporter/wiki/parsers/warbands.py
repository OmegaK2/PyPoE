"""
Path     PyPoE/cli/exporter/wiki/parser/warbands.py
Name     Wiki warbands exporter
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
from PyPoE.cli.core import console
from PyPoE.cli.exporter.wiki.handler import *

# =============================================================================
# Classes
# =============================================================================

class WarbandsHandler(ExporterHandler):
    def __init__(self, sub_parser):
        self.parser = sub_parser.add_parser('warbands', help='Warbands Exporter')
        self.parser.set_defaults(func=lambda args: self.parser.print_help())
        lua_sub = self.parser.add_subparsers()

        parser = lua_sub.add_parser(
            'warbands',
            help='Extract warbands info.'
        )
        self.add_default_parsers(
            parser=parser,
            cls=WarbandsParser,
            func=WarbandsParser.warbands,
        )

        parser = lua_sub.add_parser(
            'graph',
            help='Extract the warbands movement graph.',
        )
        self.add_default_parsers(
            parser=parser,
            cls=WarbandsParser,
            handler=WarbandsParser.graph,
        )
        parser.add_argument(
            'type',
            choices=('map', 'normal'),
            help='The type of the graph file to extract.',
        )
        parser.add_argument(
            '-f', '--format',
            choices=('svg', 'pdf', 'png'),
            default='svg',
            help='File format to use when extracting.',
        )

class WarbandsParser(object):
    def __init__(self, **kwargs):
        #self.mods = DatFile('Mods.dat', read_file=data_path).reader
        #self.stats = DatFile('Stats.dat', read_file=data_path).reader

        opt = {
            'use_dat_value': False,
        }
        data_path = kwargs['data_path']

        self.monster_packs = DatFile('MonsterPacks.dat', read_file=data_path, options=opt).reader
        self.monster_varieties = DatFile('MonsterVarieties.dat', read_file=data_path, options=opt).reader

        self.warbands_graph = DatFile('WarbandsGraph.dat', read_file=data_path, options=opt).reader
        self.warbands_map_graph = DatFile('WarbandsMapGraph.dat', read_file=data_path, options=opt).reader
        self.warbands_pack_monsters = DatFile('WarbandsPackMonsters.dat', read_file=data_path, options=opt).reader
        self.warbands_pack_numbers = DatFile('WarbandsPackNumbers.dat', read_file=data_path, options=opt).reader

        self.world_areas = DatFile('WorldAreas.dat', read_file=data_path, options=opt).reader

    def warbands(self, parsed_args):
        out = []
        for warband in self.warbands_pack_monsters.table_data:
            out.append(warband['Name'])
            out.append('\n\n')

            '''for key in warband['Data0']:
                mob = self.monster_varieties.table_data[key]
                out.append(mob['Name'])'''


            for i in range(0, 4):
                ix = 4 - i
                out.append('Tier %s: %s\n' % (ix, warband['Tier%sName' % ix ]))
                for key in warband['Data%s' % i]:
                    mob = self.monster_varieties.table_data[key]
                    out.append("%s %s\n" % (mob['Name'], mob.rowid))
                    #out.append(mob)
                    #break
                out.append('\n')

            out.append('-' * 80 + '\n')

        r = ExporterResult()
        r.add_result(lines=out, out_file='warbands.txt')

        return r

    def graph(self, parsed_args, **kwargs):
        if parsed_args.type == 'map':
            dat_file = self.warbands_map_graph
            out_file = 'warbands_map_graph.cv'
        elif parsed_args.type == 'normal':
            dat_file = self.warbands_graph
            out_file = 'warbands_graph.cv'

        print ('Creating Graph...')
        dot = Digraph(comment='Warbands Graph', engine='dot', format=parsed_args.format)
        for row in dat_file:
            world_area = self.world_areas.table_data[row['WorldAreasKey']]
            dot.node(str(row.rowid), world_area['Name'])
            for node in row['Connections']:
                dot.edge(str(row.rowid), str(node))

        out_path = os.path.join(kwargs['out_dir'], out_file)
        console('Writing graph to "%s"...' % out_path)
        dot.render(out_path, view=parsed_args.print)

        print ('Done.')
        return 0