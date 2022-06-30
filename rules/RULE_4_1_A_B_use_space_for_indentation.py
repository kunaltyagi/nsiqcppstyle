"""
Use spaces for indentation.
This rule check if the each line starts with tabs.
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
from nsiqunittest.nsiqcppstyle_unittestbase import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulemanager import *
from nsiqcppstyle_types import *


def RunRule(lexer: LexerType, line: LineType, lineno: LineNumberType):
    if not Match(r"^\s*$", line):
        if Search("^\t", line):
            nsiqcppstyle_reporter.Error(DummyToken(
                lexer.filename, line, lineno, 0), __name__, "Do not use tab for indent")


ruleManager.AddLineRule(RunRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddLineRule(RunRule)

    def test1(self):
        self.Analyze("test/thisFile.c",
                     "\tbool CanHave() {\n\t}")
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze("test/thisFile.c",
                     """
class K {
    Hello
}""")
        self.ExpectSuccess(__name__)

    def test3(self):
        self.Analyze("test/thisFile.c",
                     """
class K {

Hello
}""")
        self.ExpectSuccess(__name__)
