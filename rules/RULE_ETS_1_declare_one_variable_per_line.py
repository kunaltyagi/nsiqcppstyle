"""
Declare one variable per line.


== Violation ==

    void functionA()
    {
        int a, b; <== Violation.
     }

    void functionB()
    {
        int x;
        if(x==10){
            int a, b;<== Violation.
        }
     }

== Good ==

    void functionA(){
        int a,
            b; <== OK
    }

"""
from nsiqunittest.nsiqcppstyle_unittestbase import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulemanager import *

base_types = ("CHAR",
              "INT",
              "LONG",
              "DOUBLE",
              "FLOAT",
              "SHORT",
              "BOOL",
              "VOID")


def consume_all_stars(lexer):
    t = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess()

    while t.type == "TIMES":
        lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
        t = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess()

def RunRule(lexer, contextStack):
    global base_types
    t = lexer.GetCurToken()
    if t != "ID":
        return

    consume_all_stars(lexer)

    t2 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
    t3 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()

    if t2 != "ID":
        return

    if t3 != "COMMA":
        return

    # check if we're in a function prototype
    counter = 0
    t2 = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
    while t2 is not None:
        if t2.type == "RPAREN":
            return
        if t2.type == "SEMI":
            break
        counter += 1
        t2 = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess(counter)

    """    
    nt1 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
    if (t.type in base_types or t.type == "ID") and nt1.type == "TIMES":
        while nt1.type == "TIMES":
            nt1 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
    if (t.type in base_types or t.type == "ID") and nt1.type == "ID":
        # we got a variable declaration, let's see if it's followed by a comma
        last_variable_line = nt1.lineno
        nt2 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
        nt3 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
        nt4 = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
        while nt2.type == "COMMA" and nt3.type == "ID" and nt4.type not in ("ID", "TIMES"):
            if nt3.lineno == last_variable_line:
                nsiqcppstyle_reporter.Error(
                    nt3, __name__, "Variable {} on line {} should be declared on a separate line".format(nt3.value, nt3.lineno))
            last_variable_line = nt3.lineno
            nt2 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
            nt3 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
            nt4 = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
    """


ruleManager.AddRule(RunRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddRule(RunRule)

    def test1(self):
        self.Analyze("test/thisFile.c",
                     """
void function(int k, int j, int pp)
{
    int a, 
        b,
        c;
}
""")
        self.ExpectSuccess(__name__)

    def test2(self):
        self.Analyze("test/thisFile.c",
                     """
void function(int k, int j, int pp)
{
    int a, b, c;
}
""")
        self.ExpectError(__name__)

    def test3(self):
        self.Analyze("test/thisFile.c",
                     """
void function(int k, int j, int pp)
{
    int *a, 
        b, c;
}
""")
        self.ExpectError(__name__)

    def test4(self):
            self.Analyze("test/thisFile.c",
                         """
void function(int k, int j, int pp)
{
       void a, *b;
}
""")
            self.ExpectError(__name__)
