"""
Wiki warbands exporter

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/wiki/parsers/warbands.py                      |
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
import os

# 3rd Party
from graphviz import Digraph

# Self
from PyPoE.cli.core import console
from PyPoE.cli.exporter.wiki.handler import *
from PyPoE.cli.exporter.wiki.parser import BaseParser

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
            wiki=False,
        )

        parser = lua_sub.add_parser(
            'graph',
            help='Extract the warbands movement graph.',
        )
        self.add_default_parsers(
            parser=parser,
            cls=WarbandsParser,
            handler=WarbandsParser.graph,
            wiki=False,
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

class WarbandsParser(BaseParser):

    # Load files in advance
    _files = [
        'MonsterPacks.dat',
        'MonsterVarieties.dat',
        'WarbandsGraph.dat',
        'WarbandsMapGraph.dat',
        'WarbandsPackNumbers.dat',
        'WarbandsPackMonsters.dat',
        'WorldAreas.dat',
    ]

    # Load translations in advance
    _translations = [
    ]

    def warbands(self, parsed_args):
        out = []
        for warband in self.rr['WarbandsPackMonsters.dat']:
            out.append(warband['Id'])
            out.append('\n\n')

            '''for key in warband['Data0']:
                mob = self.monster_varieties.table_data[key]
                out.append(mob['Name'])'''


            for i in range(1, 5):
                out.append('Tier %s: %s\n' % (i, warband['Tier%sName' % i]))
                for mv in warband['Tier%s_MonsterVarietiesKeys' % i]:
                    out.append("%s %s\n" % (mv['Name'], mv.rowid))
                    #out.append(mob)
                    #break
                out.append('\n')

            out.append('-' * 80 + '\n')

        r = ExporterResult()
        r.add_result(text=''.join(out), out_file='warbands.txt')

        return r

    def graph(self, parsed_args, **kwargs):
        if parsed_args.type == 'map':
            dat_file = self.rr['WarbandsMapGraph.dat']
            out_file = 'warbands_map_graph.cv'
        elif parsed_args.type == 'normal':
            dat_file = self.rr['WarbandsGraph.dat']
            out_file = 'warbands_graph.cv'

        console('Creating Graph...')
        dot = Digraph(comment='Warbands Graph', engine='dot', format=parsed_args.format)
        for row in dat_file:
            world_area = row['WorldAreasKey']
            dot.node(str(row.rowid), world_area['Name'])
            for node in row['Connections']:
                dot.edge(str(row.rowid), str(node))

        out_path = os.path.join(kwargs['out_dir'], out_file)
        console('Writing graph to "%s"...' % out_path)
        dot.render(out_path, view=parsed_args.print)

        console('Done.')
        return 0