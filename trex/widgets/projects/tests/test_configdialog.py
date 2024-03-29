# -*- coding: utf-8 -*-
#
# Copyright © TRex Project Contributors
# Licensed under the terms of the MIT License
#

"""
Tests for configdialog.py
"""

# Standard librery imports
import os.path as osp
import tempfile

# Test library imports
import pytest

# Local imports
from trex.widgets.projects.configdialog import (EmptyProject,
                                                  ProjectPreferences)

@pytest.fixture
def setup_projects_preferences(qtbot):
    """Set up ProjectPreferences."""
    project_dir = tempfile.mkdtemp() + osp.sep + '.spyproject'
    project = EmptyProject(project_dir)
    project_preferences = ProjectPreferences(None, project)
    qtbot.addWidget(project_preferences)
    return (project, project_preferences)

def test_projects_preferences(qtbot):
    """Run Project Preferences."""
    project, preferences = setup_projects_preferences(qtbot)
    preferences.resize(250, 480)
    preferences.show()
    assert preferences


if __name__ == "__main__":
    pytest.main()
