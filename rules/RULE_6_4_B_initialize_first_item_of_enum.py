"""
Check the first item of enum type and check if it is initalized.

It checks the first element and see there is = token.

== Violation ==

    enum A {
        A, B <== Violation
    }

== Good ==

    enum A {
        A=4, B <== OK
    }

"""
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, typeName, typeFullName, decl, contextStack, typeContext):
    if not decl and typeName == "ENUM" and typeContext is not None:
        lexer._MoveToToken(typeContext.startToken)
        t2 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
        t3 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
        if t3 is not None and t3.type != "EQUALS":
            nsiqcppstyle_reporter.Error(
                t3,
                __name__,
                f"The first item({t2.value}) of enum type({typeFullName}) should be initialized.",
            )


ruleManager.AddTypeNameRule(RunRule)


##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddTypeNameRule(RunRule)

    def test1(self):
        self.Analyze(
            "thisfile.c",
            """
enum KK {
    tt,
    kk
}
""",
        )
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze(
            "thisfile.c",
            """
enum KK {
    tt = 1,
    kk
}
""",
        )
        self.ExpectSuccess(__name__)

    def test3(self):
        self.Analyze(
            "thisfile.c",
            """
enum KK {
    tt = 1, kk
}
""",
        )
        self.ExpectSuccess(__name__)

    def test4(self):
        self.Analyze(
            "thisfile.c",
            """
typedef enum {
    tt = 1, kk
} KK;
""",
        )
        self.ExpectSuccess(__name__)

    def test5(self):
        self.Analyze(
            "thisfile.c",
            """
void A() {
enum KK{
    tt, kk
};
}
""",
        )
        self.ExpectError(__name__)
