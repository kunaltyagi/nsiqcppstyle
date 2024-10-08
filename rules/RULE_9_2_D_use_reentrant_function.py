"""
Use reentrant functions. Do not use not reentrant functions.(ctime, strtok, toupper)

== Violation ==

  void A() {
      k = ctime();   <== Violation. ctime() is not the reenterant function.
      j = strok(blar blar); <== Violation. strok() is not the reenterant function.
  }

== Good ==

  void A() {
      k = t.ctime(); <== Correct. It may be the reentrant function.
  }

  void A() {
      k = ctime;     <==  Correct. It may be the reentrant function.
  }
"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *

no_reenterant_functions = (
    "ctime",
    "strtok",
    "toupper",
)


def RunRule(lexer, contextStack):
    """
    Use reenterant keyword.
    """
    t = lexer.GetCurToken()
    if t.type == "ID" and t.value in no_reenterant_functions:
        t2 = lexer.PeekNextTokenSkipWhiteSpaceAndComment()
        t3 = lexer.PeekPrevTokenSkipWhiteSpaceAndComment()
        if t2 is not None and t2.type == "LPAREN" and (t3 is None or t3.type != "PERIOD"):
            if (
                t.value == "toupper"
                and nsiqcppstyle_state._nsiqcppstyle_state.GetVar("ignore_toupper", "false") == "true"
            ):
                return
            nsiqcppstyle_reporter.Error(t, __name__, f"Do not use not reentrant function({t.value}).")


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
    k = ctime()
}
""",
        )
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze(
            "thisfile.c",
            """

void func1() {
#define ctime() k
}
""",
        )
        self.ExpectSuccess(__name__)

    def test3(self):
        self.Analyze(
            "thisfile.c",
            """
void ctime() {
}
""",
        )
        self.ExpectSuccess(__name__)

    def test4(self):
        self.Analyze(
            "thisfile.c",
            """
void ctime () {
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
    k = help.ctime ()
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
    k = toupper()
}
""",
        )
        self.ExpectError(__name__)

    def test7(self):
        nsiqcppstyle_state._nsiqcppstyle_state.varMap["ignore_toupper"] = "true"
        self.Analyze(
            "thisfile.c",
            """
void func1()
{
    k = toupper()
}
""",
        )
        self.ExpectSuccess(__name__)
