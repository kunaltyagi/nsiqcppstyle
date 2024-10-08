"""
Provide the namespace doxygen comment.
It checks if there is doxygen sytle comment in front of each 'namespace' keyword

== Violation ==

    namespace AA         <== Violation. No comment on the namespace AA
    {
    }

    /*                   <== Violation. There is comment but not a doxygen comment.
     * blar blar
     */
    namespace BB
    {
    }

== Good ==

    /**                  <== OK!
     * blar blar
     */
    namespace AA
    {
    }

"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, currentType, fullName, decl, contextStack, typeContext):
    if not decl and currentType == "NAMESPACE" and typeContext is not None:
        t = lexer.GetCurToken()
        lexer.PushTokenIndex()
        t2 = lexer.GetPrevTokenInType("COMMENT")
        lexer.PopTokenIndex()
        lexer.PushTokenIndex()
        t3 = lexer.GetPrevTokenInTypeList(["SEMI", "PREPROCESSOR", "LBRACE"], False, True)
        lexer.PopTokenIndex()
        if t2 is not None and (t3 is None or t2.lexpos > t3.lexpos):
            if t2.additional in ["DOXYGEN_JAVADOC", "DOXYGEN_QT", "DOXYGEN_CPP"]:
                return
        nsiqcppstyle_reporter.Error(
            t,
            __name__,
            f"Doxygen Comment should be provided in front of namespace def({fullName}).",
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
namespace K;
""",
        )
        self.ExpectSuccess(__name__)

    def test2(self):
        self.Analyze(
            "thisfile.c",
            """
/*
 */
namespace K {
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
using namespace A;
""",
        )
        self.ExpectSuccess(__name__)
