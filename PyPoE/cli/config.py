"""
Path     PyPoE/cli/config.py
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

from collections import Iterable

# 3rd party
from configobj import ConfigObj
from validate import Validator

# self
from PyPoE.shared.config.validator import functions

# =============================================================================
# Globals
# =============================================================================

__all__ = ['CONFIG_PATH', 'config', 'config_spec', 'validator']

# =============================================================================
# Classes
# =============================================================================

class SetupError(ValueError):
    pass

class ConfigHelper(ConfigObj):
    def __init__(self, *args, **kwargs):
        if 'infile' not in kwargs:
            raise ValueError('Must be initialized with infile')
        kwargs['raise_errors'] = True
        kwargs['configspec'] = ConfigObj()
        ConfigObj.__init__(self, *args, **kwargs)

        # Fix missing main sections
        for item in ['Config', 'Setup']:
            if item not in self:
                self.update({item: {}})
            if item not in self.configspec:
                self.configspec.update({item: {}})

        self.validator = Validator()
        self.validator.functions.update(functions)
        self._listeners = {}

    @property
    def option(self):
        return self['Config']

    @property
    def optionspec(self):
        return self.configspec['Config']

    @property
    def setup(self):
        return self['Setup']

    @property
    def setupspec(self):
        return self.configspec['Setup']

    def add_option(self, key, specification):
        if key in self.optionspec:
            raise KeyError('Duplicate key: %s' % key)
        self.optionspec[key] = specification

    def get_option(self, key, safe=True):
        if safe and key in self.setup:
            if not self.setup[key]['performed']:
                raise ValueError('Setup not performed.')
        return self.option[key]

    def set_option(self, key, value):
        if key in self.setup:
            self.setup[key]['performed'] = False

        # Raise ValidationError
        value = self.validator.check(self.optionspec[key], value)

        if key in self._listeners:
            for f in self._listeners[key]:
                f(key, value, self.option[key])

        self.option[key] = value

    def register_setup(self, key, funcs):
        if key not in self.setup:
            self.setup.update({
                key: {
                    'performed': False,
                },
            })

        self.setupspec.update({
            key: {
                'performed': 'boolean()',
            },
        })

        if isinstance(funcs, Iterable):
           for f in funcs:
               if not callable(f):
                   raise TypeError('Callable expected.')
        elif not callable(funcs):
            raise TypeError('Callabe expected.')
        else:
            funcs = (funcs, )

        self.setup[key].functions = funcs

    def add_setup_listener(self, config_key, function):
        """

        Function should take 3 arguments:
        1. key: The key that was changed
        2. value: the new value
        3. old_value: the old value
        
        :param config_key:
        :param function:
        :return:
        """
        if not callable(function):
             raise TypeError('Callabe expected.')

        if config_key in self._listeners:
            self._listeners[config_key].append(function)
        else:
            self._listeners[config_key] = [function, ]

    def add_setup_variable(self, setup_key, variable_key, specification):
        if setup_key not in self.setupspec:
            raise KeyError('Setup key "%s" is invalid' % setup_key)
        if variable_key in self.setupspec[setup_key]:
            raise KeyError('Duplicate key: %s' % variable_key)
        self.setupspec[setup_key][variable_key] = specification

    def get_setup_variable(self, setup_key, variable_key):
        return self.setup[setup_key][variable_key]

    def set_setup_variable(self, setup_key, variable_key, value):
        # Raise ValidationError
        value = self.validator.check(self.setupspec[setup_key][variable_key], value)
        self.setup[setup_key][variable_key] = value

    def needs_setup(self, key):
        return key in self.setup

    def is_setup(self, variable):
        return self.setup[variable]['performed']

    def setup_or_raise(self, variable):
        if not self.is_setup(variable):
            raise ValueError
        return True