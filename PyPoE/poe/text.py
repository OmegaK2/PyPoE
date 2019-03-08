"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/text.py                                                |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Utilities for dealing with certain text/string related tasks in regards to PoE.

Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

.. autoclass:: Tag

.. autofunction:: parse_description_tags
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
from functools import partial

# 3rd-party

# self
from PyPoE.shared.mixins import ReprMixin

# =============================================================================
# Globals
# =============================================================================

__all__ = ['Tag', 'parse_description_tags']

# =============================================================================
# Classes
# =============================================================================


class Tag(ReprMixin):
    """
    Represents a tag in PoE texts.

    For example:
        <size:45>{I have <item>{My item} for sale}

        tag.id = 'size'
        tag.parent = None
        tag.children = ['I have ', <Tag object>, ' for sale']
        tag.parameter = '45'

    Parameters
    ----------
    id : str
        identifier string of the tag
    parent : tag
        parent Tag instance if any
    children : list[str or Tag]
        list of child strings or tag instances
    parameter : str
        parameter specified in the text to this tag if any

    """
    __slots__ = ['id', 'parent', 'parameter', 'children']

    _REPR_ARGUMENTS_IGNORE = {'parent'}

    def __init__(self, id=None, parent=None, children=None, parameter=None):
        """
        Parameters
        ----------
        id : str
            identifier string of the tag
        parent : tag
            parent Tag instance if any
        children : list[str or Tag]
            list of child strings or tag instances
        parameter : str
            parameter specified in the text to this tag if any
        """
        self.id = id
        self.parent = parent
        self.parameter = parameter
        if children is None:
            self.children = []

    def root(self):
        """
        Returns the root Tag node

        Returns
        -------
        Tag
            root node
        """
        parent = self.parent
        while parent:
            parent = self.parent

        return parent

    def handle_tags(self, handlers):
        """
        Handle this and child tags with the handlers passed to this function.

        Parameters
        ----------
        handlers : dict[str, callable]
            Dictionary containing a mapping of handler ids to callables that
            handle them.

            The callable will be passed two keyword parameters:
                hstr - the current contained string for the parameter to handle
                parameter - any parameters passed to the tag (may be None)

        Returns
        -------
        str
            The handled string

        Raises
        ------
        KeyError
            if a id is not present in the handlers parameter
        """
        out_str = ''.join([
            item.handle_tags(handlers=handlers) if isinstance(item, Tag)
            else item for item in self.children
        ])
        if self.id is None:
            return out_str
        else:
            return handlers[self.id](hstr=out_str, parameter=self.parameter)

# =============================================================================
# Functions
# =============================================================================


def parse_description_tags(text):
    """
    Parses a text containing description tags into :class:`Tag` classes which
    can be used for further handling.

    Parameters
    ----------
    text : str
        The text to parse

    Returns
    -------
    Tag
        the parsed text as Tag class (with no id)
    """
    def f(scanner, result, tid):
        return tid, scanner.match, result

    scanner = re.Scanner([
        (r'(?<!<)<(?!<)', partial(f, tid='lt')),
        (r'(?<!>)>(?!>)', partial(f, tid='gt')),
        (r'\{', partial(f, tid='lbrace')),
        (r'\}', partial(f, tid='rbrace')),
        (r':', partial(f, tid='colon')),
        (r'[^<>\{\}:]+', partial(f, tid='text')),
        # Harbinger stuff
        (r'<<[^<>\{\}:]+>>', partial(f, tid='text')),

    ], re.UNICODE | re.MULTILINE)

    in_tag = [False]
    in_text = [True]
    parameter = [False]
    depth = 0
    out = Tag(id=None)
    last = out

    for tid, match, text in scanner.scan(text)[0]:
        if tid == 'lt':
            depth += 1
            in_tag.append(True)
            parameter.append(False)
        elif tid == 'gt':
            in_tag[depth] = False
            parameter[depth] = False
        elif tid == 'lbrace':
            in_text.append(True)
        elif tid == 'rbrace':
            del in_tag[depth]
            del in_text[depth]
            del parameter[depth]
            last = last.parent
            depth -= 1
        elif tid == 'colon':
            if in_tag[depth]:
                parameter[depth] = True
            else:
                last.children[-1] += text
        elif tid == 'text':
            if in_tag[depth]:
                if parameter[depth]:
                    last.parameter = text
                else:
                    tag = Tag(id=text, parent=last)
                    last.children.append(tag)
                    last = tag
            else:
                if last.children:
                    if isinstance(last.children[-1], Tag):
                        last.children.append(text)
                    else:
                        last.children[-1] += text
                else:
                    last.children.append(text)

    return out