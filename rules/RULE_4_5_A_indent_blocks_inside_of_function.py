"""
Indent blocks inside of function.

== Violation ==

    void A() {
    for (;;) <== Violation
        {
        }
    }

    void K()
    {  <== Don't care. It's not the block inside of the function.
        if (true)
        {
            if (KK) {
            AA; <== Violation
            }
        }

        switch(TT) {
        case WEWE: <== Violation
            WOW;
        }
    }

== Good ==

    void K()
    {
        if (true)
        {
            if (KK) { <== OK
                AA;   <== OK
            }
        }

        switch(TT) {   <== OK
            case WEWE: <== OK
                WOW;
        }
    }

"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, contextStack):
    t = lexer.GetCurToken()
    if t.type == "LBRACE" and t.pp is None:
        column = GetIndentation(t)
        t2 = lexer.GetNextMatchingToken(True)
        if t2 is not None and t.lineno != t2.lineno:
            nt = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
            if nt is not None and nt != t2 and nt.type not in ("LBRACE", "RBRACE") and GetIndentation(nt) <= column:
                nsiqcppstyle_reporter.Error(
                    nt,
                    __name__,
                    f"Indent in the block. token({nt.value}) seems to be located left column of previsous brace",
                )


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
for (;;) {
}
}
""",
        )
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze(
            "thisfile.c",
            """
void function() {
a = {
}
}
""",
        )
        self.ExpectError(__name__)

    def test3(self):
        self.Analyze(
            "thisfile.c",
            """
void function() {
    a = {
        }
    while(True)
    {
    tt {
    }
    }
    k = {}
}
""",
        )
        self.ExpectError(__name__)

    def test4(self):
        self.Analyze(
            "thisfile.c",
            """
void function() {
    a = {
        }
    while(True)
    {
    }
}
""",
        )
        self.ExpectSuccess(__name__)

    def test5(self):
        self.Analyze(
            "thisfile.c",
            """
void function() {
    a = { dsdsd}
}
""",
        )
        self.ExpectSuccess(__name__)

    def test6(self):
        self.Analyze(
            "thisfile.c",
            """
#define AA(p, t) \
do {\
aa = e;
} while(0)
""",
        )
        self.ExpectSuccess(__name__)
