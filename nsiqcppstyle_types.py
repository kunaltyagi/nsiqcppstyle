# Copyright (c) 2022 All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from typing import NewType, Union
import nsiqcppstyle_lexer
import nsiqcppstyle_checker

# A stack showing the lexical context the token resides in
ContextStackType = NewType('ContextStackType', nsiqcppstyle_checker.ContextStack)

# The new context entry that will be pushed to the contextStack due to this token
ContextType = NewType('ContextType', nsiqcppstyle_checker.Context)

# A boolean flag denoting whether the function is a declaration (True) or definition (False)
DeclarationType = NewType('DeclarationType', bool)

# A directory name
DirNameType = NewType('DirNameType', str)

# The name of the file being analyzed
FileNameType = NewType('FileNameType', str)

# A full function name
FullNameType = NewType('FullNameType', str)

# The lexer object used to analyze the source file
LexerType = NewType('LexerType', nsiqcppstyle_checker.CppLexerNavigator)

# The line number (> 0) of the <LineType> in the file currently being processed
LineNumberType = NewType('LineNumberType', int)

# The text of the source file line just read
LineType = NewType('LineType', str)

# The target directory currently being analyzed
TargetPathType = NewType('TargetPathType', Union[str, bytes])

# The token currently being processed
TokenType = NewType('ContextStackType', nsiqcppstyle_lexer.LexToken)

# The new context entry that will be pushed to the contextStack due to this "type" token
TypeContextType = NewType('TypeContextType', ContextType)

# The typed variable name (e.g., the class name)
TypeFullNameType = NewType('TypeFullNameType', FullNameType)

# The name of the C++ type encountered (e.g., "CLASS", "STRUCT")
TypeNameType = NewType('TypeNameType', str)
