"""
Do not use lower case letters for the macro constant.
However, it's ok to write a macro function using lower case letters.

== Violation ==

    #define Kk 1 <== Violation. The lower case 'k' is used in macro name.
    #define tT "sds" <== Violation. The lower case 't' is used in macro name.

== Good ==

    #define KK 3        <== OK. KK is upper case.
    #define kk(A) (A)*3 <== Don't care. It's the macro function.

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
            if Search("[a-z]", d.value):
                nsiqcppstyle_reporter.Error(d, __name__, f"Do not use lower case ({d.value}) for macro value")


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

    def test5(self):
        self.Analyze(
            "thisfile.c",
            """
#  define t # "ewew"
""",
        )
        self.ExpectSuccess(__name__)
