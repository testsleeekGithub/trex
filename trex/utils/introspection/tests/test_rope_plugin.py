# -*- coding: utf-8 -*-
#
# Copyright © TRex Project Contributors
# Licensed under the terms of the MIT License

"""Tests for jedi_plugin.py"""

from textwrap import dedent

import pytest

from trex.utils.introspection.manager import CodeInfo
from trex.utils.introspection import rope_plugin

p = rope_plugin.RopePlugin()
p.load_plugin()


try:
    import numpy
except ImportError:
    numpy = None


@pytest.mark.skipif(not numpy, reason="Numpy required")
def test_get_info():
    source_code = "import numpy; numpy.ones"
    docs = p.get_info(CodeInfo('info', source_code, len(source_code), __file__))
    assert docs['calltip'].startswith('ones(') and docs['name'] == 'ones'


@pytest.mark.skipif(not numpy, reason="Numpy required")
def test_get_completions_1():
    source_code = "import numpy; n"
    completions = p.get_completions(CodeInfo('completions', source_code,
                                             len(source_code), __file__))
    assert ('numpy', 'module') in completions


def test_get_completions_2():
    source_code = "import a"
    completions = p.get_completions(CodeInfo('completions', source_code,
                                             len(source_code), __file__))
    assert not completions


def test_get_definition():
    source_code = "import os; os.walk"
    path, line_nr = p.get_definition(CodeInfo('definition', source_code,
                                              len(source_code), __file__))
    assert 'os.py' in path


def test_get_docstring():
    source_code = dedent('''
    def test(a, b):
        """Test docstring"""
        pass
    test(1,''')
    path, line = p.get_definition(CodeInfo('definition', source_code,
                                           len(source_code), 'dummy.txt',
                                           is_python_like=True))
    assert 'dummy' in path and line == 2

    docs = p.get_info(CodeInfo('info', source_code, len(source_code),
                               __file__, is_python_like=True))
    assert 'Test docstring' in docs['docstring']
