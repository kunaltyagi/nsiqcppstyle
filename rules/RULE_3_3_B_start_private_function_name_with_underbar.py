"""
Start the private function name with a underbar.
This rule is only applied on the cpp files.

== Violation ==

    class A
    {
        private:
            bool GetSth(); <== Violation. The private function should starts with _.
    };

== Good ==

    class A
    {
        public :
            bool GetSth();  <== Don't care. it's public function.
        private:
            bool _GetSth(); <== OK.
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
    if IsConstructor(value, fullName, upperBlock):
        return
    if IsOperator(value):
        return
    if upperBlock is not None and upperBlock.additional == "PRIVATE" and not value.startswith("_"):
        nsiqcppstyle_reporter.Error(t, __name__, "Start private function name(%s) with underbar" % fullName)


def RunTypeScopeRule(lexer, contextStack):
    t = lexer.GetCurToken()
    if t.type in ["PUBLIC", "PRIVATE", "PROTECTED"]:
        curContext = contextStack.SigPeek()
        if curContext.type in ["CLASS_BLOCK", "STRUCT_BLOCK"]:
            curContext.additional = t.type


ruleManager.AddFunctionNameRule(RunRule)
ruleManager.AddTypeScopeRule(RunTypeScopeRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddFunctionNameRule(RunRule)
        ruleManager.AddTypeScopeRule(RunTypeScopeRule)
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
private:
bool CTEST:CanHave() {
}
}""",
        )
        self.ExpectError(__name__)

    def test3(self):
        self.Analyze(
            "test/thisFile.c",
            """
class K {
private:
bool CTEST:_CanHave() {
}
}""",
        )
        self.ExpectSuccess(__name__)

    def test4(self):
        self.Analyze(
            "test/thisFile.c",
            """
class K {
public:
bool CTEST:_CanHave() {
}
}""",
        )
        self.ExpectSuccess(__name__)

    def test5(self):
        self.Analyze(
            "test/thisFile.c",
            """
class K {
private:
bool CTEST:_CanHave() ;
}""",
        )
        self.ExpectSuccess(__name__)

    def test6(self):
        self.Analyze(
            "test/thisFile.c",
            """
class K {
private:
public :
bool CTEST:CanHave();
""",
        )
        self.ExpectSuccess(__name__)

    def test7(self):
        self.Analyze(
            "test/thisFile.c",
            """
class K {
public :
private:
bool CTEST:CanHave();
""",
        )
        self.ExpectError(__name__)

    def test8(self):
        self.Analyze(
            "test/thisFile.c",
            """
class TT::K {
public :
private:
 K();
 ~K();
""",
        )
        self.ExpectSuccess(__name__)

    def test9(self):
        self.Analyze(
            "test/thisFile.c",
            """
int KK:KK(Hello wow){
};

int KK:~KK() {
}
""",
        )
        self.ExpectSuccess(__name__)

    def test10(self):
        self.Analyze(
            "test/thisFile.c",
            """
class KK {
    private :
        int K1();
}
""",
        )
        self.ExpectError(__name__)

    def test11(self):
        self.Analyze(
            "test/thisFile.c",
            """
class TT {
    private :
        void operator=(sdsd) {
}
""",
        )
        self.ExpectSuccess(__name__)

    def test12(self):
        self.Analyze(
            "test/thisFile.c",
            """
class K {
public :
private:
 K();
 ~K();
""",
        )
        self.ExpectSuccess(__name__)

    def test13(self):
        self.Analyze(
            "test/thisFile.c",
            """
DEF_DD(wewe)
""",
        )
        self.ExpectSuccess(__name__)

    def test14(self):
        self.Analyze(
            "test/thisFile.c",
            """
DEF11_DD(wewe)
""",
        )
        self.ExpectSuccess(__name__)
