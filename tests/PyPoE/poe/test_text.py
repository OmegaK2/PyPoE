"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/poe/test_text.py                                     |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Tests for PyPoE.poe.text

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
from functools import partial

# 3rd-party
import pytest

# self
from PyPoE.poe import text

# =============================================================================
# Setup
# =============================================================================


def sample_parser(**kwargs):
    if kwargs['parameter']:
        return '<%(id)s attr="%(parameter)s">%(hstr)s</%(id)s>' % kwargs
    else:
        return '<%(id)s>%(hstr)s</%(id)s>' % kwargs

# =============================================================================
# Fixtures
# =============================================================================

# =============================================================================
# Tests
# =============================================================================


class TestTags():
    sample_strings = [
        (
            'Basic',
            'Basic',
            [],
        ),
        # Basic functionality
        (
            'Test <item:20>{test} part 2 <item>{more test}',
            'Test <item attr="20">test</item> part 2 <item>more test</item>',
            ['item'],
        ),
        # nested values
        (
            '<bold>{<title>{<size:45>{test}}}',
            '<bold><title><size attr="45">test</size></title></bold>',
            ['bold', 'title', 'size'],
        ),
        (
            'Test <<TEST>>',
            'Test <<TEST>>',
            [],
        )
    ]

    @pytest.mark.parametrize('input,output,handler_ids', sample_strings)
    def test_parsing_results(self, input, output, handler_ids):
        handlers = {
            hid: partial(sample_parser, id=hid)
            for hid in handler_ids
        }

        tag = text.parse_description_tags(input)
        assert tag.handle_tags(handlers=handlers) == output