"""
Use braces even for the one statement.

== Violation ==

    void Function() {
        for (;;)
            print("WOW"); <== Violation

        while(i > 7)
            i++; <== Violation
    }

== Good ==

    void Function()
    {
        for (;;)
        {
            print("WOW"); <== OK
        }
        while(i > 7) { <== OK
            i++;
        }
    }

"""

from nsiqcppstyle_checker import *
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, contextStack):
    t = lexer.GetCurToken()
    if t.type in ("IF", "WHILE", "FOR"):
        lparen = lexer.GetNextTokenInType("LPAREN", False, True)
        if lparen is None:
            return
        lexer.GetNextMatchingToken()
        nt = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
        if nt is not None and nt.type not in ("SEMI", "LBRACE"):
            nsiqcppstyle_reporter.Error(t, __name__, "use brace for even on statement in if/while/for clause")
    elif t.type == "ELSE":
        nt = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
        if nt is not None and nt.type not in ("IF", "LBRACE"):
            nsiqcppstyle_reporter.Error(t, __name__, "use brace for even on statement in else clause")


ruleManager.AddFunctionScopeRule(RunRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddFunctionScopeRule(RunRule)

    def test1(self):
        self.Analyze(
            "thisfile.c",
            """
void function() {
for (;;)
    a = 3;
}
""",
        )
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze(
            "thisfile.c",
            """
void function() {
for (;;)  {
    a = 3;
    }
}
""",
        )
        self.ExpectSuccess(__name__)

    def test3(self):
        self.Analyze(
            "thisfile.c",
            """
void function() {
while(True)
    sdsd();
}
""",
        )
        self.ExpectError(__name__)

    def test4(self):
        self.Analyze(
            "thisfile.c",
            """
void function() {
do {
} while(true);
}
""",
        )
        self.ExpectSuccess(__name__)

    def test5(self):
        self.Analyze(
            "thisfile.c",
            """
void function() {
if (true) {
    sdsd();
    } else
        SSDD();
}
""",
        )
        self.ExpectError(__name__)

    def test6(self):
        self.Analyze(
            "thisfile.c",
            """
void function() {
if (true) {
    sdsd();
    } else {
        SSDD();
    } else if (true) {
    }

}
""",
        )
        self.ExpectSuccess(__name__)
