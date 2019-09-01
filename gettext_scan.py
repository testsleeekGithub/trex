# -*- coding: utf-8 -*-
#
# Copyright © TRex Project Contributors
# Licensed under the terms of the MIT License
# (see trex/__init__.py for details)

from gettext_helpers import do_rescan, do_rescan_files

if __name__ == "__main__":
    do_rescan("trex")
    do_rescan_files(["trex_pylint/pylint.py",
                     "trex_pylint/widgets/pylintgui.py"],
                     "pylint", "trex_pylint")
    do_rescan_files(["trex_profiler/profiler.py",
                     "trex_profiler/widgets/profilergui.py"],
                     "profiler", "trex_profiler")
    do_rescan_files(["trex_breakpoints/breakpoints.py",
                     "trex_breakpoints/widgets/breakpointsgui.py"],
                     "breakpoints", "trex_breakpoints")
