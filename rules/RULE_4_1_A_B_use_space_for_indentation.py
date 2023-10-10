"""
Use spaces for indentation.
This rule ensures that each line starts with spaces.
In addition, it suppresses the violation when the line contains only spaces and tabs.

== Violation ==

    void Hello()
    {
    [TAB]         <== Don't care if the line is empty
    [TAB]Hello(); <== Violation. A tab is used for indentation.
    }

== Good ==

    void Hello()
    {
    [TAB] <== Don't care.
    [SPACE][SPACE]Hello(); <== Good. Spaces are used for indentation.
    }

"""
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqcppstyle_types import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer: Lexer, line: LineText, lineno: LineNumber) -> None:
    t = lexer.GetCurToken()

    # Skip comment lines
    if t.type in ["COMMENT", "CPPCOMMENT"]:
        next_token = lexer.GetNextTokenSkipWhiteSpaceAndComment()
        if next_token.lineno != t.lineno:
            return

    if not Match(r"^\s*$", line) and Search("^\t", line):
        nsiqcppstyle_reporter.Error(
            DummyToken(lexer.filename, line, lineno, 0),
            __name__,
            "Do not use tab for indent",
        )


ruleManager.AddLineRule(RunRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddLineRule(RunRule)

    def test1(self):
        self.Analyze("test/thisFile.c", "\tbool CanHave() {\n\t}")
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze(
            "test/thisFile.c",
            """
class K {
    Hello
}""",
        )
        self.ExpectSuccess(__name__)

    def test3(self):
        self.Analyze(
            "test/thisFile.c",
            """
class K {

Hello
}""",
        )
        self.ExpectSuccess(__name__)

    def test4(self):
        self.Analyze(
            "test/thisFile.c",
            """
 /**
\t* Check for Doxygen Comment. This rule doesn't care about doxygen comment block.
  */
class K {

Hello
}""",
        )
        self.ExpectSuccess(__name__)
