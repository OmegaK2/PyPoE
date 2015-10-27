"""
pywikibot Setup

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/pywikibot_setup.py                            |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Setups up the path of exile family and a few other things to be able to use
pywikibot.

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
import sys

# self
from PyPoE import __version__

# =============================================================================
# Pywikibot loading
# =============================================================================
# Unfortunately have to be a bit hacky here due to the way pywikibot works...
#

# Disable pywikibot's userconfig; we'll only be operating on the Path of Exile
# wiki
os.environ['PYWIKIBOT2_NO_USER_CONFIG'] = '1'

# Suppress stdout
_old_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')

# Attempt to import
try:
    import pywikibot
finally:
    # Make sure to restore the stdout in case the import fails
    sys.stdout = _old_stdout

# =============================================================================
# Globals
# =============================================================================

pywikibot.config.put_throttle = 1

__all__ = ['pywikibot', 'get_site', 'get_edit_message']

# =============================================================================
# Classes
# =============================================================================

class PoEFamily(pywikibot.family.Family):
    def __init__(self):
        pywikibot.family.Family.__init__(self)
        self.name = 'pathofexile'
        self.langs = {
            'en': 'pathofexile.gamepedia.com',
        }

    def scriptpath(self, code):
        return {
            'en': '',
        }[code]

    def protocol(self, code):
        return {
            'en': u'http',
        }[code]

# =============================================================================
# Functions
# =============================================================================

def get_site():
    return pywikibot.Site(code='en', fam=PoEFamily(), user=input('Enter username:\n'))

def get_edit_message(msg=''):
    return 'PyPoE/ExporterBot/%s: %s' % (__version__, msg)