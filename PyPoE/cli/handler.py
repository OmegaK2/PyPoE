"""
Path     PyPoE/cli/handler.py
Name     Generic Console Handlers
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Generic console handlers


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import traceback

# 3rd Party
from colorama import Fore
from validate import ValidateError

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'BaseHandler', 'ConfigHandler',
]

# =============================================================================
# Classes
# =============================================================================

class BaseHandler(object):
    def __init__(self, sub_parser):
        raise NotImplemented

    def _help(self, *args):
        self.parser.print_help()
        return 0

    def _show_error(self, e):
        print(e)
        return -1

    def print_sep(self, char='-'):
        print(char*70)

class ConfigHandler(BaseHandler):
    def __init__(self, sub_parser, config):
        # Config
        self.config = config
        if not self.config.validate(config.validator):
            raise ValueError('Config validation failed')

        # Parsing stuff
        self.parser = sub_parser.add_parser('config', help='Edit config options')
        self.parser.set_defaults(func=self._help)
        config_sub = self.parser.add_subparsers()

        print_debug_parser = config_sub.add_parser(
            'print_debug',
            help='Prints out all registered and internal options for debugging.'
        )
        print_debug_parser.set_defaults(func=self.print_debug)

        print_all_parser = config_sub.add_parser(
            'print_all',
            help='Prints out all registered config options'
        )
        print_all_parser.set_defaults(func=self.print_all)

        get_parser = config_sub.add_parser('get', help='Get config option')
        get_parser.set_defaults(func=self.get)
        get_parser.add_argument(
            'variable',
            choices=config.optionspec.keys(),
            help='Variable to set',
        )

        set_parser = config_sub.add_parser('set', help='Set config option')
        set_parser.set_defaults(func=self.set)
        set_parser.add_argument(
            'variable',
            choices=config.optionspec.keys(),
            help='Variable to set',
        )
        set_parser.add_argument(
            'value',
            action='store',
            help='Value to set',
        )
    def print_debug(self, args):
        print(self.config)
        return 0

    def print_all(self, args):
        spec = self.config.optionspec.keys()

        print ('Current stored config variables:')
        for key in list(spec):
            print("%s: %s" % (key, self.config.option[key]))

        real = set(self.config.option.keys())
        diff = list(real.difference(set(spec))).sort()
        if diff:
            print('Extra variables:')
            for key in diff:
                print("%s: %s" % (key, self.config.option[key]))

        return 0

    def get(self, args):
        print('Config setting "%s" is currently set to:\n%s' % (args.variable, self.config.option[args.variable]))
        return 0

    def set(self, args):
        try:
            self.config.set_option(args.variable, args.value)
        except ValidateError as e:
            return self._show_error(e)
        self.config.write()

        print('Config setting "%s" has been set to:\n%s' % (args.variable, args.value))

        if self.config.needs_setup(args.variable) and not self.config.is_setup(args.variable):
            print('\nVariable needs setup. Please run:\nsetup perform')

        return 0


class SetupHandler(BaseHandler):
    def __init__(self, sub_parser, config):
        self.config = config
        self.parser = sub_parser.add_parser('setup', help='CLI Interface Setup')
        self.parser.set_defaults(func=self._help)

        setup_sub = self.parser.add_subparsers()

        setup_perform = setup_sub.add_parser(
            'perform',
            help='Perform setup'
        )
        setup_perform.set_defaults(func=self.setup)

    def setup(self, args):
        print('Performing setup. This may take a while - please wait...')
        self.print_sep()
        for key in self.config['Setup']:
            section = self.config['Setup'][key]
            if section['performed']:
                continue
            print('Performing setup for: %s' % key)
            try:
                for func in section.functions:
                    func(args)
            except Exception as e:
                print('Unexpected error occured during setup:\n')
                print(Fore.LIGHTRED_EX + traceback.format_exc() + Fore.RESET)
                continue
            self.config['Setup'][key]['performed'] = True
            self.print_sep()
        self.config.write()
        print('Done.')