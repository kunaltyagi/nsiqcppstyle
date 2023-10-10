# Copyright (c) 2022 All rights reserved.
# SPDX-License-Identifier: GPL-2.0-only
# File: trace-callbacks.py
# Purpose: Trace every N'Siq CppStyle callback for one or more given input source
#          files.  Using the trace, the rule developer can plan how to write a new rule.
import os
import subprocess
import sys

if len(sys.argv) == 1:
    print("Error: Provide one or more source file paths for analysis")
    print("")
    print('Example: python trace-callbacks.py "c:\\test\\a.cpp"')
    print('Example: python trace-callbacks.py "c:\\test\\a.cpp" "d:\\src\\b.cpp"')
    sys.exit(0)

argument_list = [
    sys.executable,
    "nsiqcppstyle.py",
    '--filter-string="~ TOOL_trace_nsiqcppstyle_callbacks"',
    "-o",
    os.devnull,
]
argument_list.extend(sys.argv[1:])
subprocess.run(argument_list)
