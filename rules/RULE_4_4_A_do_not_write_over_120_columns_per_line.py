"""
Do not write over 120 columns per a line.
This rule doesn't recognize tabs. It only think each character as 1 column.

== Violation ==

    int HEEEEEEEEEEEEEEEEEEELLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO = 1;
    <== Violation. Too long

== Good ==

    int K; <== OK. It's short.
"""
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, line, lineno):
    if not Match(r"^\s*$", line):
        if len(line) > 120:
            nsiqcppstyle_reporter.Error(
                DummyToken(lexer.filename, line, lineno, 0),
                __name__,
                "Lines should very rarely be longer than 120 characters",
            )
        else:
            # add code to recognise tabs as charachters
            pass


ruleManager.AddLineRule(RunRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddLineRule(RunRule)

    def test1(self):
        self.Analyze(
            "test/thisFile.c",
            """
void function(int k, int j, int pp)
{
%s
}
"""
            % ("d" * 121),
        )
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze(
            "test/thisFile.c",
            """
void function(int k, int j, int pp)
{{
{}
{}
}}
""".format(
                "d" * 119,
                " " * 130,
            ),
        )
        self.ExpectSuccess(__name__)
