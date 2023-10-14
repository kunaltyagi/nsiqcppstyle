"""
Do not use buffer overflow risky functions in unix env.
if they're found, this rule reports a volation.

== Buffer Overflow Risky Function List ==
    - strcpy()
    - strcat()
    - sprintf()
    - vsprintf()
    - gets()
    - realpath()
    - getopt()
    - getpass()
    - streadd()
    - strecpy()
    - strtrns()
"""

import nsiqcppstyle_reporter
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *

unix_bufferoverflow_functions = (
    "strcpy",
    "strcat",
    "sprintf",
    "vsprintf",
    "gets",
    "realpath",
    "getopt",
    "getpass",
    "streadd",
    "strecpy",
    "strtrns",
)


def RunRule(lexer, contextStack):
    # Boost.Format, Folly.Format don't provide printf but if they do,
    # that can be handled by adding (or others) to whitelist
    whitelist = ["fmt"]
    blacklist = ["std", ""]  # to catch ::printf

    t = lexer.GetCurToken()
    if t.type == "ID" and t.value in unix_bufferoverflow_functions:
        t2 = lexer.PeekNextTokenSkipWhiteSpaceAndComment()
        if t2 is not None and t2.type == "LPAREN":
            t3 = lexer.PeekPrevTokenSkipWhiteSpaceAndComment()
            # tribool state: safe, unsafe, unknown
            safe_alternative = False
            unsafe_alternative = False
            if t3 is None:
                # C style usage: flat out error
                unsafe_alternative = True
            elif t3.type == "PERIOD":
                # class member: the call is safe, impl might not be
                safe_alternative = True
            elif t3.type == "DOUBLECOLON":
                # check the namespace to classify as a dangerous
                # usage or a safe usage
                prev_namespace_token = lexer.GetPrevTokenInType("ID", keepCur=True)
                if prev_namespace_token.value in whitelist:
                    safe_alternative = True
                elif prev_namespace_token.value in blacklist:
                    unsafe_alternative = True
                # elif unknown namespace => unknown safety
            if unsafe_alternative:
                nsiqcppstyle_reporter.Error(t, __name__, "Do not use bufferoverflow risky function(%s)" % t.value)
            elif not safe_alternative:
                nsiqcppstyle_reporter.Error(
                    t,
                    __name__,
                    "Caution: Uknown imlementation of a bufferoverflow risky function(%s)" % t.value,
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
void func1()
{
    k = strcat()
}
""",
        )
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze(
            "thisfile.c",
            """

void func1() {
#define strcat() k
}
""",
        )
        self.ExpectSuccess(__name__)

    def test3(self):
        self.Analyze(
            "thisfile.c",
            """
void strcat() {
}
""",
        )
        self.ExpectSuccess(__name__)

    def test4(self):
        self.Analyze(
            "thisfile.c",
            """
void strcat () {
}
""",
        )
        self.ExpectSuccess(__name__)

    def test5(self):
        self.Analyze(
            "thisfile.c",
            """
void func1()
{
    k = help.strcat ()
}
""",
        )
        self.ExpectSuccess(__name__)

    def test6(self):
        self.Analyze(
            "thisfile.c",
            """
void func1()
{
    k = fmt::strcat ()
}
""",
        )
        self.ExpectSuccess(__name__)

    def test7(self):
        self.Analyze(
            "thisfile.c",
            """
void func1()
{
    k = std::strcat ()
}
""",
        )
        self.ExpectError(__name__)

    def test8(self):
        self.Analyze(
            "thisfile.c",
            """
void func1()
{
    k = random::strcat ()
}
""",
        )
        self.ExpectError(__name__)

    def test9(self):
        self.Analyze(
            "thisfile.c",
            """
void func1()
{
    k = ::strcat ()
}
""",
        )
        self.ExpectError(__name__)

    def test10(self):
        # known issue. Not a problem
        self.Analyze(
            "thisfile.c",
            """
#define strcat k
void func1()
{
    p = k()
}
""",
        )
        self.ExpectSuccess(__name__)
