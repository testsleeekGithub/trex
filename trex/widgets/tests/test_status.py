# -*- coding: utf-8 -*-
#
# Copyright © TRex Project Contributors
# Licensed under the terms of the MIT License
#

"""
Tests for status.py
"""

# Test library imports
import pytest

# Thrid party imports
from qtpy.QtWidgets import QMainWindow

# Local imports
from trex.widgets.status import (ReadWriteStatus, EOLStatus, EncodingStatus,
                                   CursorPositionStatus, MemoryStatus,
                                   CPUStatus)

@pytest.fixture
def setup_status_bar(qtbot):
    """Set up StatusBarWidget."""
    win = QMainWindow()
    win.setWindowTitle("Status widgets test")
    win.resize(900, 300)
    statusbar = win.statusBar()
    qtbot.addWidget(win)
    return (win, statusbar)

def test_status_bar(qtbot):
    """Run StatusBarWidget."""
    win, statusbar = setup_status_bar(qtbot)
    swidgets = []
    for klass in (ReadWriteStatus, EOLStatus, EncodingStatus,
                  CursorPositionStatus, MemoryStatus, CPUStatus):
        swidget = klass(win, statusbar)
        swidgets.append(swidget)
    assert win
    assert len(swidgets) == 6


if __name__ == "__main__":
    pytest.main()
