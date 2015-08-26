"""
Path     PyPoE/cli/exporter/wiki/parser/__init__.py
Name     Parser package init
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Automatically all ExporterHandlers in the package files and import them into
WIKI_HANDLERS.


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
from importlib import import_module

# self
from PyPoE.cli.exporter.wiki.handler import ExporterHandler


# =============================================================================
# Globals
# =============================================================================


WIKI_HANDLERS = []

__all__ = ['WIKI_HANDLERS']


# =============================================================================
# Funcs
# =============================================================================


def _load():
    cur_dir = os.path.split(os.path.realpath(__file__))[0]
    for file_name in os.listdir(cur_dir):
        if file_name.startswith('_'):
            continue
        file_name = file_name.replace('.py', '')
        imp = import_module('.' + file_name, __package__)
        for obj_name in dir(imp):
            if obj_name.startswith('_'):
                continue

            if not obj_name.endswith('Handler'):
                continue

            obj = getattr(imp, obj_name)

            # Not a class
            if not isinstance(obj, type):
                continue

            # Only export handlers
            if not issubclass(obj, ExporterHandler):
                continue

            # Only subclasses of which
            if obj is ExporterHandler:
                continue

            WIKI_HANDLERS.append(obj)


# =============================================================================
# Init
# =============================================================================


_load()