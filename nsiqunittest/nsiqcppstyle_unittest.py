# Copyright (c) 2009 NHN Inc. All rights reserved.
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
#    * Neither the name of NHN Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
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

import unittest
import nsiqcppstyle_checker
from nsiqcppstyle_outputer import _consoleOutputer as console
import nsiqcppstyle_state


class unitTest(unittest.TestCase):
    def __testFunctionSpecifier(self, specifier):
        lexer = nsiqcppstyle_checker.CppLexerNavigator(
            "a.cpp", "void FunctionName() " + specifier + ";")
        # This step resolves comments and some token types like FUNCTION
        nsiqcppstyle_checker.ContructContextInfo(lexer)
        lexer.Reset()

        assert(lexer.GetNextTokenSkipWhiteSpaceAndComment().type == 'VOID')
        assert(lexer.GetNextTokenSkipWhiteSpaceAndComment().type == 'FUNCTION')
        assert(lexer.GetNextTokenSkipWhiteSpaceAndComment().type == 'LPAREN')
        assert(lexer.GetNextTokenSkipWhiteSpaceAndComment().type == 'RPAREN')
        # Specifier keyword
        specifierToken = lexer.GetNextTokenSkipWhiteSpaceAndComment()
        assert(specifierToken.type == 'IGNORE')
        assert(specifierToken.value == specifier)

        assert(lexer.GetNextTokenSkipWhiteSpaceAndComment().type == 'SEMI')
        assert(lexer.GetNextTokenSkipWhiteSpaceAndComment() is None)

    def testIgnoreFinalFunctionSpecifier(self):
        self.__testFunctionSpecifier("final")

    def testIgnoreOverrideFunctionSpecifier(self):
        self.__testFunctionSpecifier("override")

    def testIgnoreNoexceptFunctionSpecifier(self):
        self.__testFunctionSpecifier("noexcept")

    def testGetPrevMatchingLT(self):
        lexer = nsiqcppstyle_checker.CppLexerNavigator(
            "a.cpp", "std::set<int> m;")
        # This step resolves comments and some token types like FUNCTION
        nsiqcppstyle_checker.ContructContextInfo(lexer)
        lexer.Reset()

        ltToken = lexer.GetNextTokenInType("LT")
        assert(ltToken is not None and ltToken.type == "LT")
        gtToken = lexer.GetNextTokenInType("GT")
        assert(gtToken is not None and gtToken.type == "GT")

        matchingLtToken = lexer.GetPrevMatchingLT()
        assert(matchingLtToken is not None and matchingLtToken.type == "LT")
        assert(matchingLtToken.column == ltToken.column)

    def testGetPrevMatchingLTWithInnerOnes(self):
        lexer = nsiqcppstyle_checker.CppLexerNavigator(
            "a.cpp", "std::map<std::set<int>, float> m;")
        # This step resolves comments and some token types like FUNCTION
        nsiqcppstyle_checker.ContructContextInfo(lexer)
        lexer.Reset()

        # Get the first < token
        ltToken = lexer.GetNextTokenInType("LT")
        assert(ltToken is not None and ltToken.type ==
               "LT" and ltToken.column == 9)

        # Get the first > token
        gtToken = lexer.GetNextTokenInType("GT")
        assert(gtToken is not None and gtToken.type == "GT")
        # Get the second > token
        prevGtTokenColumn = gtToken.column
        gtToken = lexer.GetNextTokenInType("GT")
        assert(gtToken is not None and gtToken.type ==
               "GT" and gtToken.column != prevGtTokenColumn)

        # Expect the matching < token to be the first < token
        matchingLtToken = lexer.GetPrevMatchingLT()
        assert(matchingLtToken is not None and matchingLtToken.type == "LT")
        assert(matchingLtToken.column == ltToken.column)

    def testGetPrevMatchingLTWithInner(self):
        lexer = nsiqcppstyle_checker.CppLexerNavigator(
            "a.cpp", "std::set<std::map<int, float>> m;")
        # This step resolves comments and some token types like FUNCTION
        nsiqcppstyle_checker.ContructContextInfo(lexer)
        lexer.Reset()

        # Get the first < token
        ltToken = lexer.GetNextTokenInType("LT")
        assert(ltToken is not None and ltToken.type ==
               "LT" and ltToken.column == 9)

        # Get the >> token
        gtToken = lexer.GetNextTokenInType("RSHIFT")
        assert(gtToken is not None and gtToken.type == "RSHIFT")

        # Expect the matching < token to be the first < token
        matchingLtToken = lexer.GetPrevMatchingLT()
        assert(matchingLtToken is not None and matchingLtToken.type == "LT")
        assert(matchingLtToken.column == ltToken.column)

    def test2(self):
        data = """
#ifdef __NAME__
#define KK
void function() {
}
auto
#if 0
    void function2() {
    }
#endif
#endif
"""
        navigator = nsiqcppstyle_checker.CppLexerNavigator("a.cpp", data)

        while(True):
            tok = navigator.GetNextToken()
            if tok is None:
                break

    def test3(self):
        data = """
#ifdef dsd
void function1() {
#else
void function2() {
#endif
}
"""
        navigator = nsiqcppstyle_checker.CppLexerNavigator("a.cpp", data)
        nsiqcppstyle_checker.ContructContextInfo(navigator)
        navigator.Reset()
        while(True):
            tok = navigator.GetNextTokenSkipWhiteSpaceAndComment()
            if tok is None:
                break
            # print tok, tok.contextStack

    def test4(self):
        data = """
#define dsd(dsd) \\
\tdo { \\
   ff(1);\\
} while(0)
int a;
"""

        console.SetLevel(console.Level.Verbose)
        navigator = nsiqcppstyle_checker.CppLexerNavigator("a.cpp", data)
        nsiqcppstyle_checker.ContructContextInfo(navigator)
        navigator.Reset()
        while(True):
            tok = navigator.GetNextTokenSkipWhiteSpaceAndComment()
            if tok is None:
                break
            # print tok, tok.contextStack, tok.pp

    def test5(self):
        data = """
foo (bar*)[];
"""
        navigator = nsiqcppstyle_checker.CppLexerNavigator("a.cpp", data)
        nsiqcppstyle_checker.ContructContextInfo(navigator)
        navigator.Reset()
        tok = navigator.GetNextTokenSkipWhiteSpaceAndComment()
        assert(tok.type == 'ID' and tok.value == 'foo')
