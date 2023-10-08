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
import sys


class ConsoleOuputer:
    class Level:
        Verbose = logging.DEBUG
        Info = logging.INFO
        Ci = logging.WARNING
        Error = logging.ERROR

    def __init__(self):
        # Default level is set to Info
        self.__level = self.Level.Info

        # Commonly used console separator
        self.Separator = "======================================================================================"

        # Available output stream loggers
        self.Err = self.__NSIQLogger(sys.stderr, "stdErrConsole")
        self.Out = self.__NSIQLogger(sys.stdout, "stdOutConsole")

    def IsLevelDisplayed(self, level):
        return level >= self.__level

    def SetLevel(self, level):
        self.__level = level
        self.Out.SetLoggerLevel(level)
        self.Err.SetLoggerLevel(level)

    class __NSIQLogger:
        def __init__(self, output, name):
            self.__logger = logging.getLogger(name)
            self.__logger.setLevel(ConsoleOuputer.Level.Info)

            # Create console handler and set level to Verbose
            consoleHandler = logging.StreamHandler(output)
            consoleHandler.setLevel(ConsoleOuputer.Level.Verbose)

            # Create formatter
            formatter = logging.Formatter("%(message)s")

            # Add formatter to consoleHandler
            consoleHandler.setFormatter(formatter)

            # Add consoleHandler to logger
            self.__logger.addHandler(consoleHandler)

        def Verbose(self, *msgArgs):
            self.__logger.debug(self.__Format(*msgArgs))

        def Info(self, *msgArgs):
            self.__logger.info(self.__Format(*msgArgs))

        def Ci(self, *msgArgs):
            self.__logger.warning(self.__Format(*msgArgs))

        def Error(self, *msgArgs):
            self.__logger.error(self.__Format(*msgArgs))

        def SetLoggerLevel(self, level):
            self.__logger.setLevel(level)

        def __Format(self, *msgArgs):
            # Format output the same way a direct call to print would
            return " ".join(str(a) for a in msgArgs)


_consoleOutputer = ConsoleOuputer()
