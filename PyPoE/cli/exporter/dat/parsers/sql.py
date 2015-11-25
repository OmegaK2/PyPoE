"""
.dat export to SQL

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/dat/parsers/sql.py                            |
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
from sqlalchemy.types import Boolean, Text, String
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, BIGINT

# self
from PyPoE.poe.file.dat import load_spec
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter.dat.handler import DatExportHandler

# =============================================================================
# Globals
# =============================================================================

__all__ = ['SQLExportHandler']

# =============================================================================
# Classes
# =============================================================================


class SQLExportHandler(DatExportHandler):
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
        'varchar': String(255),
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
        self.sql.set_defaults(func=self.handle)

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

        self.sql.add_argument(
            '--skip-data',
            help='Skip gathering the data and committing to the database',
            action='store_true',
        )

        self.add_default_arguments(self.sql)

    def _get_data_table_name(self, name, field):
        return '%s_%s%s' % (name, field, self._data_suffix)

    def _get_data_reference_key(self, name):
        return '%s%s' % (name, self._data_key_suffix)

    def _get_field(self, field, section, type):
        args = []
        kwargs = {}
        if section['primary_key']:
            kwargs['primary_key'] = section['primary_key']
            if type == 'string':
                type = 'varchar'

        if section['key']:
            # SQL doesn't like mixing types, force ulong
            type = 'ulong'
            args.append(ForeignKey('%s.rid' % section['key'][:-4]))
            kwargs['nullable'] = True
        # TODO: This is a bit of a temporary fix
        elif section.name.startswith('Key'):
            kwargs['nullable'] = True
        else:
            kwargs['nullable'] = False

        return Column(field, self._type_to_sql_map[type], *args, **kwargs)

    def handle(self, args):
        """

        :param args:
        :type args: argparse.Namespace

        :return:
        """
        super(SQLExportHandler, self).handle(args)

        engine = create_engine(args.url, echo=False, convert_unicode=True, encoding='utf-8')
        metadata = MetaData(bind=engine)

        spec = load_spec()

        #
        # SQL Tables
        #
        prefix = 'SQL Tables - '
        console(prefix + 'Creating virtual tables from specification...')
        tables = {}
        for name in tqdm(args.files):
            top_section = spec[name]
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
                        Column(self._get_data_reference_key(name), BIGINT(unsigned=True), ForeignKey('%s.rid' % (name, )), nullable=False),
                        self._get_field('value', section, type_in),
                        Column('index', SMALLINT, nullable=False),
                    ))
                elif dim >= 2:
                    raise ValueError('unsupported dim >=2')
                else:
                    col = self._get_field(field, section, type_in)
                    columns.append(col)
            tables[name] = Table(name, metadata, *columns)

        console(prefix + 'Committing tables to SQL...')

        metadata.create_all()

        console(prefix + 'Done')

        #
        # SQL Data
        #
        if not args.skip_data:
            prefix = 'SQL Data - '

            dat_files = self._read_dat_files(args, prefix=prefix)

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
