# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License

"""
Tests for arrayeditor.py
"""

# Stdlib imports
import os

# Third party imports
import numpy as np
from numpy.testing import assert_array_equal
import pytest

# Local imports
from spyder.utils.qthelpers import qapplication
from spyder.widgets.variableexplorer.arrayeditor import ArrayEditor


def launch_arrayeditor(data, title="", xlabels=None, ylabels=None):
    """Helper routine to launch an arrayeditor and return its result"""
    dlg = ArrayEditor()
    assert dlg.setup_and_check(data, title, xlabels=xlabels, ylabels=ylabels)
    dlg.show()
    dlg.accept()  # trigger slot connected to OK button
    return dlg.get_value()


# --- Tests
# -----------------------------------------------------------------------------
def test_arrayeditor_with_string_array(qtbot):
    arr = np.array(["kjrekrjkejr"])
    assert arr == launch_arrayeditor(arr, "string array")


def test_arrayeditor_with_unicode_array(qtbot):
    arr = np.array([u"ñññéáíó"])
    assert arr == launch_arrayeditor(arr, "unicode array")


def test_arrayeditor_with_masked_array(qtbot):
    arr = np.ma.array([[1, 0], [1, 0]], mask=[[True, False], [False, False]])
    assert_array_equal(arr, launch_arrayeditor(arr, "masked array"))


def test_arrayeditor_with_record_array(qtbot):
    arr = np.zeros((2, 2), {'names': ('red', 'green', 'blue'),
                           'formats': (np.float32, np.float32, np.float32)})
    assert_array_equal(arr, launch_arrayeditor(arr, "record array"))


@pytest.mark.skipif(not os.name == 'nt', reason="It segfaults sometimes on Linux")
def test_arrayeditor_with_record_array_with_titles(qtbot):
    arr = np.array([(0, 0.0), (0, 0.0), (0, 0.0)],
                   dtype=[(('title 1', 'x'), '|i1'),
                          (('title 2', 'y'), '>f4')])
    assert_array_equal(arr, launch_arrayeditor(arr, "record array with titles"))


def test_arrayeditor_with_float_array(qtbot):
    arr = np.random.rand(5, 5)
    assert_array_equal(arr, launch_arrayeditor(arr, "float array",
                                      xlabels=['a', 'b', 'c', 'd', 'e']))


def test_arrayeditor_with_complex_array(qtbot):
    arr = np.round(np.random.rand(5, 5)*10)+\
                   np.round(np.random.rand(5, 5)*10)*1j
    assert_array_equal(arr, launch_arrayeditor(arr, "complex array",
                                      xlabels=np.linspace(-12, 12, 5),
                                      ylabels=np.linspace(-12, 12, 5)))


def test_arrayeditor_with_bool_array(qtbot):
    arr_in = np.array([True, False, True])
    arr_out = launch_arrayeditor(arr_in, "bool array")
    assert arr_in is arr_out

def test_arrayeditor_with_int8_array(qtbot):
    arr = np.array([1, 2, 3], dtype="int8")
    assert_array_equal(arr, launch_arrayeditor(arr, "int array"))


def test_arrayeditor_with_float16_array(qtbot):
    arr = np.zeros((5,5), dtype=np.float16)
    assert_array_equal(arr, launch_arrayeditor(arr, "float16 array"))


def test_arrayeditor_with_3d_array(qtbot):
    arr = np.zeros((3,3,4))
    arr[0,0,0]=1
    arr[0,0,1]=2
    arr[0,0,2]=3
    assert_array_equal(arr, launch_arrayeditor(arr, "3D array"))


if __name__ == "__main__":
    pytest.main()

