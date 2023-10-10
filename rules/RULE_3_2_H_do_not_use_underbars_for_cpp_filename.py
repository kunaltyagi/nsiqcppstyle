"""
Do not use unberbars for cpp filename.

Only alphabets, numbers can be used for a cpp filename.

== Vilolation ==

    /testdir/test_1.cpp <== Violation. - is used.
    /testdir1/_test1.cxx <== Violation. _ is used
    /testdir/test_1.cc <== Violation. - is used.
    /testdir1/_test1.mm <== Violation. _ is used

== Good ==

    testdir/test.cpp
    testdir/test.cxx
    testdir/test.cc
    testdir/test.mm
    testdir1/test_1.c <== Don't care. it's c file.
"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, filename, dirname):
    if Search("[_]", filename) and filename[filename.rfind(".") :] in (".cpp", ".cxx", ".cc", ".mm"):
        nsiqcppstyle_reporter.Error(
            DummyToken(lexer.filename, "", 0, 0),
            __name__,
            "Do not use underbar for cpp file name (%s)." % filename,
        )


ruleManager.AddFileStartRule(RunRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddFileStartRule(RunRule)

    def test1(self):
        self.Analyze("test/thisfile.cpp", "")
        self.ExpectSuccess(__name__)

    def test2(self):
        self.Analyze("test/this_file.c", "")
        self.ExpectSuccess(__name__)

    def test3(self):
        self.Analyze("test/thisfile.cxx", "")
        self.ExpectSuccess(__name__)

    def test4(self):
        self.Analyze("test/thisfile.cc", "")
        self.ExpectSuccess(__name__)

    def test5(self):
        self.Analyze("test/thisfile.mm", "")
        self.ExpectSuccess(__name__)

    def test6(self):
        self.Analyze("test/this_file.cxx", "")
        self.ExpectError(__name__)

    def test7(self):
        self.Analyze("test/this_file.cpp", "")
        self.ExpectError(__name__)

    def test8(self):
        self.Analyze("test/this_file.cc", "")
        self.ExpectError(__name__)

    def test9(self):
        self.Analyze("test/this_file.mm", "")
        self.ExpectError(__name__)
