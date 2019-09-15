"""
Do not use goto statements.
if it's shown... this rule reports a violation.

== Violation ==

    void FunctionA()
    {
        while(True)
        {
            goto AAA; <== Violation. A goto statement is used.
        }
        AAA:
    }

== Good ==

    void FunctionA()
    {
        while(True)
        {
            break;  <== OK.
        }
    }
"""

from nsiqunittest.nsiqcppstyle_unittestbase import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulemanager import *


def RunRule(lexer, contextStack):
    t = lexer.GetCurToken()
    if t.type == "GOTO":
        nsiqcppstyle_reporter.Error(t, __name__, "Do not use goto keyword")


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
        self.Analyze("thisfile.c", """
void Hello() {
   goto TT:
}
""")
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze("thisfile.c", """
goto TT:
void Hello() {
}
""")
        self.ExpectSuccess(__name__)
