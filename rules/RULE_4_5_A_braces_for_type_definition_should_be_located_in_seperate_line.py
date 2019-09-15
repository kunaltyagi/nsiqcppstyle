"""
Braces for type definition(class / struct / union / enum) should be located in the seperate line.

== Violation ==

    class K() { <== ERROR
    }

    struct K { <== ERROR
    }

== Good ==

    struct A()
    { <== CORRECT
    }

    class K()
    { <== CORRECT
    public :
        void Hello() { <== Don't care. It's a function definition.
        }
    }
"""
from nsiqunittest.nsiqcppstyle_unittestbase import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulemanager import *


def RunRule(lexer, currentType, fullName, decl, contextStack, typeContext):
    if not decl and currentType != "NAMESPACE" and typeContext is not None:
        t = lexer.GetNextTokenInType("LBRACE", False, True)
        if t is not None:
            t2 = typeContext.endToken
            if t2 is not None and t.lineno != t2.lineno:
                prevToken = lexer.GetPrevTokenSkipWhiteSpaceAndCommentAndPreprocess()
                # print contextStack.Peek()
                if prevToken is not None and prevToken.lineno == t.lineno:
                    nsiqcppstyle_reporter.Error(
                        t, __name__, "The brace for type definition should be located in start of line")
                if t2.lineno != t.lineno and GetRealColumn(
                        t2) != GetRealColumn(t):
                    nsiqcppstyle_reporter.Error(
                        t2, __name__, "The brace for type definition should be located in same column")


ruleManager.AddTypeNameRule(RunRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddTypeNameRule(RunRule)

    def test1(self):
        self.Analyze("thisfile.c", """
public class A {

}
""")
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze("thisfile.c", """
class C : public AA {

}
""")
        self.ExpectError(__name__)

    def test3(self):
        self.Analyze("thisfile.c", """
class K
{
    void function() const {
    }
    class T
    {
    }
}
""")
        self.ExpectSuccess(__name__)

    def test4(self):
        self.Analyze("thisfile.c", """
class K
{
    void function() const {
    }
    class T {
    }
}
""")
        self.ExpectError(__name__)

    def test5(self):
        self.Analyze("thisfile.c", """
class C : public AA
{
    class T {
    }
}
""")
        self.ExpectError(__name__)

    def test6(self):
        self.Analyze("thisfile.c", """
class C : public AA
{
    class T
    {
      }
}
""")
        self.ExpectError(__name__)

    def test7(self):
        self.Analyze("thisfile.c", """
class C : public AA
{
    class T
    {   }
}
""")
        self.ExpectSuccess(__name__)

    def test8(self):
        self.Analyze("thisfile.c", """
namespace C {
}
""")
        self.ExpectSuccess(__name__)

    def test9(self):
        self.Analyze("thisfile.c", """
if (hello) {
// {kr} m_btn5 {/kr}
}
""")
        self.ExpectSuccess(__name__)
