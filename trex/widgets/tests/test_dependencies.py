# -*- coding: utf-8 -*-
#
# Copyright © TRex Project Contributors
# Licensed under the terms of the MIT License
#

"""
Tests for dependencies.py
"""

# Test library imports
import pytest

# Local imports
from trex.widgets.dependencies import DependenciesDialog
from trex import dependencies

@pytest.fixture
def setup_dependencies(qtbot):
    """Set up dependency widget test."""
    widget = DependenciesDialog(None)
    qtbot.addWidget(widget)
    return widget

def test_dependencies(qtbot):
    """Run dependency widget test."""
    # Test sample
    dependencies.add("IPython", "Enhanced Python interpreter", ">=0.13")
    dependencies.add("foo", "Non-existent module", ">=1.0")

    dlg = setup_dependencies(qtbot)
    dlg.set_data(dependencies.DEPENDENCIES)
    dlg.show()    
    assert dlg


if __name__ == "__main__":
    pytest.main()
