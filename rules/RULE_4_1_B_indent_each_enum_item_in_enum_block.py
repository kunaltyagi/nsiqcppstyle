"""
Indent the each enum item in the enum block.

== Violation ==

    enum A {
    A_A,  <== Violation
    A_B   <== Violation
    }


== Good ==

    enum A {
        A_A,     <== Good
        A_B
    }
"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, typeName, typeFullName, decl, contextStack, typeContext):
    if not decl and typeName == "ENUM" and typeContext is not None:
        column = GetIndentation(lexer.GetCurToken())
        lexer._MoveToToken(typeContext.startToken)
        t2 = typeContext.endToken
        while True:
            t = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
            if t is None or t == t2:
                break
            #            if typeContext != t.contextStack.Peek() : continue
            if GetRealColumn(t) <= (column + 1):
                nsiqcppstyle_reporter.Error(
                    t,
                    __name__,
                    f"Enum block should be indented. But the token({t.value}) seems to be unindented",
                )


ruleManager.AddTypeNameRule(RunRule)


##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddTypeNameRule(RunRule)

    def test1(self):
        self.Analyze(
            "test/thisFile.c",
            """
enum A {
}
""",
        )
        self.ExpectSuccess(__name__)

    def test2(self):
        self.Analyze(
            "test/thisFile.c",
            """
enum C {
    AA, BB
}
""",
        )
        self.ExpectSuccess(__name__)

    def test3(self):
        self.Analyze(
            "test/thisFile.c",
            """
enum C {
AA = 4,
    BB
}
""",
        )
        self.ExpectError(__name__)

    def test4(self):
        self.Analyze(
            "test/thisFile.c",
            """
enum C {
    AA = 4
,BB
}
""",
        )
        self.ExpectError(__name__)

    def test5(self):
        self.Analyze(
            "test/thisFile.c",
            """
enum C {
    AA = 4
/** HELLO */
    ,BB
}
""",
        )
        self.ExpectSuccess(__name__)

    def test6(self):
        self.Analyze(
            "test/thisFile.c",
            """
typedef enum  {
    AA = 4
/** HELLO */
    ,BB
} DD
""",
        )
        self.ExpectSuccess(__name__)

    def test7(self):
        self.Analyze(
            "test/thisFile.c",
            """
typedef enum
{
  SERVICE,
  SERVER,
  BROKER,
  MANAGER,
  REPL_SERVER,
  REPL_AGENT,
  UTIL_HELP,
  UTIL_VERSION,
  ADMIN
} UTIL_SERVICE_INDEX_E;
""",
        )
        self.ExpectSuccess(__name__)

    def test8(self):
        self.Analyze(
            "test/thisFile.c",
            """
enum COLOR
{
        COLOR_TRANSPARENT = RGB(0, 0, 255),
        COLOR_ROOM_IN_OUT = 0xffff00,
        COLOR_CHAT_ITEM = 0xff9419,
        COLOR_CHAT_MY = 0x00b4ff,
        COLOR_CHAT_YOUR = 0xa3d5ff,
        COLOR_ROOM_INFO = 0x00ffff,
        COLOR_RESULT_SCORE = 0xffcc00,
        COLOR_RESULT_RATING = 0x00fcff,
        COLOR_RESULT_POINT = 0x33ff00
}; """,
        )
        self.ExpectSuccess(__name__)
