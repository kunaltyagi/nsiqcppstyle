"""
Start the function name with a lower case letter.
It's rule for only Unix / Linux C/C++ code.

== Violation ==

    bool CheckSth() { <== Violation. The function name starts with uppercase C.
        return false;
    }

    bool _CheckSth() { <== Violation. The function name starts with uppercase C.
        return false;
    }

== Good ==

    bool isSth() { <== OK.
        return true;
    }

"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, fullName, decl, contextStack, context):
    t = lexer.GetCurToken()
    value = t.value
    if value.startswith("_"):
        value = value[1:]
    if value.startswith("~"):
        value = value[1:]
    if Search("^[A-Z]", value):
        if IsConstructor(value, fullName, contextStack.SigPeek()):
            return
        if IsOperator(value):
            return
        nsiqcppstyle_reporter.Error(t, __name__, "Do not start function name(%s) with uppercase" % fullName)


ruleManager.AddFunctionNameRule(RunRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddFunctionNameRule(RunRule)

    def test1(self):
        self.Analyze(
            "test/thisFile.c",
            """
bool CanHave() {
}""",
        )
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze(
            "test/thisFile.c",
            """
bool CTEST:CanHave() {
}""",
        )
        self.ExpectError(__name__)

    def test3(self):
        self.Analyze(
            "test/thisFile.c",
            """
extern bool CTEST:canHave() {
}""",
        )
        self.ExpectSuccess(__name__)

    def test4(self):
        self.Analyze(
            "test/thisFile.c",
            """
extern int CTEST:_CanHave() {
}""",
        )
        self.ExpectError(__name__)

    def test5(self):
        self.Analyze(
            "test/thisFile.c",
            """
class AA {
extern int ~IsIt();
}""",
        )
        self.ExpectError(__name__)

    def test6(self):
        self.Analyze(
            "test/thisFile.c",
            """
class K {
extern bool CTEST:canHave();
}""",
        )
        self.ExpectSuccess(__name__)

    def test7(self):
        self.Analyze(
            "test/thisFile.c",
            """
class K {
   a = new EE();
}""",
        )
        self.ExpectSuccess(__name__)

    def test8(self):
        self.Analyze(
            "test/thisFile.c",
            """
class K {
  int Hello()
  int EE();
}""",
        )
        self.ExpectError(__name__)

    def test9(self):
        self.Analyze(
            "test/thisFile.c",
            """
class K {
  int K()
  int ~K()
  int ee();
}""",
        )
        self.ExpectSuccess(__name__)

    def test10(self):
        self.Analyze(
            "test/thisFile.c",
            """
#define TT KK() {\
}}
""",
        )
        self.ExpectSuccess(__name__)

    def test11(self):
        self.Analyze(
            "test/thisFile.c",
            """
void KK::KK() {
}
""",
        )
        self.ExpectSuccess(__name__)

    def test12(self):
        self.Analyze(
            "test/thisFile.c",
            """
void KK::~KK() {
}
""",
        )
        self.ExpectSuccess(__name__)

    def test13(self):
        self.Analyze(
            "test/thisFile.c",
            """
TEST()
   BLOCK1()
   BLOCK2()
   BLOCK3()

""",
        )
        self.ExpectSuccess(__name__)

    def test14(self):
        self.Analyze(
            "test/thisFile.c",
            """
void KK() {
}
""",
        )
        self.ExpectError(__name__)
