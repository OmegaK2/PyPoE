"""
.dat export to SQL

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/dat/sql.py                                    |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Commandline .dat export to SQL using sqlalchemy.

Currently only MySQL is supported.

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import argparse

# 3rd-party
from tqdm import tqdm
from sqlalchemy import Column, Table, MetaData, ForeignKey, create_engine
from sqlalchemy.types import Boolean, Text
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, BIGINT

# self
from PyPoE.poe.file.dat import load_spec, DatFile
from PyPoE.poe.file.ggpk import GGPKFile
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter.util import get_content_ggpk_path

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================


class SQLHandler(object):
    _type_to_sql_map = {
        'bool': Boolean(),
        'byte': TINYINT(),
        'ubyte': TINYINT(unsigned=True),
        'short': SMALLINT(),
        'ushort': SMALLINT(unsigned=True),
        'int': INTEGER(),
        'uint': INTEGER(unsigned=True),
        'long': BIGINT(),
        'ulong': BIGINT(unsigned=True),
        'string': Text(),
    }

    _data_suffix = ''
    _data_key_suffix = 'Key'

    def __init__(self, sub_parser):
        """

        :type sub_parser: argparse._SubParsersAction
        """
        self.sql = sub_parser.add_parser(
            'sql',
            help='Export to MySQL',
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self.sql.set_defaults(func=self.handle_sql)

        self.sql.add_argument(
            '--url',
            help=
                'SQLAlchemy database URL, for more info, see:\n'
                'http://docs.sqlalchemy.org/en/rel_1_0/core/'
                'engines.html#sqlalchemy.create_engine',
            default='mysql+pymysql://root@localhost/test?charset=utf8',
        )

        self.sql.add_argument(
            '-v', '--verbose',
            help='Verbosity\n'
                 '-v  - \n'
                 '-vv - ',
            action='count',
        )

    def _get_data_table_name(self, name, field):
        return '%s_%s%s' % (name, field, self._data_suffix)

    def _get_data_reference_key(self, name):
        return '%s%s' % (name, self._data_key_suffix)

    def _get_field(self, field, section, type):
        if section['key']:
            # SQL doesn't like mixing types, force ulong
            type = self._type_to_sql_map['ulong']
            return Column(field, type, ForeignKey('%s.rid' % section['key'].replace('.dat', '')))
        else:
            return Column(field, type)


    def handle_sql(self, args):
        """

        :param args:
        :type args: argparse.Namespace

        :return:
        """
        engine = create_engine(args.url, echo=False, convert_unicode=True, encoding='utf-8')
        metadata = MetaData(bind=engine)

        spec = load_spec()

        #
        # SQL Tables
        #
        prefix = 'SQL Tables - '
        console(prefix + 'Creating virtual tables from specification...')
        tables = {}
        for name, top_section in tqdm(spec.items()):
            name = name.replace('.dat', '')
            columns = [
                Column('rid', BIGINT(unsigned=True), primary_key=True)
            ]
            for field, section in top_section['fields'].items():
                type_in = section['type']
                dim = 0
                while type_in.startswith('ref|list|'):
                    type_in = type_in[9:]
                    dim += 1

                if type_in.startswith('ref|'):
                    type_in = type_in[4:]

                if dim == 1:
                    table_name = self._get_data_table_name(name, field)
                    tables[table_name] = (Table(
                        table_name,
                        metadata,
                        Column(self._get_data_reference_key(name), BIGINT(unsigned=True), ForeignKey('%s.rid' % (name, ))),
                        self._get_field('value', section, self._type_to_sql_map[type_in]),
                        Column('index', SMALLINT),
                    ))
                elif dim >= 2:
                    raise ValueError('unsupported dim >=2')
                else:
                    col = self._get_field(field, section, self._type_to_sql_map[type_in])
                    columns.append(col)
            tables[name] = Table(name, metadata, *columns)

        console(prefix + 'Committing tables to SQL...')

        metadata.create_all()

        console(prefix + 'Done')

        #
        # SQL Data
        #
        prefix = 'SQL Data - '

        path = get_content_ggpk_path()

        console(prefix + 'Reading "%s"...' % path)

        ggpk = GGPKFile()
        ggpk.read(path)
        ggpk.directory_build()

        console(prefix + 'Parsing .dat files...')

        dat_files = {}
        ggpk_data = ggpk['Data']
        for name in tqdm(spec):
            node = ggpk_data[name]
            if node is None:
                console(prefix + 'Skipping "%s" (missing)' % name, msg=Msg.warning)
                continue

            df = DatFile(name)
            df.read(file_path_or_raw=node.record.extract(), use_dat_value=False)

            dat_files[name] = df

        console(prefix + 'Committing data...')
        con = engine.connect()
        con.execute('SET foreign_key_checks = 0;')
        for name, df in tqdm(dat_files.items()):
            name_noext = name.replace('.dat', '')
            foreign_key = self._get_data_reference_key(name_noext)
            data = []
            for row in df.reader:
                dt = {}
                for k, v in zip(row.keys(), row):
                    if isinstance(v, list) and v:

                        con.execute(
                            tables[
                                self._get_data_table_name(name_noext, k)
                            ].insert(
                                bind=engine,
                                values=[
                                    {
                                        'value': item,
                                        foreign_key: row.rowid,
                                        'index': i,
                                    } for i, item in enumerate(v)
                                ]
                            )
                        )
                    else:
                        dt[k] = v
                data.append(dt)
            con.execute(
                tables[name_noext].insert(bind=engine, values=data)
            )
        con.execute('SET foreign_key_checks = 1;')

        console(prefix + 'All done.')

# =============================================================================
# Functions
# =============================================================================
