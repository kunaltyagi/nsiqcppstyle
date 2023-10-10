"""
Provide the struct/union doxygen comment.
It checks if there is doxygen sytle comment in front of each struct/union definition.

== Violation ==

    struct A { <== Violation. No doxygen comment.
    };

    /*        <== Violation. It's not doxygen comment
     *
     */
    union B {
    };

== Good ==

    /**
     * blar blar
     */
    struct A { <== OK
    };

    struct A; <== Don't care. It's forward decl.
"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, currentType, fullName, decl, contextStack, context):
    if not decl and currentType in ("STRUCT", "UNION") and context is not None:
        t = lexer.GetCurToken()
        lexer.PushTokenIndex()
        t2 = lexer.GetPrevTokenInType("COMMENT")
        lexer.PopTokenIndex()
        lexer.PushTokenIndex()
        t3 = lexer.GetPrevTokenInTypeList(["SEMI", "PREPROCESSOR", "LBRACE"], False, True)
        lexer.PopTokenIndex()
        if t2 is not None and t2.additional == "DOXYGEN" and (t3 is None or t2.lexpos > t3.lexpos):
            return
        nsiqcppstyle_reporter.Error(
            t,
            __name__,
            "Doxygen Comment should be provided in front of struct/union def(%s)." % fullName,
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
struct A {
}
""",
        )
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze(
            "thisfile.c",
            """
/*
 */
struct K {
}
""",
        )
        self.ExpectError(__name__)

    def test3(self):
        self.Analyze(
            "thisfile.c",
            """
/**
 */
struct K {
    struct T {
    }
}
""",
        )
        self.ExpectError(__name__)

    def test4(self):
        self.Analyze(
            "thisfile.c",
            """
/**
 *
 */
struct J {
    int k;
    /**
     */
    struct T {
    }
}
class T;
""",
        )
        self.ExpectSuccess(__name__)

    def test5(self):
        self.Analyze(
            "thisfile.c",
            """
/*
 */
struct K {
}
""",
        )
        self.ExpectError(__name__)

    def test6(self):
        self.Analyze(
            "thisfile.c",
            """
typedef struct  {
} K
""",
        )
        self.ExpectError(__name__)
