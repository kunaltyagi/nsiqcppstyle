"""
Do not use macro for the constants.
if the constants is defined by macro. this rule reports a violation.
Instead, use enum or const variables.

However, it's ok to write a macro function.
And.. If the macro is start with underbar,
it regards this macro is defined for the special purpose
and it doesn't report a violation on it.

== Violation ==

    #define KK 1 <== Violation
    #define TT "sds" <== Violation

== Good ==

    #define KK(A) (A)*3 <== Don't care. It's macro function
    const int k = 3; <== OK
    const char *t = "EWEE"; <== OK
"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, contextStack):
    t = lexer.GetCurToken()
    if t.type == "PREPROCESSOR" and t.value.find("define") != -1:
        d = lexer.GetNextTokenSkipWhiteSpaceAndComment()
        k2 = lexer.GetNextTokenSkipWhiteSpaceAndComment()
        if d.type == "ID" and k2 is not None and k2.type in ["NUMBER", "STRING", "CHARACTOR"] and d.lineno == k2.lineno:
            if not Search("^_", d.value):
                nsiqcppstyle_reporter.Error(d, __name__, f"Do not use macro({d.value}) for constant")


ruleManager.AddPreprocessRule(RunRule)


##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddPreprocessRule(RunRule)

    def test1(self):
        self.Analyze(
            "thisfile.c",
            """
#define k 1
""",
        )
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze(
            "thisfile.c",
            """
#define tt(A) 3
""",
        )
        self.ExpectSuccess(__name__)

    def test3(self):
        self.Analyze(
            "thisfile.c",
            """
#  define t "ewew"
""",
        )
        self.ExpectError(__name__)

    def test4(self):
        self.Analyze(
            "thisfile.c",
            """
#  define _t "ewew"
""",
        )
        self.ExpectSuccess(__name__)
