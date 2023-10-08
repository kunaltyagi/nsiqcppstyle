"""
Do not use question(?) keyword.
if it's shown... this rule reports a violation.

== Violation ==

    void a() {
        c = t ? 1 : 2;  <== Violation. ? keyword is used.
    }

== Good ==

    void a() {
        if (t) { <== OK.
           c = 1;
        } else {
           c = 2;
        }
    }

"""
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, contextStack):
    t = lexer.GetCurToken()
    if t.type == "TERNARY":
        t2 = lexer.PeekPrevTokenSkipWhiteSpaceAndComment()
        if t2 is not None and t2.type != "OPERATOR":
            nsiqcppstyle_reporter.Error(t, __name__, "Do not use ? keyword")


ruleManager.AddFunctionScopeRule(RunRule)
ruleManager.AddPreprocessRule(RunRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddFunctionScopeRule(RunRule)
        ruleManager.AddPreprocessRule(RunRule)

    def test1(self):
        self.Analyze(
            "thisfile.c",
            """
void Hello() {
   int k = true ? 1 : 2;
}
""",
        )
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze(
            "thisfile.c",
            """
int k = true ? 1 : 2;
void Hello() {
}
""",
        )
        self.ExpectSuccess(__name__)

    def test3(self):
        self.Analyze(
            "thisfile.c",
            """
#define k (t ? 1 : 2);
void Hello() {
}
""",
        )
        self.ExpectError(__name__)
