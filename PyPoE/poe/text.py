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
from typing import Callable, Dict, Union, List

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
    id
        identifier string of the tag
    parent
        parent Tag instance if any
    children
        list of child strings or tag instances
    parameter
        parameter specified in the text to this tag if any

    """
    __slots__ = ['id', 'parent', 'parameter', 'children']

    _REPR_ARGUMENTS_IGNORE = {'parent'}

    def __init__(self,
                 id: Union[str, None] = None,
                 parent: Union['Tag', None] = None,
                 children: Union[List[Union[str, 'Tag']], None] = None,
                 parameter: Union[str, None] = None):
        """
        Parameters
        ----------
        id
            identifier string of the tag
        parent
            parent Tag instance if any
        children
            list of child strings or tag instances
        parameter
            parameter specified in the text to this tag if any
        """
        self.id: Union[str, None] = id
        self.parent: Union['Tag', None] = parent
        self.parameter: Union[str, None] = parameter
        if children is None:
            self.children: List[Union[str, 'Tag']] = []

    def append_to_children(self, text: str):
        """
        Appends a given text to the children attribute

        Parameters
        ----------
        text
            Text to append to the children
        """
        if self.children:
            if isinstance(self.children[-1], Tag):
                self.children.append(text)
            else:
                self.children[-1] += text
        else:
            self.children.append(text)

    def root(self) -> 'Tag':
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

    def handle_tags(self, handlers: Dict[str, Callable]) -> str:
        """
        Handle this and child tags with the handlers passed to this function.

        Parameters
        ----------
        handlers
            Dictionary containing a mapping of handler ids to callables that
            handle them.

            The callable will be passed two keyword parameters:
                hstr - the current contained string for the parameter to handle
                parameter - any parameters passed to the tag (may be None)

        Returns
        -------
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


def parse_description_tags(text: str) -> Tag:
    """
    Parses a text containing description tags into :class:`Tag` classes which
    can be used for further handling.

    Parameters
    ----------
    text
        The text to parse

    Returns
    -------
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
    has_tag = [False]
    parameter = [False]
    depth = 0
    out = Tag(id=None)
    last = out

    for tid, match, text in scanner.scan(text)[0]:
        if tid == 'lt':
            depth += 1
            in_tag.append(True)
            has_tag.append(True)
            parameter.append(False)
        elif tid == 'gt':
            in_tag[depth] = False
            parameter[depth] = False
        elif tid == 'lbrace':
            if has_tag[depth]:
                in_text.append(True)
            else:
                last.append_to_children(text)
        elif tid == 'rbrace':
            if has_tag[depth]:
                del in_tag[depth]
                del in_text[depth]
                del parameter[depth]
                del has_tag[depth]
                last = last.parent
                depth -= 1
            else:
                last.append_to_children(text)
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
                last.append_to_children(text)

    return out