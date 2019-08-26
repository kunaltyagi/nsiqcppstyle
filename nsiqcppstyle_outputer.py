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
# ----------------------------------------------------------------------

import logging

class Verbosity:
    Verbose = logging.DEBUG
    Default = logging.INFO
    Ci      = logging.WARNING
    Error   = logging.ERROR

class ConsoleOuputer:
    def __init__(self):
        # Default verbosity is set to Default
        self.__verbosity = Verbosity.Default
        self.__CreateLogger()
        self.Separator = "======================================================================================"

    def IsVerbosityDisplayed(self, verbosity):
        return verbosity >= self.__verbosity

    def Verbose(self, *msgArgs):
        self.__logger.debug(self.__Format(*msgArgs))

    def Info(self, *msgArgs):
        self.__logger.info(self.__Format(*msgArgs))

    def CI(self, *msgArgs):
        self.__logger.warning(self.__Format(*msgArgs))

    def Error(self, *msgArgs):
        self.__logger.error(self.__Format(*msgArgs))

    def SetVerbosity(self, verbosity):
        self.__verbosity = verbosity
        self.__logger.setLevel(verbosity)
        
    def __CreateLogger(self):
        self.__logger = logging.getLogger('console')
        self.__logger.setLevel(Verbosity.Default)
        
        # create console handler and set level to Verbose
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(Verbosity.Verbose)

        # create formatter
        formatter = logging.Formatter('%(message)s')

        # add formatter to consoleHandler
        consoleHandler.setFormatter(formatter)

        # add consoleHandler to __logger
        self.__logger.addHandler(consoleHandler)
        
    def __Format(self, *msgArgs):
        # Format output te same way a direct call to print would
        return ' '.join(str(a) for a in msgArgs)

_consoleOutputer = ConsoleOuputer()

