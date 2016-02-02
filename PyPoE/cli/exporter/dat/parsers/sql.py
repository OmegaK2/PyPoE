"""
.dat export to SQL

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/dat/parsers/sql.py                            |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Commandline .dat export to SQL using sqlalchemy.

Currently only MySQL is supported.

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import argparse
from collections import defaultdict

# 3rd-party
from tqdm import tqdm
import sqlalchemy
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
                'engines.html#sqlalchemy.sqlalchemy.create_engine',
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

        self.sql.add_argument(
            '--skip-child-data',
            help='Skips committing of child data (i.e. list entries)',
            action='store_true',
        )

        self.add_default_arguments(self.sql)

    def _get_data_table_name(self, name, field):
        return '%s_%s%s' % (name, field, self._data_suffix)

    def _get_data_reference_key(self, name):
        return '%s%s' % (name, self._data_key_suffix)

    def _get_field(self, section, type, field=None):
        args = []
        kwargs = {}
        if section['unique']:
            kwargs['unique'] = True
            if type == 'string':
                type = 'varchar'

        if section['key']:
            # SQL doesn't like mixing types, force ulong
            if type != 'varchar':
                type = 'ulong'

            if section['key_offset']:
                foreign_key = 'rid'
            elif section['key_id']:
                foreign_key = section['key_id']
            else:
                foreign_key = 'rid'

            other = section['key'][:-4]

            args.append(sqlalchemy.ForeignKey(
                '%s.%s' % (other, foreign_key)
            ))
            kwargs['nullable'] = True
        # TODO: This is a bit of a temporary fix
        elif section.name.startswith('Key'):
            kwargs['nullable'] = True
        else:
            kwargs['nullable'] = False

        if not isinstance(field, str):
            field = self._get_data_list_field_name(section, field)

        return sqlalchemy.Column(field, self._type_to_sql_map[type], *args, **kwargs)

    def _get_list_field_columns(self, parent_name):
        return [
            sqlalchemy.Column(
                'rid',
                BIGINT(unsigned=True),
                primary_key=True,
                autoincrement=True,
            ),
            sqlalchemy.Column(
                'index',
                SMALLINT,
                nullable=False,
            ),
            sqlalchemy.Column(
                self._get_data_reference_key(parent_name),
                BIGINT(unsigned=True),
                sqlalchemy.ForeignKey('%s.rid' % (parent_name, )),
                nullable=False,
            ),
        ]

    def _get_data_list_field_name(self, section, index=None):
        if section['key']:
            return self._get_data_reference_key(section['key'][:-4])
        elif index is not None:
            return 'value' + str(index)
        else:
            return 'value'

    def handle(self, args):
        """

        :param args:
        :type args: argparse.Namespace

        :return:
        """
        super(SQLExportHandler, self).handle(args)

        prefix = 'SQL init - '

        console(prefix + 'Establishing DB connection')
        engine = sqlalchemy.create_engine(args.url, echo=False, convert_unicode=True, encoding='utf-8')
        metadata = sqlalchemy.MetaData(bind=engine)
        con = engine.connect()

        console(prefix + 'Setting session sql_modes')
        result = con.execute('SELECT @@SESSION.sql_mode;')
        sql_modes = result.fetchone()[0].split(',')
        if 'NO_AUTO_VALUE_ON_ZERO' not in sql_modes:
            sql_modes.append('NO_AUTO_VALUE_ON_ZERO')
            con.execute("SET SESSION sql_mode=%s", ','.join(sql_modes))

        spec = load_spec()

        #
        # SQL tables
        #

        prefix = 'SQL tables - '
        console(prefix + 'Creating virtual tables from specification...')
        tables = {}
        for name in tqdm(args.files):
            top_section = spec[name]
            name = name.replace('.dat', '')
            columns = [
                sqlalchemy.Column('rid', BIGINT(unsigned=True), primary_key=True)
            ]
            for field in top_section['columns_zip']:
                if field in top_section['fields']:
                    section = top_section['fields'][field]
                    type_in = section['type']
                    dim = 0
                    while type_in.startswith('ref|list|'):
                        type_in = type_in[9:]
                        dim += 1

                    if type_in.startswith('ref|'):
                        type_in = type_in[4:]

                    if dim == 1:
                        table_name = self._get_data_table_name(name, field)

                        lcols = self._get_list_field_columns(parent_name=name)
                        lcols.append(self._get_field(section, type_in))

                        tables[table_name] = sqlalchemy.Table(
                            table_name,
                            metadata,
                            *lcols
                        )
                    elif dim >= 2:
                        raise ValueError('unsupported dim >=2')
                    else:
                        col = self._get_field(section, type_in, field)
                        columns.append(col)
                elif field in top_section['virtual_fields']:
                    # We know we are a list field
                    fields = top_section['virtual_fields'][field]['fields']
                    vcolumns = self._get_list_field_columns(parent_name=name)

                    for i, sub_field in enumerate(fields):
                        section = top_section['fields'][sub_field]
                        # We know the type starts with ref|list
                        vcolumns.append(
                            self._get_field(section, section['type'][9:], i)
                        )

                    table_name = self._get_data_table_name(name, field)
                    tables[table_name] = sqlalchemy.Table(
                        table_name,
                        metadata,
                        *vcolumns
                    )

            tables[name] = sqlalchemy.Table(name, metadata, *columns)

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
            con.execute('SET SESSION foreign_key_checks = 0;')
            for name, df in tqdm(dat_files.items()):
                name_noext = name.replace('.dat', '')
                foreign_key = self._get_data_reference_key(name_noext)
                data = []
                indexes = defaultdict(int)
                dr = df.reader

                sub_field_names = {}

                for field_name in dr.columns_zip:
                    if field_name in dr.specification['fields']:
                        sub_field_names[field_name] = \
                            self._get_data_list_field_name(
                                dr.specification['fields'][field_name]
                            )
                    elif field_name in dr.specification['virtual_fields']:
                        vsection = dr.specification['virtual_fields'][field_name]
                        names = []
                        for i, fn in enumerate(vsection['fields']):
                            names.append(self._get_data_list_field_name(
                                dr.specification['fields'][fn], index=i)
                            )
                        sub_field_names[field_name] = names

                for row in df.reader:
                    dt = {
                        'rid': row.rowid,
                    }

                    for k in dr.columns_zip:
                        v = row[k]
                        if isinstance(v, (list, zip)) and not args.skip_child_data and v:
                            if isinstance(v, list):
                                values = [
                                    {
                                        'rid': indexes[k] + i,
                                        sub_field_names[k]: item,
                                        foreign_key: row.rowid,
                                        'index': i,
                                    } for i, item in enumerate(v)
                                ]
                            elif isinstance(v, zip):
                                values = []
                                for i, items in enumerate(v):
                                    value_data = {
                                        'rid': indexes[k] + i,
                                        foreign_key: row.rowid,
                                        'index': i,
                                    }
                                    for j, item in enumerate(items):
                                        value_data[sub_field_names[k][j]] = item
                                    values.append(value_data)

                            length = len(values)
                            if length:
                                con.execute(
                                    tables[
                                        self._get_data_table_name(name_noext, k)
                                    ].insert(
                                        bind=engine,
                                        values=values,
                                    )
                                )

                                indexes[k] += length
                        else:
                            if df.reader.table_columns[k]['section']['key_offset']:
                                v -= df.reader.table_columns[k]['section']['key_offset']
                            if df.reader.table_columns[k]['section']['key'] and v == '':
                                v = None
                            dt[k] = v
                    data.append(dt)
                con.execute(
                    tables[name_noext].insert(bind=engine, values=data)
                )
            con.execute('SET SESSION foreign_key_checks = 1;')

        console(prefix + 'All done.')

# =============================================================================
# Functions
# =============================================================================
