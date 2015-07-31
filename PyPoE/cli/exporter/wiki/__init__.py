"""
Path     PyPoE/cli/exporter/wiki/__init__.py
Name     GGPK User Interface Classes
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Creates a qt User Interface to browse GGPK files.


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
import hashlib

# 3rd aprty
from colorama import Fore

# self
from PyPoE.poe.file.ggpk import GGPKFile
from PyPoE.poe.path import PoEPath
from PyPoE.cli.config import SetupError
from PyPoE.cli.handler import BaseHandler
from PyPoE.cli.exporter import config
from PyPoE.cli.exporter.wiki.lua import QuestRewardReader

# =============================================================================
# Decorators
# =============================================================================

def check_hash(func):
    def wrapper(self, *args, **kwargs):
        if self._check_hash():
            return func(self, *args, **kwargs)
        else:
            print(Fore.LIGHTRED_EX + 'Game file hash mismatch. Please rerun setup.' + Fore.RESET)
            return -1
    return wrapper

# =============================================================================
# class
# =============================================================================

class WikiHandler(BaseHandler):
    LUA_OPTIONS = ('quest_rewards', 'vendor_rewards')

    def __init__(self, sub_parser):
        # Config Options
        config.add_option('temp_dir', 'is_directory(exists=True)')
        config.add_option('out_dir', 'is_directory(exists=True)')
        config.register_setup('temp_dir', self._setup)
        config.add_setup_variable('temp_dir', 'hash', 'string(default="")')
        config.add_setup_listener('version', self._ver_dist_changed)

        # Parser
        self.parser = sub_parser.add_parser('wiki', help='Wiki Exporter')
        self.parser.set_defaults(func=lambda args: self.parser.print_help())
        wiki_sub = self.parser.add_subparsers()

        lua = wiki_sub.add_parser('lua')
        lua.set_defaults(func=self.lua)
        lua.add_argument(
            '-d', '--outdir',
            help='Destination directory. If empty, uses current directory.'
        )
        lua.add_argument(
            '-t', '--type',
            action='append',
            choices=self.LUA_OPTIONS,
            help='Which file to export.'
        )
    def _ver_dist_changed(self, key, value, old_value):
        if value == old_value:
            return
        config.set_setup_variable('temp_dir', 'performed', False)

    def _get_content_ggpk_hash(self):
        ggpk = self._get_content_ggpk_path()
        with open(ggpk, 'rb') as f:
            data = f.read(2**16)

        return hashlib.md5(data).hexdigest()

    def _check_hash(self):
        hash_old = config.get_setup_variable('temp_dir', 'hash')
        hash_new = self._get_content_ggpk_hash()

        if hash_old == hash_new:
            return True

        config.set_setup_variable('temp_dir', 'performed', False)
        return False

    def _get_content_ggpk_path(self):
        args = config.get_option('version'), config.get_option('distributor')
        paths = PoEPath(*args).get_installation_paths()

        if not paths:
            raise SetupError('No PoE Installation found.')

        return os.path.join(paths[0], 'content.ggpk')

    def _setup(self, args):
        """
        :param args: argparse args passed on
        :return:
        """
        temp_dir = config.get_option('temp_dir', safe=False)

        content_ggpk = self._get_content_ggpk_path()

        print('Reading "%s"...' % content_ggpk)
        ggpk = GGPKFile(content_ggpk)
        ggpk.read()

        print('Building directory...')
        ggpk.directory_build()

        print('Extracting data files to "%s"...' % temp_dir)
        ggpk['Data'].extract_to(temp_dir)

        meta_dir = os.path.join(temp_dir, 'Metadata')
        print('Extracting description files to "%s"...' % meta_dir)
        nodes = ggpk['Metadata'].search('.*descriptions.*\.txt$', search_directories=False)
        if not os.path.exists(meta_dir):
            os.mkdir(meta_dir)
        for node in nodes:
            node.extract_to(meta_dir)

        print('Hashing...')

        hash = self._get_content_ggpk_hash()
        config.set_setup_variable('temp_dir', 'hash', hash)

        print('Done.')

    @check_hash
    def lua(self, args):
        opts = args.type if args.type is not None else self.LUA_OPTIONS
        out_dir = args.outdir if args.outdir is not None else config.get_option('out_dir')
        data_dir = os.path.join(config.get_option('temp_dir'), 'Data')

        for item in (out_dir, data_dir):
            if not os.path.exists(item):
                print('Path "%s" does not exist' % item)
                return -1

        print('Reading .dat files...')
        r = QuestRewardReader(data_path=data_dir)
        print('Done.\n')
        for item in opts:
            file_name = item + '.lua'
            print('Formatting for %s' % file_name)
            outfile = os.path.join(out_dir, file_name)
            getattr(r, 'read_' + item)(outfile)
            print('Wrote: %s\n' % file_name)

        print('Done.')
        return 0
