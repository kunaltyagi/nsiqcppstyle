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

import nsiqcppstyle_checker
from nsiqcppstyle_outputer import _consoleOutputer as console
import unittest
import nsiqcppstyle_rulemanager
import nsiqcppstyle_reporter
import nsiqcppstyle_state

errors = []


def MockError(token, category, message):
    global errors
    errors.append((token, category, message))
    # print token, category, message


class nct(unittest.TestCase):
    def setUp(self):
        nsiqcppstyle_rulemanager.ruleManager.ResetRules()
        nsiqcppstyle_rulemanager.ruleManager.ResetRegisteredRules()
        console.SetLevel(console.Level.Verbose)
        nsiqcppstyle_reporter.Error = MockError
        self.setUpRule()
        global errors
        errors = []

    def Analyze(self, filename, data):
        nsiqcppstyle_checker.ProcessFile(
            nsiqcppstyle_rulemanager.ruleManager, filename, data)

    def ExpectError(self, msg):
        result = self._CheckErrorContent(msg)
        # Error with message
        self.assertTrue(result, "Expected error but got none")

    def ExpectSuccess(self, msg):
        global errors
        result = self._CheckErrorContent(msg)
        # Error with message
        self.assertFalse(result, "Expected no error but got: " + str(errors))

    def _CheckErrorContent(self, msg):
        global errors
        for err in errors:
            if err[1] == msg:
                return True
        return False
