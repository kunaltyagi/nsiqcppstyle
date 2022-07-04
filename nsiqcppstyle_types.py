# Copyright (c) 2022 All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from typing import NewType, Union
import nsiqcppstyle_lexer
import nsiqcppstyle_checker

# A stack showing the lexical context the token resides in
ContextStack = NewType('ContextStack', nsiqcppstyle_checker.ContextStack)

# The new context entry that will be pushed to the contextStack due to this token
Context = NewType('Context', nsiqcppstyle_checker.Context)

# A boolean flag denoting whether the function is a declaration (True) or definition (False)
Declaration = NewType('Declaration', bool)

# A directory name
DirName = NewType('DirName', str)

# The name of the file being analyzed
FileName = NewType('FileName', str)

# A full function name
FullFunctionName = NewType('FullFunctionName', str)

# The lexer object used to analyze the source file
Lexer = NewType('Lexer', nsiqcppstyle_checker.CppLexerNavigator)

# The line number (> 0) of the <LineType> in the file currently being processed
LineNumber = NewType('LineNumber', int)

# The text of the source file line just read
LineText = NewType('LineText', str)

# The target directory currently being analyzed
TargetDirectory = NewType('TargetDirectory', Union[str, bytes])

# The token currently being processed
Token = NewType('Token', nsiqcppstyle_lexer.LexToken)

# The typed variable name (e.g., the class name)
TypeFullName = NewType('TypeFullName', str)

# The name of the C++ type encountered (e.g., "CLASS", "STRUCT")
TypeName = NewType('TypeName', str)
