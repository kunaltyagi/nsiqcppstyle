"""
Ensure that the functions declarations/definitions in the class/struct scope are scoped

== Violation ==

    class A
    {
            bool GetSth();  <== Violation. Should be A::GetSth.
    };

== Good ==

    class A
    {
        bool ::GetSth();  <== OK.
        public:
            bool A::GetSthElse();  <== OK.
    };
"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, fullName, decl, contextStack, context):
    t = lexer.GetCurToken()
    value = t.value
    upperBlock = contextStack.SigPeek()
    if upperBlock is None:
        return
    if upperBlock.type in ["CLASS_BLOCK", "STRUCT_BLOCK"] and value == fullName:
        class_name = upperBlock.name.rsplit("::")[-1]
        nsiqcppstyle_reporter.Error(t, __name__, f"Function name({fullName}) should include local scope({class_name})")


ruleManager.AddFunctionNameRule(RunRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddFunctionNameRule(RunRule)
        global currentVisibility
        currentVisibility = False

    def test1(self):
        self.Analyze(
            "test/thisFile.c",
            """
bool CanHave() {
}""",
        )
        self.ExpectSuccess(__name__)

    def test2(self):
        self.Analyze(
            "test/thisFile.c",
            """
class TT::K {
bool CanHave() {
}
}""",
        )
        self.ExpectError(__name__)

    def test3(self):
        self.Analyze(
            "test/thisFile.c",
            """
class TT::K {
bool K::CanHave() {
}
}""",
        )
        self.ExpectSuccess(__name__)

    def test4(self):
        self.Analyze(
            "test/thisFile.c",
            """
class TT::K {
bool TT::K::CanHave() {
}
}""",
        )
        self.ExpectSuccess(__name__)

    def test5(self):
        self.Analyze(
            "test/thisFile.c",
            """
class TT::K {
K& operator++();
}""",
        )
        self.ExpectError(__name__)

    def test6(self):
        self.Analyze(
            "test/thisFile.c",
            """
class TT::K {
K& K::operator++();
}""",
        )
        self.ExpectSuccess(__name__)
