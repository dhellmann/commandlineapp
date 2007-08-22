#!/usr/bin/env python
#
# Copyright 2007 Doug Hellmann.
#
#
#                         All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software and
# its documentation for any purpose and without fee is hereby
# granted, provided that the above copyright notice appear in all
# copies and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of Doug
# Hellmann not be used in advertising or publicity pertaining to
# distribution of the software without specific, written prior
# permission.
#
# DOUG HELLMANN DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
# NO EVENT SHALL DOUG HELLMANN BE LIABLE FOR ANY SPECIAL, INDIRECT OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

"""Tests for CommandLineApp

"""

__module_id__ = "$Id$"

#
# Import system modules
#
import unittest

#
# Import local modules
#
from CommandLineApp import *

#
# Module
#

class CLATestCase(unittest.TestCase):

    def testScanForOptions(self):
        class CLAScanForOptionsTest(CommandLineApp):
            force_exit = False
            debugging = True
            def optionHandler_multi_args(self, *options):
                "Expects multiple arguments."
            optionHandler_alias = optionHandler_multi_args
            def optionHandler_n(self):
                "No arguments"
            def optionHandler_kwd(self, default='value'):
                "single arg with default"

        options = CLAScanForOptionsTest().scanForOptions()
        test_options = [ (o.switch, o.option_name, o.arg_name, o.default, o.is_variable)
                         for o in options 
                         ]
        self.failUnlessEqual(
            test_options, 
            [('--alias', 'alias', 'options', None, True),
             ('--debug', 'debug', None, None, False),
             ('-h', 'h', None, None, False),
             ('--help', 'help', None, None, False),
             ('--kwd', 'kwd', 'default', 'value', False),
             ('--multi-args', 'multi_args', 'options', None, True),
             ('-n', 'n', None, None, False),
             ('--quiet', 'quiet', None, None, False),
             ('-v', 'v', None, None, False),
             ('--verbose', 'verbose', 'level', 1, False),
             ])
        return

    def testShortHelpDoesNotRunMain(self):
        class CLAShortHelpDoesNotRunMain(CommandLineApp):
            force_exit = False
            debugging = True
            _app_name = 'CLAShortHelpDoesNotRunMain'
            def showHelp(self, *args, **kwds):
                return
            def showVerboseHelp(self):
                return
            def main(self, *args):
                raise AssertionError('Should not be in main!')

        CLAShortHelpDoesNotRunMain(['-h']).run()
        return

    def testLongHelpDoesNotRunMain(self):
        class CLALongHelpDoesNotRunMain(CommandLineApp):
            force_exit = False
            debugging = True
            _app_name = 'CLALongHelpDoesNotRunMain'
            def showHelp(self, *args, **kwds):
                return
            def showVerboseHelp(self):
                return
            def main(self, *args):
                raise AssertionError('Should not be in main!')

        CLALongHelpDoesNotRunMain(['--help']).run()
        return

    def testOptionList(self):

        class CLAOptionListTest(CommandLineApp):
            force_exit = False
            debugging = True
            _app_name = 'CLAOptionListTest'
            expected_options = ('a', 'b', 'c')
            def optionHandler_t(self, *options):
                "Expects multiple arguments."
                assert options == self.expected_options, \
                       "Option value does not match expected (%s)" % str(options)
            optionHandler_option_list = optionHandler_t

        CLAOptionListTest( [ '-t', 'a,b,c' ] ).run()
        CLAOptionListTest( [ '--option-list', 'a,b,c' ] ).run()
        CLAOptionListTest( [ '--option-list=a,b,c' ] ).run()
        return

    def testLongOptions(self):
        class CLALongOptionTest(CommandLineApp):
            force_exit = False
            debugging = True
            def optionHandler_test(self):
                "Expects no arguments."
                return
            def optionHandler_test_args(self, args):
                "Expects some arguments"
                assert args == 'foo'
                return

        CLALongOptionTest( [ '--test' ] ).run()
        CLALongOptionTest( [ '--test-args', 'foo' ] ).run()
        CLALongOptionTest( [ '--test-args=foo' ] ).run()
        return

    def testHelpForMainArgs(self):
        class CLAOneMainArg(CommandLineApp):
            def main(self, argname):
                return
        
        app = CLAOneMainArg()
        self.failUnlessEqual(app.getArgumentsSyntaxString(), 'argname')

        class CLAListMainArg(CommandLineApp):
            def main(self, *argname):
                return
        
        app = CLAListMainArg()
        self.failUnlessEqual(app.getArgumentsSyntaxString(), 'argname [argname...]')

        class CLAComboMainArg(CommandLineApp):
            def main(self, onearg, *listarg):
                return
        
        app = CLAComboMainArg()
        self.failUnlessEqual(app.getArgumentsSyntaxString(), 
                             'onearg listarg [listarg...]')

        class CLATwoSinglesMainArg(CommandLineApp):
            def main(self, onearg, twoarg, *listarg):
                return
        
        app = CLATwoSinglesMainArg()
        self.failUnlessEqual(app.getArgumentsSyntaxString(), 
                             'onearg twoarg listarg [listarg...]')
        return

    def testArgsToMain(self):
        class CLAArgsToMainTest(CommandLineApp):
            force_exit = False
            expected_args = ( 'a', 'b', 'c' )
            def optionHandler_t(self):
                pass
            def main(self, *args):
                assert args == self.expected_args, \
                       'Got %s instead of expected values.' % str(args)

        CLAArgsToMainTest( [ 'a', 'b', 'c' ] ).run()
        CLAArgsToMainTest( [ '-t', 'a', 'b', 'c' ] ).run()
        CLAArgsToMainTest( [ '-t', '--', 'a', 'b', 'c' ] ).run()
        CLAArgsToMainTest( [ '--', 'a', 'b', 'c' ] ).run()

        new_test = CLAArgsToMainTest( [ '--', '-t', 'a', 'b', 'c' ] )
        new_test.expected_args = ('-t',) + new_test.expected_args
        new_test.run()
        return

    def testArgsToMainInvalid(self):
        class CLAArgsToMainInvalidTest(CommandLineApp):
            force_exit = False
            debugging = True
            called_help = False
            def showHelp(self, message):
                self.called_help = True
            def main(self, a, b, *args):
                return

        try:
            app = CLAArgsToMainInvalidTest( [ 'a' ] )
        except TypeError:
            pass
        else:
            app.run()
            self.failUnless(app.called_help)
        return

    def testArgsToMainInvalidNoVarArgs(self):
        class CLAArgsToMainInvalidNoVarArgsTest(CommandLineApp):
            force_exit = False
            debugging = True
            called_help = False
            def showHelp(self, message):
                self.called_help = True
            def main(self, a, b):
                return

        try:
            app = CLAArgsToMainInvalidNoVarArgsTest( [ 'a' ] )
        except TypeError:
            pass
        else:
            app.run()
            self.failUnless(app.called_help)
        return

    def testInterrupt(self):
        class CLAInterruptTest(CommandLineApp):
            force_exit = False
            called = False
            def handleInterrupt(self):
                self.called = True
                return 99
            def main(self, *args):
                raise KeyboardInterrupt()

        app = CLAInterruptTest()
        try:
            exit_code = app.run()
        except KeyboardInterrupt:
            self.fail('Should have trapped the exception')
        self.failUnless(app.called)
        self.failUnlessEqual(exit_code, 99)
        return

    def testMainException(self):
        class CLAMainExceptionTest(CommandLineApp):
            force_exit = False
            called = False
            def handleMainException(self, err):
                self.called = True
                return 99
            def main(self, *args):
                raise RuntimeError()

        app = CLAMainExceptionTest()
        try:
            exit_code = app.run()
        except RuntimeError:
            self.fail('Should have trapped the exception')
        self.failUnless(app.called)
        self.failUnlessEqual(exit_code, 99)
        return

    def testRaiseSystemExit(self):
        class CLARaiseSystemExitTest(CommandLineApp):
            force_exit = False
            called = False
            def handleMainException(self):
                self.called = True
                return 99
            def main(self, *args):
                raise SystemExit(88)

        app = CLARaiseSystemExitTest()
        try:
            exit_code = app.run()
        except SystemExit:
            self.fail('Should have trapped the exception')
        self.failIf(app.called)
        self.failUnlessEqual(exit_code, 88)
        return

    def testSimpleHelpText(self):
        class CLAHelpTest(CommandLineApp):
            force_exit = False
                

        app = CLAHelpTest()
        s = app.getSimpleSyntaxHelpString()
        self.failUnlessEqual(s, '''test_CommandLineApp.py [<options>] args [args...]

    --debug
    -h
    --help
    --quiet
    -v
    --verbose=level
''')
        return

    def testVerboseHelpText(self):
        class CLAHelpTest(CommandLineApp):
            """This is a test program to verify the help works
            as expected.
            """
            force_exit = False

            EXAMPLES_DESCRIPTION = '''
Describe a few examples here.
'''

            def main(self, arg1, *args):
                """arg1 - First argument.

                args - Remaining arguments.
                """
                return

        app = CLAHelpTest()
        s = app.getVerboseSyntaxHelpString()
        self.failUnlessEqual(s, '''This is a test program to verify the help works as expected.


SYNTAX:

  test_CommandLineApp.py [<options>] arg1 args [args...]

    --debug
    -h
    --help
    --quiet
    -v
    --verbose=level


ARGUMENTS:

    arg1 - First argument.

    args - Remaining arguments.


OPTIONS:

    --debug
        Set debug mode to see tracebacks.

    -h
        Displays abbreviated help message.

    --help
        Displays verbose help message.

    --quiet
        Turn on quiet mode.

    -v
        Increment the verbose level. Higher levels are more verbose.
        The default is 1.

    --verbose=level
        Set the verbose level.

EXAMPLES:


Describe a few examples here.
''')
        return


if __name__ == '__main__':
    unittest.main()
