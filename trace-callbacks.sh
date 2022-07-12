# Copyright (c) 2022 All rights reserved.
# SPDX-License-Identifier: GPL-2.0-only
# File: trace-callbacks.sh
# Purpose: Trace every N'Siq CppStyle callback for a given input source file.  Using
#          the trace, the rule developer can plan how to write a new rule.

FILEFILTER=filefilter.trace-callbacks.txt

usage () {
    echo "USAGE: trace-callbacks.sh path-to-source-file"
}

delete_filefilter () {
    rm $FILEFILTER
}

if [ $# -eq 0 ]; then
    echo "No file path argument provided"
    usage
    exit 1
fi

if ! [[ "$(python3 -V)" =~ "Python 3" ]]; then
    echo "python3 not found"
    exit 2
fi

delete_filterfilter

echo "~ TOOL_trace_nsiqcppstyle_callbacks" > filefilter.trace-callbacks.txt

python3 nsiqcppstyle.py -f filefilter.trace-callbacks.txt $1

delete_filefilter
