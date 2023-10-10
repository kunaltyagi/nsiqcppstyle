"""
Provide file comment.

File comment including 'copyright' should be provided in the head of file.
This rule detect following style file comment.

== Violation ==

    = start of file =
    #define "AA" <== Violation. file comment should be the first element of file.
    ///
    /// blar blar
    /// Copyright reserved.
    ///

    = start of file =
    /**         <== Violation. No copyright string.
     * blar blar
     * blar blar
     */

== Good ==

    = start of file =
    ///
    /// blar blar
    /// Copyright reserved. <== Correct
    /// file
    /// author
    /// date
    /// version
    /// brief
    ///

    = start of file =
    /**
     * blar blar
     * Copyright reserved. <== Correct
     * file
     * author
     * date
     * version
     * brief
     * blar blar
     */
"""
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def error(lexer):
    nsiqcppstyle_reporter.Error(
        DummyToken(lexer.filename, "", 1, 0),
        __name__,
        """Please provide file info comment in front of
            file. It includes license/copyright information along
            with filename, author, date of modification, version and
            a brief description""",
    )


def RunRule(lexer, filename, dirname):
    token = lexer.GetNextToken()

    while True:
        if token is None or token.type not in ("COMMENT", "CPPCOMMENT"):
            error(lexer)
            return

        if token.value.lower().find("copyright") != -1 or token.value.lower().find("license") != -1:
            return

        token = lexer.GetNextTokenSkipWhiteSpace()


ruleManager.AddFileStartRule(RunRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddFileStartRule(RunRule)

    def test1(self):
        self.Analyze(
            "thisfile.c",
            """// license
// copyright
""",
        )
        self.ExpectSuccess(__name__)

    def test2(self):
        self.Analyze(
            "thisfile.c",
            """/**
#if 0
#endif
license
coryright */ """,
        )
        self.ExpectSuccess(__name__)

    def test3(self):
        self.Analyze(
            "thisfile.c",
            """
// license
// copyrigh1
""",
        )
        self.ExpectError(__name__)

    def test4(self):
        self.Analyze(
            "thisfile.c",
            """#define "WEWE"
// license
// copyrigh1
#include </ewe/kk> """,
        )
        self.ExpectError(__name__)

    def test5(self):
        self.Analyze(
            "thisfile.c",
            """
#define "WEWE"
// license
// copyright
#include </ewe/kk> """,
        )
        self.ExpectError(__name__)

    def test6(self):
        self.Analyze(
            "thisfile.c",
            """// license
// copyright
#define "WEWE"
#include </ewe/kk> """,
        )
        self.ExpectSuccess(__name__)

    def test7(self):
        self.Analyze(
            "thisfile.c",
            """/*
 * license
 * copyright
 */
""",
        )
        self.ExpectSuccess(__name__)
