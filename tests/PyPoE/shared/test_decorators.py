"""
Tests for PyPoE.shared.decorators

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/shared/test_decorators.py                            |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================



Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import sys

# 3rd-party
import pytest

# self
from PyPoE.shared import decorators

# =============================================================================
# Utility functions
# =============================================================================

def make_test_list(stuff):
    parsed_data = []
    for decorator, kwargs in stuff:
        row = []
        if kwargs is None:
            row.append(decorator)
        else:
            row.append(decorator(**kwargs))

        parsed_data.append(row)


# =============================================================================
# Setup
# =============================================================================


def make_objects(uncallables=False):
    def function(*args, **kwargs):
        pass
    
    class A:
        """A"""
        def __call__(self, *args, **kwargs):
            """__call__"""
            pass
    
        def method(self, *args, **kwargs):
            """method"""
            pass
    
        @classmethod
        def classmethod(cls, *args, **kwargs):
            """classmethod"""
            pass

    data = [
        # callable object, instance object
        (function, None),
        (A.classmethod, None),
        (A.method, A),
        (A.__call__, A),
    ]

    if uncallables:
        data.append((A, None))

    return data

# =============================================================================
# Tests
# =============================================================================


class TestDeprecated:
    def run_test(self, decorator, callobj, obj):
        with pytest.warns(DeprecationWarning) as record:
            o = decorator(callobj)
            args = (1, 2, 3)
            kwargs = {'a': 1, 'b': 2, 'c': 3}
            if obj:
                o(obj(), *args, **kwargs)
            else:
                o(*args, **kwargs)
            return record

    @pytest.mark.parametrize('callobj,obj', make_objects())
    def test_simple(self, callobj, obj):
        self.run_test(decorators.deprecated, callobj, obj)

    @pytest.mark.parametrize('callobj,obj', make_objects())
    def test_empty_args(self, callobj, obj):
        self.run_test(decorators.deprecated(), callobj, obj)

    @pytest.mark.parametrize('callobj,obj', make_objects())
    def test_message_arg(self, callobj, obj):
        deco = decorators.deprecated(message='Test')

        for warn in self.run_test(deco, callobj, obj):
            assert warn.message.args[0] == 'Test'

    @pytest.mark.parametrize('callobj,obj', make_objects())
    def test_message_arg(self, callobj, obj):
        deco = decorators.deprecated(doc_message='Test')

        self.run_test(deco, callobj, obj)
        assert callobj.__doc__.startswith('Test')


class TestDoc:
    """Test"""

    @pytest.mark.parametrize('callobj,obj', make_objects(True))
    def test_simple(self, callobj, obj):
        o = decorators.doc(callobj)

    @pytest.mark.parametrize('callobj,obj', make_objects(True))
    def test_empty_args(self, callobj, obj):
        o = decorators.doc()(callobj)

    @pytest.mark.parametrize('callobj,obj', make_objects(True))
    def test_arg_prepend(self, callobj, obj):
        o = decorators.doc(prepend='Test')(callobj)

        assert o.__doc__.startswith('Test')

    @pytest.mark.parametrize('callobj,obj', make_objects(True))
    def test_arg_append(self, callobj, obj):
        o = decorators.doc(append='Test')(callobj)

        assert o.__doc__.endswith('Test')

    @pytest.mark.parametrize('callobj,obj', make_objects(True))
    def test_arg_doc_with_str(self, callobj, obj):
        o = decorators.doc(doc='Test')(callobj)

        assert o.__doc__ == 'Test'

    @pytest.mark.parametrize('callobj,obj', make_objects(True))
    def test_arg_doc_with_obj(self, callobj, obj):
        o = decorators.doc(doc=TestDoc)(callobj)

        assert o.__doc__ == 'Test'