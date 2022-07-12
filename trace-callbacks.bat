@echo off
REM Copyright (c) 2022 All rights reserved.
REM SPDX-License-Identifier: GPL-2.0-only
REM File: trace-callbacks.bat
REM Purpose: Trace every N'Siq CppStyle callback for a given input source file.  Using
REM          the trace, the rule developer can plan how to write a new rule.

if [%1]==[] goto no_file_given
if exist filefilter.trace-callbacks.txt del filefilter.trace-callbacks.txt

echo ~ TOOL_trace_nsiqcppstyle_callbacks > filefilter.trace-callbacks.txt

python nsiqcppstyle.py -f filefilter.trace-callbacks.txt %1
goto finish

:no_file_given
echo No source file was given
goto usage

:usage
echo USAGE: trace-callbacks.bat full-path-to-source-file
goto finish

:finish
if exist filefilter.trace-callbacks.txt del filefilter.trace-callbacks.txt