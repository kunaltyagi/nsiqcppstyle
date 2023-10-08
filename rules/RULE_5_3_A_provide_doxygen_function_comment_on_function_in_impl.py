"""
Provide the function doxygen comment in impl file.
It check if there is doxygen sytle comment in front of each function definition.
It only check none static and none private funcions definition.
Unfortunately, this rule can not determine the method is private or not,
if the function definition is located in a cpp file.
Please put the '// NS' on the right side of the private function signature to suppress the false alarms.

Example)
 = a.cpp =
void KK::C()  // NS
{
}

== Violation ==

 = a.cpp =
    void FunctionA() { <== Violation. No doxygen comment.
    }

    /*        <== Violation. It's not the doxygen comment
     *
     */
    void FunctionB()
    {
    }

== Good ==

 = a.cpp =

    /**          <== OK
     * blar blar
     */
    void FunctionA()
    {
    }

    /**
     * blar blar
     */
    void FunctionB();  <== OK.

    class A {
        private :
            void FunctionC() {  <== Don't care. it's the private function.
            }
    }
    static void FunctionD() <== Don't care. it's the c style private function.
    {
    }
  = a.h =
    void FunctionB();  <== Don't care. It's the declared in the header.

"""
import nsiqcppstyle_reporter
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, fullName, decl, contextStack, context):
    ext = lexer.filename[lexer.filename.rfind(".") :]
    if not decl and ext != ".h" and context is not None:
        upperBlock = contextStack.SigPeek()
        if upperBlock is not None and upperBlock.type == "CLASS_BLOCK" and upperBlock.additional == "PRIVATE":
            return

        t1 = lexer.GetPrevTokenInType("STATIC", True)
        t2 = lexer.GetPrevTokenInTypeList(["SEMI", "RBRACE"], True)
        if t1 is not None and (t2 is None or t1.lexpos > t2.lexpos):
            return

        t = lexer.GetCurToken()
        lexer.PushTokenIndex()
        t2 = lexer.GetPrevTokenInType("COMMENT")
        lexer.PopTokenIndex()
        lexer.PushTokenIndex()
        t3 = lexer.GetPrevTokenInTypeList(["SEMI", "PREPROCESSOR"], False, True)
        lexer.PopTokenIndex()
        if t2 is not None and t2.additional == "DOXYGEN" and (t3 is None or t.lexpos > t3.lexpos):
            return
        nsiqcppstyle_reporter.Error(
            t,
            __name__,
            "Doxygen Comment should be provided in front of function (%s) in impl file." % fullName,
        )


ruleManager.AddFunctionNameRule(RunRule)


def RunTypeScopeRule(lexer, contextStack):
    t = lexer.GetCurToken()
    if t.type in ["PUBLIC", "PRIVATE", "PROTECTED"]:
        curContext = contextStack.SigPeek()
        if curContext.type in ["CLASS_BLOCK", "STRUCT_BLOCK"]:
            curContext.additional = t.type


ruleManager.AddTypeScopeRule(RunTypeScopeRule)


##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddFunctionNameRule(RunRule)
        ruleManager.AddTypeScopeRule(RunTypeScopeRule)

    def test1(self):
        self.Analyze(
            "thisfile.c",
            """
void FunctionA() {
}
""",
        )
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze(
            "thisfile.c",
            """
/*
 *
 */
extern void FunctionB() {
}
""",
        )
        self.ExpectError(__name__)

    def test3(self):
        self.Analyze(
            "thisfile.c",
            """
class A {
public:
    void ~A() {
    }
}
""",
        )
        self.ExpectError(__name__)

    def test4(self):
        self.Analyze(
            "thisfile.c",
            """
class J {
    /** HELLO */
    C() {
    }
public :
    /** HELLO */
    A();
private :
    B() {}

}
""",
        )
        self.ExpectSuccess(__name__)

    def test5(self):
        self.Analyze(
            "thisfile.c",
            """
/*
 *
 */
static void FunctionB() {
}
""",
        )
        self.ExpectSuccess(__name__)

    def test6(self):
        self.Analyze(
            "thisfile.h",
            """
int a;
void FunctionB(){
}
""",
        )
        self.ExpectSuccess(__name__)

    def test7(self):
        self.Analyze(
            "thisfile.c",
            """
int a;
void FunctionB(){
}
""",
        )
        self.ExpectError(__name__)

    def test8(self):
        self.Analyze(
            "thisfile.c",
            """
class J {
    C() {
    }
}
""",
        )
        self.ExpectError(__name__)
