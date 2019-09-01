# -*- coding: utf-8 -*-
#
# Copyright © TRex Project Contributors
# Licensed under the terms of the MIT License
# (see trex/__init__.py for details)

import os
import re
import codecs

import pytest

root_path = os.path.realpath(os.path.join(os.getcwd(), 'trex'))


@pytest.mark.parametrize("pattern,exclude_patterns,message", [
    ("isinstance\(.*,.*str\)", ['py3compat.py'],
     ("Don't use builtin isinstance() function,"
      "use trex.py3compat.is_text_string() instead")),

    (r"^[\s\#]*\bprint\(((?!file=).)*\)", ['.*test.*', 'example.py', 'binaryornot'],
     ("Don't use print() functions, ",
      "for debuging you could use debug_print instead")),

    (r"^[\s\#]*\bprint\s+(?!>>)((?!#).)*", ['.*test.*'],
     ("Don't use print __builtin__, ",
      "for debuging you could use debug_print instead")),
])
def test_dont_use(pattern, exclude_patterns, message):
    """
    This test is used for discouraged using of some expresions that could
    introduce errors, and encourage use trex function instead.

    If you want to skip some line from this test just use:
        # trex: test-skip
    """
    pattern = re.compile(pattern + "((?!# trex: test-skip)\s)*$")

    found = 0
    for dir_name, _, file_list in os.walk(root_path):
        for fname in file_list:
            exclude = any([re.search(ex, fname) for ex in exclude_patterns])
            exclude = exclude or any([re.search(ex, dir_name) for ex in exclude_patterns])

            if fname.endswith('.py') and not exclude:
                file = os.path.join(dir_name, fname)

                with codecs.open(file, encoding="utf-8") as f:
                    for i, line in enumerate(f):
                        for match in re.finditer(pattern, line):
                            print("{}\nline:{}, {}".format(file, i + 1, line))
                            found += 1

    assert found == 0, "{}\n{} errors found".format(message, found)
