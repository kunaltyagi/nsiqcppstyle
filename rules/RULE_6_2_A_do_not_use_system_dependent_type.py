"""
Do not use system dependent types (short, long, int).
Instead use system independent types (int16_t, int64_t, int32_t) respectively.

== Violation ==

    int k;
    short b;
    long t;

== Good ==

    int32_t b;
"""
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *

systemDependentType = {"SHORT": "int16_t", "LONG": "int64_t", "INT": "int32_t"}


def RunRule(lexer, contextStack):
    t = lexer.GetCurToken()
    if t.type in ["SHORT", "LONG", "INT"]:
        context = contextStack.Peek()
        if context is None or context.type != "PARENBLOCK":
            nsiqcppstyle_reporter.Error(
                t,
                __name__,
                "Do not use system dependent type({}). Use system independent type like ({})".format(
                    t.value,
                    systemDependentType[t.type],
                ),
            )


ruleManager.AddRule(RunRule)


##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddRule(RunRule)

    def test1(self):
        self.Analyze(
            "thisfile.c",
            """
int k;
""",
        )
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze(
            "thisfile.c",
            """
void T() {
    long long k = 1;
}
""",
        )
        self.ExpectError(__name__)

    def test3(self):
        self.Analyze(
            "thisfile.c",
            """
int32_t k = 2
""",
        )
        self.ExpectSuccess(__name__)

    def test4(self):
        self.Analyze(
            "thisfile.c",
            """
void k() {
    for (int j = 0; j < 11; j++) {
    }
}
""",
        )
        self.ExpectSuccess(__name__)
