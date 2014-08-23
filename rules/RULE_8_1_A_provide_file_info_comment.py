"""
Provide file comment.

File comment including 'copyright' should be provided in the head of file.
This rule detect following style file comment.

== Violation ==

    = start of file =
    #define "AA" <== Violation. file comment should be the first element of file.
    ///
    /// blar blar
    /// Copyright reserved.
    ///

    = start of file =
    /**         <== Violation. No copyright string.
     * blar blar
     * blar blar
     */

== Good ==

    = start of file =
    ///
    /// blar blar
    /// Copyright reserved. <== Correct
    /// file
    /// author
    /// date
    /// version
    /// brief
    ///

    = start of file =
    /**
     * blar blar
     * Copyright reserved. <== Correct
     * file
     * author
     * date
     * version
     * brief
     * blar blar
     */
"""
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulemanager import *

def error(lexer):
    nsiqcppstyle_reporter.Error(DummyToken(lexer.filename, "", 1, 0),
            __name__, """Please provide file info comment in front of
            file. It includes license/copyright information along
            with filename, author, date of modification, version and
            a brief description""")

def RunRule(lexer, filename, dirname) :

    t = lexer.GetNextTokenSkipWhiteSpace()
    if t == None : return
    if t.type in ("COMMENT", "CPPCOMMENT") :
        find = False
        while(t != None and t.type == "CPPCOMMENT") :
            if t.value.lower().find("copyright") != -1 or t.value.lower().find("license") != -1:
                find = True
                break;
            t = lexer.GetNextTokenSkipWhiteSpace()
        if not find :
            error(lexer)
    else :
        error(lexer)

ruleManager.AddFileStartRule(RunRule)

###########################################################################################
# Unit Test
###########################################################################################

from nsiqunittest.nsiqcppstyle_unittestbase import *
class testRule(nct):
    def setUpRule(self):
        ruleManager.AddFileStartRule(RunRule)
    def test1(self):
        self.Analyze("thisfile.c","""
// license
// copyright
""")
        assert not CheckErrorContent(__name__)
    def test2(self):
        self.Analyze("thisfile.c", """
/**
#if 0
#endif
license
coryright */ """)
        assert CheckErrorContent(__name__)
    def test3(self):
        self.Analyze("thisfile.c","""

// license
// copyrigh1
""")
        assert CheckErrorContent(__name__)
    def test4(self):
        self.Analyze("thisfile.c","""
#define "WEWE"
// license
// copyrigh1
#include </ewe/kk> """)
        assert  CheckErrorContent(__name__)
    def test5(self):
        self.Analyze("thisfile.c","""
#define "WEWE"
// license
// copyright
#include </ewe/kk> """)
        assert CheckErrorContent(__name__)
    def test6(self):
        self.Analyze("thisfile.c","""
// license
// copyright
#define "WEWE"
#include </ewe/kk> """)
        assert not CheckErrorContent(__name__)

