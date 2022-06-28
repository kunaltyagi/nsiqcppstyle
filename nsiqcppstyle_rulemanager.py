# Copyright (c) 2009 NHN Inc. All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#    * Neither the name of NHN Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os  # @UnusedImport
import sys  # @UnusedImport
import sre_compile
from nsiqcppstyle_outputer import _consoleOutputer as console
from nsiqcppstyle_util import *  # @UnusedWildImport


class RuleManager:
    def __init__(self, runtimePath):
        self.availRuleNames = []
        basePath = os.path.join(runtimePath, "rules")
        ruleFiles = os.listdir(basePath)
        rulePattern = sre_compile.compile(r"^(.*)\.py$")
        for eachRuleFile in ruleFiles:
            if os.path.isfile(os.path.join(basePath, eachRuleFile)):
                ruleMatch = rulePattern.match(eachRuleFile)
                if ruleMatch is not None and eachRuleFile.find(
                        "__init__") == -1:
                    ruleName = ruleMatch.group(1)
                    self.availRuleNames.append(ruleName)
        self.availRuleCount = len(self.availRuleNames)
        self.availRuleModules = {}
        self.loadedRule = []
        self.rules = []
        self.preprocessRules = []
        self.commentRules = []
        self.functionNameRules = []
        self.functionScopeRules = []
        self.typeNameRules = []
        self.typeScopeRules = []
        self.lineRules = []
        self.fileEndRules = []
        self.fileStartRules = []
        self.sessionEndRules = []
        self.sessionStartRules = []
        self.projectRules = []
        self.rollBackImporter = None
#       self.LoadAllRules()

    def LoadRules(self, checkingRuleNames):
        """
        Load Rules. It resets rule before loading rules
        """
        self.ResetRules()
        self.ResetRegisteredRules()
        if self.rollBackImporter is not None:
            self.rollBackImporter.uninstall()

        self.rollBackImporter = RollbackImporter()
        console.Out.Ci(console.Separator)

        for ruleName in checkingRuleNames:
            count = self.availRuleNames.count(ruleName)
            if count == 0:
                console.Out.Error(
                    "%s does not exist or incompatible." % ruleName)
                continue
            else:
                console.Out.Info("  - ", ruleName, "is applied.")
            ruleModule = __import__("rules." + ruleName)
            self.loadedRule.append(ruleModule)
        if len(self.loadedRule) == 0:
            console.Out.Ci(
                "  No Rule is specified. Please configure rules in filefilter.txt.")
        console.Out.Ci(console.Separator)

    def ResetRules(self):
        self.loadedRule = []

    ##########################################################################
    # Rule Runner
    ##########################################################################
    def RunPreprocessRule(self, lexer, contextStack):
        """ Run rules which runs in the preprecessor blocks """
        for preprocessRule in self.preprocessRules:
            data = lexer.Backup()
            preprocessRule(lexer, contextStack)
            lexer.Restore(data)

    def RunCommentRule(self, lexer, token):
        """ Rule when a comment is encountered """
        for eachCommentRule in self.commentRules:
            data = lexer.Backup()
            eachCommentRule(lexer, token)
            lexer.Restore(data)

    def RunFunctionNameRule(self, lexer, functionFullName,
                            decl, contextStack, functionContext):
        """ Run rules which runs on the function name """
        for eachFunctionNameRule in self.functionNameRules:
            data = lexer.Backup()
            eachFunctionNameRule(lexer, functionFullName,
                                 decl, contextStack, functionContext)
            lexer.Restore(data)

    def RunFunctionScopeRule(self, lexer, contextStack):
        """ Run rules which runs in the function blocks """
        for eachFunctionScopeRule in self.functionScopeRules:
            data = lexer.Backup()
            eachFunctionScopeRule(lexer, contextStack)
            lexer.Restore(data)

    def RunTypeNameRule(self, lexer, typeName, typeFullName,
                        decl, contextStack, typeContext):
        """ Run rules which runs on the type names """
        for typeNameRule in self.typeNameRules:
            data = lexer.Backup()
            typeNameRule(lexer, typeName, typeFullName,
                         decl, contextStack, typeContext)
            lexer.Restore(data)

    def RunTypeScopeRule(self, lexer, contextStack):
        """ Run rules which runs in the type blocks """
        for typeScopeRule in self.typeScopeRules:
            data = lexer.Backup()
            typeScopeRule(lexer, contextStack)
            lexer.Restore(data)

    def RunRule(self, lexer, contextStack):
        """ Run rules which runs in any tokens """
        for rule in self.rules:
            data = lexer.Backup()
            rule(lexer, contextStack)
            lexer.Restore(data)

    def RunLineRule(self, lexer, line, lineno):
        """ Run rules which runs in each lines. """
        for lineRule in self.lineRules:
            data = lexer.Backup()
            lineRule(lexer, line, lineno)
            lexer.Restore(data)

    def RunFileEndRule(self, lexer, filename, dirname):
        """ Run rules which runs at the end of files. """
        for fileEndRule in self.fileEndRules:
            data = lexer.Backup()
            fileEndRule(lexer, filename, dirname)
            lexer.Restore(data)

    def RunFileStartRule(self, lexer, filename, dirname):
        """ Run rules which runs at the start of files. """
        for fileStartRule in self.fileStartRules:
            data = lexer.Backup()
            fileStartRule(lexer, filename, dirname)
            lexer.Restore(data)

    def RunSessionEndRules(self):
        """ Run rules which runs at the end of the script session. """
        for sessionEndRule in self.sessionEndRules:
            sessionEndRule()

    def RunSessionStartRules(self):
        """ Run rules which runs at the start of the script session. """
        for sessionStartRule in self.sessionStartRules:
            sessionStartRule()

    def RunProjectRules(self, targetName):
        """ Run rules which runs once a project. """
        for projectRule in self.projectRules:
            projectRule(targetName)

    ##########################################################################
    # Rule Resister Methods
    ##########################################################################

    def ResetRegisteredRules(self):
        """ Reset all registered rules. """
        del self.functionNameRules[:]
        del self.functionScopeRules[:]
        del self.lineRules[:]
        del self.rules[:]
        del self.typeNameRules[:]
        del self.typeScopeRules[:]
        del self.fileStartRules[:]
        del self.fileEndRules[:]
        del self.sessionStartRules[:]
        del self.sessionEndRules[:]
        del self.projectRules[:]
        del self.preprocessRules[:]
        del self.commentRules[:]

    def AddPreprocessRule(self, preprocessRule):
        """
        Add rule which runs in preprocess statements
        Added rule should be function with following prototype:
            def RunRule(lexer, contextStack)
                lexer is the lexer used to analyze the source, it points the start token of source.
                contextStack is a stack showing the lexical context the token resides in
        """
        self.preprocessRules.append(preprocessRule)

    def AddCommentRule(self, commentRule):
        """
        Add rule which runs when a comment is encountered
        Added rule should be function with following prototype:
            def RunRule(lexer, token)
                lexer is the lexer used to analyze the source, it points the start token of source.
                token is the current token being processed
        """
        self.commentRules.append(commentRule)

    def AddFunctionScopeRule(self, functionScopeRule):
        """
        Add rule which runs in function scope
        Added rule should be function with following prototype:
            def RunRule(lexer, contextStack)
                lexer is the lexer used to analyze the source, it points the start token of source.
                contextStack is a stack showing the lexical context the token resides in
        """
        self.functionScopeRules.append(functionScopeRule)

    def AddFunctionNameRule(self, functionRule):
        """
        Add rule on the function name place
        Added rule should be function with following prototype:
            def RunRule(lexer, fullName, decl, contextStack, context)
                lexer is the lexer used to analyze the source, it points the start token of source.
                fullName is the full function name (e.g., foo::bar)
                decl is a boolean flag denoting whether the function is a declaration (True) or
                     definition (False)
                contextStack is a stack showing the lexical context the token resides in
                context is the new context entry that will be pushed to the contextStack due to this token
        """
        self.functionNameRules.append(functionRule)

    def AddLineRule(self, lineRule):
        """
        Add rule on the each line
        Added rule should be function with following prototype:
            def RunRule(lexer, line, lineNumber)
                lexer is the lexer used to analyze the source, it points the start token of source.
                line is the text of the physical line just read
                lineNumber is the line offset of <line> in the file being processed
        """
        self.lineRules.append(lineRule)

    def AddRule(self, rule):
        """
        Add rule on any token
        Added rule should be function with following prototype:
            def RunRule(lexer, contextStack)
                lexer is the lexer used to analyze the source, it points the start token of source.
                contextStack is a stack showing the lexical context the token resides in
        """
        self.rules.append(rule)

    def AddTypeNameRule(self, typeNameRule):
        """
        Add rule on any type (class / struct / union / namespace / enum)
        Added rule should be function with following prototype:
            def RunRule(lexer, typeName, typeFullName, decl, contextStack, typeContext)
                lexer is the lexer used to analyze the source, it points the start token of source.
                typeName is the name of the C++ type encountered (e.g., "CLASS", "STRUCT")
                typeFullName is the typed variable name (e.g., the class name)
                decl is a boolean flag denoting whether the function is a declaration (True) or
                     definition (False)
                contextStack is a stack showing the lexical context the token resides in
                typeContext is the new context entry that will be pushed to the contextStack due to this token
        """
        self.typeNameRules.append(typeNameRule)

    def AddTypeScopeRule(self, typeScopeRule):
        """
        Add rule when the token is within a type definition scope
        Added rule should be function with following prototype:
            def RunRule(lexer, typeName, typeFullName, decl, contextStack, typeContext)
                lexer is the lexer used to analyze the source, it points the start token of source.
                contextStack is a stack showing the lexical context the token resides in
        """
        self.typeScopeRules.append(typeScopeRule)

    def AddFileEndRule(self, fileEndRule):
        """
        Add rule on the file end
        Added rule should be function with following prototype:
            def RunRule(lexer, filename, dirname)
            lexer is the lexer used to analyze the source. it points the end token of source.
            filename is the filename analyzed.
            dirname is the file directory.
        """
        self.fileEndRules.append(fileEndRule)

    def AddFileStartRule(self, fileStartRule):
        """
        Add rule on the file start
        Added rule should be function with following prototype:
            def RunRule(lexer, filename, dirname)
            lexer is the lexer used to analyze the source. it points the start token of source.
            filename is the filename analyzed.
            dirname is the file directory.
        """
        self.fileStartRules.append(fileStartRule)

    def AddSessionEndRule(self, sessionEndRule):
        """
        Add rule on the session end.

        This rule is called when the script has finished processing all target files.
        It is called only once at the end of the script's run.

        Added rule should be function with following prototype:
            def RunRule()
        """
        self.sessionEndRules.append(sessionEndRule)

    def AddSessionStartRule(self, sessionStartRule):
        """
        Add rule on the session start

        This rule is called before the script begins processing the first target file.
        It is called only once at the start of the script's processing activities.

        Added rule should be function with following prototype:
            def RunRule()
        """
        self.sessionStartRules.append(sessionStartRule)

    def AddProjectRules(self, projectRule):
        """
        Add rule on the project
        Added Rule should be function with following prototype:
            def RunRule(targetName)
            targetName is the analysis target directory.
        """
        self.projectRules.append(projectRule)


class RollbackImporter:
    def __init__(self):
        "Creates an instance and installs as the global importer"
        self.previousModules = sys.modules.copy()
        self.realImport = __builtins__["__import__"]
        __builtins__["__import__"] = self._import
        self.newModules = {}

    def _import(self, name, *args, **kwargs):
        result = self.realImport(name, *args, **kwargs)
        if name.find("rules") != -1:
            self.newModules[name] = 1
        return result

    def uninstall(self):
        for modname in self.newModules.keys():
            if modname.find("rules") != -1:
                if modname not in self.previousModules:
                    # Force reload when modname next imported
                    del(sys.modules[modname])
        __builtins__["__import__"] = self.realImport


ruleManager = RuleManager(GetRuntimePath())
