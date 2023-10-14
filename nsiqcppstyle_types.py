# Copyright (c) 2022 All rights reserved.
# SPDX-License-Identifier: GPL-2.0-only

from typing import NewType, TypeVar

import nsiqcppstyle_checker
import nsiqcppstyle_lexer

# Expose already existing types (i.e., Context and ContextStack)
Context = nsiqcppstyle_checker.Context
ContextStack = nsiqcppstyle_checker.ContextStack

# A boolean flag denoting whether the function is a declaration (True) or definition (False)
Declaration = NewType("Declaration", bool)

# A directory name
DirName = NewType("DirName", str)

# The name of the file being analyzed
FileName = NewType("FileName", str)

# A full function name
FullFunctionName = NewType("FullFunctionName", str)

# The lexer object used to analyze the source file
Lexer = NewType("Lexer", nsiqcppstyle_checker.CppLexerNavigator)

# The line number (> 0) of the <LineType> in the file currently being processed
LineNumber = NewType("LineNumber", int)

# The text of the source file line just read
LineText = NewType("LineText", str)

# The target directory currently being analyzed
TargetDirectoryStr = NewType("TargetDirectoryStr", str)
TargetDirectoryBytes = NewType("TargetDirectoryBytes", bytes)
TargetDirectory = TypeVar("TargetDirectory", TargetDirectoryStr, TargetDirectoryBytes)

# The token currently being processed
Token = NewType("Token", nsiqcppstyle_lexer.LexToken)

# The typed variable name (e.g., the class name)
TypeFullName = NewType("TypeFullName", str)

# The name of the C++ type encountered (e.g., "CLASS", "STRUCT")
TypeName = NewType("TypeName", str)
