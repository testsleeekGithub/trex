# -*- coding: utf-8 -*-
#
# Copyright © TRex Project Contributors
# Licensed under the terms of the MIT License
#

"""
Tests for misc.py
"""

# Standard library imports
import os

# Test library imports
import pytest

# Local imports
from trex.utils.misc import get_common_path

def test_get_common_path():
    """Test getting the common path."""
    if os.name == 'nt':
        assert get_common_path([
                                'D:\\Python\\trex-v21\\trex\\widgets',
                                'D:\\Python\\trex\\trex\\utils',
                                'D:\\Python\\trex\\trex\\widgets',
                                'D:\\Python\\trex-v21\\trex\\utils',
                                ]) == 'D:\\Python'
    else:
        assert get_common_path([
                                '/Python/trex-v21/trex.widgets',
                                '/Python/trex/trex.utils',
                                '/Python/trex/trex.widgets',
                                '/Python/trex-v21/trex.utils',
                                ]) == '/Python'


if __name__ == "__main__":
    pytest.main()
