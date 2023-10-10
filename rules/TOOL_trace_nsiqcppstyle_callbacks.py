# Copyright (c) 2022 All rights reserved.
# SPDX-License-Identifier: GPL-2.0-only
from nsiqcppstyle_rulemanager import *
from nsiqcppstyle_types import *


def PrintContextStack(contextStack: ContextStack, isLastParameter: bool):
    appendString = ""
    appendString = ")" if isLastParameter else ","
    indentString = 15 * " "

    if (contextStack is None) or (contextStack.contextstack is None) or (len(contextStack.contextstack) == 0):
        print(f"{indentString}contextStack (empty){appendString}")
    else:
        print(f"{indentString}contextStack ({len(contextStack.contextstack)}){appendString}")
        for t in contextStack.contextstack:
            print(f"{indentString}    {t!s}")


def FunctionScopeRule(lexer, contextStack):
    print("FunctionScope (lexer, ")
    PrintContextStack(contextStack, True)


def FunctionNameRule(lexer, fullName, decl, contextStack, context):
    print("FunctionName  (lexer,")
    print(f"               fullName='{fullName}',")
    print(f"               decl='{decl}',")
    PrintContextStack(contextStack, False)
    print(f"                   context='{context!s}')")


def PreprocessRule(lexer, contextStack):
    print("Preprocess    (lexer,")
    PrintContextStack(contextStack, False)
    print(f"               token={lexer.GetCurToken()})")


def CommentRule(lexer, token):
    print(f"Comment       (lexer, token={lexer.GetCurToken()})")


def LineRule(lexer, line, lineNumber):
    print("--------------------------------------------------")
    print(f"Line          (lexer, line='{line}', lineNumber={lineNumber})")


def TokenRule(lexer, contextStack):
    print("Token         (lexer,")
    PrintContextStack(contextStack, False)
    print(f"               token={lexer.GetCurToken()})")


def FileStartRule(lexer, filename, dirname):
    print(f"FileStart     (lexer, filename='{filename}', dirname='{dirname}')")


def FileEndRule(lexer, filename, dirname):
    print(f"FileEnd       (lexer, filename='{filename}', dirname='{dirname}')")


def ProjectRule(targetName):
    print(f"Project       (targetName='{targetName}')")


def TypeNameRule(lexer, typeName, typeFullName, decl, contextStack, typeContext):
    print("TypeName      (lexer,")
    print(f"               typeName='{typeName}',")
    print(f"               typeFullName='{typeFullName}',")
    print(f"               decl='{decl}'")
    PrintContextStack(contextStack, False)
    print(f"               typeContext='{typeContext!s}')")


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
