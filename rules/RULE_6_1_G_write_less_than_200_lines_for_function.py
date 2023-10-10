"""
Do not write more than 200 lines for a function.
It's really hard to detect comment line with keeping enough speed.
So it only counts non blank line.

== Violation ==

    void f() {
    -- more than 200 non blank lines <== Violated
    }

== Good ==

    void f() {
    -- more than 120 non blank lines <== OK
    }

"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, fullName, decl, contextStack, context):
    if not decl and context is not None:
        startline = context.startToken.lineno
        endline = context.endToken.lineno
        count = 0
        for eachLine in lexer.lines[startline - 1 : endline - 1]:
            if not Match(r"^\s*$", eachLine):
                count += 1
        if count > 200:
            nsiqcppstyle_reporter.Error(
                context.startToken,
                __name__,
                "Do not write function over non blank 200 lines(%s)." % fullName,
            )


ruleManager.AddFunctionNameRule(RunRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddFunctionNameRule(RunRule)

    def test1(self):
        self.Analyze("thisfile.c", "int k() {%s};" % ("hello\n\n" * 201))
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze("thisfile.c", "int k() {%s};" % ("hello\n\n" * 120))
        self.ExpectSuccess(__name__)

    def test3(self):
        self.Analyze("thisfile.c", "int k() {%s};" % ("hello\n\n" * 200))
        self.ExpectSuccess(__name__)
