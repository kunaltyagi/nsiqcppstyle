# Copyright (c) 2022 All rights reserved.
# SPDX-License-Identifier: GPL-2.0-only
from nsiqcppstyle_rulemanager import *
from nsiqcppstyle_types import *

def PrintContextStack(contextStack: ContextStack, isLastParameter: bool):
    appendString = ''
    if isLastParameter:
        appendString = ')'
    else:
        appendString = ','
    indent_string = (15 * ' ')

    if (contextStack is None) or (contextStack.contextstack is None) or (len(contextStack.contextstack) == 0):
        print("%scontextStack (empty)%s" % (indent_string, appendString))
    else:
        print("%scontextStack (%d)%s" % (indent_string, len(contextStack.contextstack), appendString))
        for t in contextStack.contextstack:
            print('%s    %s' % (indent_string, str(t)))

def FunctionScopeRule(lexer, contextStack):
    print("FunctionScope (lexer, ")
    PrintContextStack(contextStack, True)

def FunctionNameRule(lexer, fullName, decl, contextStack, context):
    print("FunctionName  (lexer,")
    print("               fullName='%s'," % (fullName))
    print("               decl='%s'," % (decl))
    PrintContextStack(contextStack, False)
    print("                   context='%s')" % (str(context)))


def PreprocessRule(lexer, contextStack):
    print("Preprocess    (lexer,")
    PrintContextStack(contextStack, False)
    print("               token=%s)" % (lexer.GetCurToken()))

def CommentRule(lexer, token):
    print("Comment       (lexer, token=%s)" % (lexer.GetCurToken()))

def LineRule(lexer, line, lineNumber):
    print("--------------------------------------------------")
    print("Line          (lexer, line='%s', lineNumber=%d)" % (line, lineNumber))

def TokenRule(lexer, contextStack):
    print("Token         (lexer,")
    PrintContextStack(contextStack, False)
    print("               token=%s)" % (lexer.GetCurToken()))

def FileStartRule(lexer, filename, dirname):
    print("FileStart     (lexer, filename='%s', dirname='%s')" % (filename, dirname))

def FileEndRule(lexer, filename, dirname):
    print("FileEnd       (lexer, filename='%s', dirname='%s')" % (filename, dirname))

def ProjectRule(targetName):
    print("Project       (targetName='%s')" % (targetName))

def TypeNameRule(lexer, typeName, typeFullName, decl, contextStack, typeContext):
    print("TypeName      (lexer,")
    print("               typeName='%s'," % (typeName))
    print("               typeFullName='%s'," % (typeFullName))
    print("               decl='%s'" % (decl))
    PrintContextStack(contextStack, False)
    print("               typeContext='%s')" % (str(typeContext)))

def TypeScopeRule(lexer, contextStack):
    print("TypeScope     (lexer, ")
    PrintContextStack(contextStack, True)

def SessionStartRule():
    # Print instructions, legend, etc. to help the developer
    print("Legend: LexToken contain six fields: (type, value, lineno, column, lexpos, inactive, pp)")
    print("")
    print("SessionStart  ()")

def SessionEndRule():
    print("SessionEnd    ()")

ruleManager.AddFunctionScopeRule(FunctionScopeRule)
ruleManager.AddFunctionNameRule(FunctionNameRule)
ruleManager.AddPreprocessRule(PreprocessRule)
ruleManager.AddCommentRule(CommentRule)
ruleManager.AddLineRule(LineRule)
ruleManager.AddRule(TokenRule)
ruleManager.AddFileStartRule(FileStartRule)
ruleManager.AddFileEndRule(FileEndRule)
ruleManager.AddProjectRules(ProjectRule)
ruleManager.AddTypeNameRule(TypeNameRule)
ruleManager.AddTypeScopeRule(TypeScopeRule)
ruleManager.AddSessionStartRule(SessionStartRule)
ruleManager.AddSessionEndRule(SessionEndRule)
