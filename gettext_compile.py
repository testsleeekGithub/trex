# -*- coding: utf-8 -*-
#
# Copyright © TRex Project Contributors
# Licensed under the terms of the MIT License
# (see trex/__init__.py for details)

from gettext_helpers import do_compile

if __name__ == "__main__":
    do_compile("trex")
    do_compile("pylint", "trex_pylint")
    do_compile("profiler", "trex_profiler")
    do_compile("breakpoints", "trex_breakpoints")
