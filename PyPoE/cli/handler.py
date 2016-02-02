"""
Generic Console Handlers

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/handler.py                                             |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Generic console handlers

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import traceback

# 3rd Party
from validate import ValidateError

# self
from PyPoE.cli.config import ConfigError
from PyPoE.cli.core import console, Msg

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'BaseHandler', 'ConfigHandler', 'SetupHandler',
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
        console(e)
        return -1

    def print_sep(self, char='-'):
        console(char*70)

class ConfigHandler(BaseHandler):
    def __init__(self, sub_parser, config):
        # Config
        self.config = config
        if not self.config.validate(config.validator):
            raise ConfigError('Config validation failed.')

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
        console(str(self.config))
        return 0

    def print_all(self, args):
        spec = set(self.config.optionspec.keys())
        real = set(self.config.option.keys())


        missing = spec.difference(real)
        extra = real.difference(spec)
        configured = spec.difference(missing)


        console('Current stored config variables:')
        for key in sorted(list(configured)):
            console("%s: %s" % (key, self.config.option[key]))

        if missing:
            console('\nMissing config variables (require config set):', msg=Msg.error)
            for key in sorted(list(missing)):
                console("%s" % (key, ), Msg.error)

        if extra:
            console('\nExtra variables (unused):', msg=Msg.warning)
            for key in sorted(list(extra)):
                console("%s: %s" % (key, self.config.option[key]), msg=Msg.warning)

        return 0

    def get(self, args):
        console('Config setting "%s" is currently set to:\n%s' % (args.variable, self.config.option[args.variable]))
        return 0

    def set(self, args):
        try:
            self.config.set_option(args.variable, args.value)
        except ValidateError as e:
            return self._show_error(e)
        self.config.write()

        console('Config setting "%s" has been set to:\n%s' % (args.variable, args.value))

        if self.config.needs_setup(args.variable) and not self.config.is_setup(args.variable):
            console('\nVariable needs setup. Please run:\nsetup perform')

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
        console('Performing setup. This may take a while - please wait...')
        self.print_sep()
        for key in self.config['Setup']:
            section = self.config['Setup'][key]
            if section['performed']:
                continue
            console('Performing setup for: %s' % key)
            try:
                for func in section.functions:
                    func(args)
            except Exception as e:
                console('Unexpected error occured during setup:\n')
                console(traceback.format_exc(), msg=Msg.error)
                continue
            self.config['Setup'][key]['performed'] = True
            self.print_sep()
        self.config.write()
        console('Done.')