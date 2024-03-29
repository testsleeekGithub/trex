# -*- coding: utf-8 -*-
#
# Copyright © TRex Project Contributors
# Licensed under the terms of the MIT License
#

"""
Tests for the Numpy Matrix/Array Builder Widget.
"""

# Third party imports
from qtpy.QtCore import Qt
from pytestqt import qtbot
import pytest

# Local imports
from trex.widgets.arraybuilder import NumpyArrayDialog


# --- Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def botinline(qtbot):
    dialog = NumpyArrayDialog(inline=True)
    qtbot.addWidget(dialog)
    dialog.show()
    return qtbot, dialog, dialog.array_widget


@pytest.fixture
def botinlinefloat(qtbot):
    dialog = NumpyArrayDialog(inline=True, force_float=True)
    qtbot.addWidget(dialog)
    dialog.show()
    return qtbot, dialog, dialog.array_widget


@pytest.fixture
def botarray(qtbot):
    dialog = NumpyArrayDialog(inline=False)
    qtbot.addWidget(dialog)
    dialog.show()
    return qtbot, dialog, dialog.array_widget


# --- Tests
# -----------------------------------------------------------------------------
def test_array_inline_array(botinline):
    qtbot, dialog, widget = botinline
    qtbot.keyClicks(widget, '1 2 3  4 5 6')
    qtbot.keyPress(widget, Qt.Key_Return)
    value = dialog.text()
    assert value == 'np.array([[1, 2, 3],\n          [4, 5, 6]])'

def test_array_inline_matrix(botinline):
    qtbot, dialog, widget = botinline
    qtbot.keyClicks(widget, '4 5 6  7 8 9')
    qtbot.keyPress(widget, Qt.Key_Return, modifier=Qt.ControlModifier)
    value = dialog.text()
    assert value == 'np.matrix([[4, 5, 6],\n           [7, 8, 9]])'

def test_array_inline_array_invalid(botinline):
    qtbot, dialog, widget = botinline
    qtbot.keyClicks(widget, '1 2  3 4  5 6 7')
    qtbot.keyPress(widget, Qt.Key_Return)
    dialog.update_warning()
    assert not dialog.is_valid()

def test_array_inline_1d_array(botinline):
    qtbot, dialog, widget = botinline
    qtbot.keyClicks(widget, '4 5 6')
    qtbot.keyPress(widget, Qt.Key_Return, modifier=Qt.ControlModifier)
    value = dialog.text()
    assert value == 'np.matrix([4, 5, 6])'

def test_array_inline_nan_array(botinline):
    qtbot, dialog, widget = botinline
    qtbot.keyClicks(widget, '4 nan 6 8 9')
    qtbot.keyPress(widget, Qt.Key_Return, modifier=Qt.ControlModifier)
    value = dialog.text()
    assert value == 'np.matrix([4, np.nan, 6, 8, 9])'

def test_array_inline_force_float_array(botinlinefloat):
    qtbot, dialog, widget = botinlinefloat
    qtbot.keyClicks(widget, '4 5 6 8 9')
    qtbot.keyPress(widget, Qt.Key_Return, modifier=Qt.ControlModifier)
    value = dialog.text()
    assert value == 'np.matrix([4.0, 5.0, 6.0, 8.0, 9.0])'

def test_array_inline_force_float_error_array(botinlinefloat):
    qtbot, dialog, widget = botinlinefloat
    qtbot.keyClicks(widget, '4 5 6 a 9')
    qtbot.keyPress(widget, Qt.Key_Return, modifier=Qt.ControlModifier)
    value = dialog.text()
    assert value == 'np.matrix([4.0, 5.0, 6.0, a, 9.0])'

def test_array_table_array(botarray):
    qtbot, dialog, widget = botarray
    qtbot.keyClick(widget, Qt.Key_1)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_2)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_Backtab)  # Hack: in the tests the selected cell is wrong
    qtbot.keyClick(widget, Qt.Key_3)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_4)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_5)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_6)
    qtbot.keyClick(widget, Qt.Key_Tab)  # Hack: in the tests the selected cell is wrong
    qtbot.keyClick(widget, Qt.Key_Return, modifier=Qt.NoModifier)
    value = dialog.text()
    assert value == 'np.array([[1, 2, 3],\n          [4, 5, 6]])'

def test_array_table_matrix(botarray):  # analysis:ignore
    qtbot, dialog, widget = botarray
    qtbot.keyClick(widget, Qt.Key_1)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_2)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_Backtab)  # Hack: in the tests the selected cell is wrong
    qtbot.keyClick(widget, Qt.Key_3)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_4)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_5)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_6)
    qtbot.keyClick(widget, Qt.Key_Tab)  # Hack: in the tests the selected cell is wrong
    qtbot.keyClick(widget, Qt.Key_Return, modifier=Qt.ControlModifier)
    value = dialog.text()
    assert value == 'np.matrix([[1, 2, 3],\n           [4, 5, 6]])'

def test_array_table_array_empty_items(botarray):  # analysis:ignore
    qtbot, dialog, widget = botarray
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_2)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_Backtab)  # Hack: in the tests the selected cell is wrong
    qtbot.keyClick(widget, Qt.Key_3)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_5)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_6)
    qtbot.keyClick(widget, Qt.Key_Tab)  # Hack: in the tests the selected cell is wrong
    qtbot.keyClick(widget, Qt.Key_Return, modifier=Qt.NoModifier)
    value = dialog.text()
    assert value == 'np.array([[0, 2, 3],\n          [0, 5, 6]])'

def test_array_table_array_spaces_in_item(botarray):  # analysis:ignore
    qtbot, dialog, widget = botarray
    qtbot.keyClicks(widget, '   ')
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_2)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_Backtab)
    qtbot.keyClick(widget, Qt.Key_3)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_5)
    qtbot.keyClick(widget, Qt.Key_Tab)
    qtbot.keyClick(widget, Qt.Key_6)
    qtbot.keyClick(widget, Qt.Key_Tab)  # Hack: in the tests the selected cell is wrong
    qtbot.keyClick(widget, Qt.Key_Return, modifier=Qt.NoModifier)
    value = dialog.text()
    assert value == 'np.array([[0, 2, 3],\n          [0, 5, 6]])'

def test_array_table_matrix_empty(botarray):  # analysis:ignore
    qtbot, dialog, widget = botarray
    qtbot.keyClick(widget, Qt.Key_Return, modifier=Qt.NoModifier)
    value = dialog.text()
    assert value == ''
