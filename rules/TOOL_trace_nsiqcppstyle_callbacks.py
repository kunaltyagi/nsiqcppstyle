from nsiqcppstyle_rulemanager import *
import nsiqcppstyle_types

def PrintContextStack(contextStack):
    if (contextStack != None) and (contextStack.contextstack != None) and (len(contextStack.contextstack) > 0):
        indent_string = (20 * ' ')
        print("%sContext stack (%d):" % (indent_string, len(contextStack.contextstack)))
        for t in contextStack.contextstack:
            print('%s    %s' % (indent_string, str(t)))

def FunctionScopeRule(lexer, contextStack):
    print("FunctionScopeRule (lexer, contextStack)")
    PrintContextStack(contextStack)

def FunctionNameRule(lexer, fullName, decl, contextStack, context):
    print("FunctionNameRule  (lexer,")
    print("                   fullName='%s'," % (fullName))
    print("                   decl='%s'," % (decl))
    print("                   contextStack,")
    print("                   context='%s')" % (str(context)))
    PrintContextStack(contextStack)


def PreprocessRule(lexer, contextStack):
    print("PreprocessRule    (lexer,")
    print("                   contextStack,")
    print("                   token=%s" % (lexer.GetCurToken()))
    PrintContextStack(contextStack)

def CommentRule(lexer, token):
    print("CommentRule       (lexer, token=%s)" % (lexer.GetCurToken()))

def LineRule(lexer, line, lineNumber):
    print("--------------------------------------------------")
    print("LineRule          (lexer, line='%s', lineNumber=%d)" % (line, lineNumber))

def TokenRule(lexer, contextStack):
    print("TokenRule         (lexer,")
    print("                   contextStack,")
    print("                   token=%s)" % (lexer.GetCurToken()))
    PrintContextStack(contextStack)

def FileStartRule(lexer, filename, dirname):
    print("FileStartRule     (lexer, filename='%s', dirname='%s')" % (filename, dirname))

def FileEndRule(lexer, filename, dirname):
    print("FileEndRule       (lexer, filename='%s', dirname='%s')" % (filename, dirname))

def ProjectRule(targetName):
    print("ProjectRule       (targetName='%s')" % (targetName))

def TypeNameRule(lexer, typeName, typeFullName, decl, contextStack, typeContext):
    print("TypeNameRule      (lexer, typeName='%s', typeFullName='%s', decl='%s')" % (typeName, typeFullname, decl))
    PrintContextStack(contextStack)

def TypeScopeRule(lexer, contextStack):
    print("TypeScopeRule     (lexer, contextStack)")
    PrintContextStack(contextStack)

def SessionStartRule():
    # Print instructions, legend, etc. to help the developer
    print("Legend: LexToken contain six fields: (type, value, lineno, column, lexpos, inactive, pp)")
    print("")
    print("SessionStartRule  ()")

def SessionEndRule():
    print("SessionEndRule    ()")

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
