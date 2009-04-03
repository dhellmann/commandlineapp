#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

""" Unit tests for commandlineapp module

"""

__module_id__ = "$Id$"

#
# Import system modules
#
from StringIO import StringIO
import unittest

#
# Import local modules
#
from commandlineapp import CommandLineApp

#
# Module
#

class CLATestCase(unittest.TestCase):

    def test_unicode_status_message_degrades_to_ascii(self):
        """ Unicode status message should degrade gracefully to ASCII """
        app = CommandLineApp([])
        buffer = StringIO()
        msg = u'André'
        app._status_message(msg, buffer)
        self.failUnlessEqual(buffer.getvalue(), msg.encode('ascii', 'replace'))
        return

    def test_option_hooks(self):
        class OptionHookTester(CommandLineApp):
            def before_options_hook(self):
                self.before = True
            def after_options_hook(self):
                self.after = True
        app = OptionHookTester([])
        self.failUnless(app.before)
        self.failUnless(app.after)
        return

    def test_ascii_status_message(self):
        app = CommandLineApp([])
        buffer = StringIO()
        msg = 'Andre'
        app._status_message(msg, buffer)
        self.failUnlessEqual(buffer.getvalue(), msg)
        return

    def test_scan_for_options(self):
        class CLAScanForOptionsTest(CommandLineApp):
            force_exit = False
            debugging = True
            def option_handler_multi_args(self, *options):
                "Expects multiple arguments."
            option_handler_alias = option_handler_multi_args
            def option_handler_n(self):
                "No arguments"
            def option_handler_kwd(self, default='value'):
                "single arg with default"

        options = CLAScanForOptionsTest([]).scan_for_options()
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

    def test_short_help_does_not_run_main(self):
        class CLAShortHelpDoesNotRunMain(CommandLineApp):
            force_exit = False
            debugging = True
            _app_name = 'CLAShortHelpDoesNotRunMain'
            def show_help(self, *args, **kwds):
                return
            def show_verbose_help(self):
                return
            def main(self, *args):
                raise AssertionError('Should not be in main!')

        CLAShortHelpDoesNotRunMain(['-h']).run()
        return

    def test_long_help_does_not_run_main(self):
        class CLALongHelpDoesNotRunMain(CommandLineApp):
            force_exit = False
            debugging = True
            _app_name = 'CLALongHelpDoesNotRunMain'
            def show_help(self, *args, **kwds):
                return
            def show_verbose_help(self):
                return
            def main(self, *args):
                raise AssertionError('Should not be in main!')

        CLALongHelpDoesNotRunMain(['--help']).run()
        return

    def test_option_list(self):

        class CLAOptionListTest(CommandLineApp):
            force_exit = False
            debugging = True
            _app_name = 'CLAOptionListTest'
            expected_options = ('a', 'b', 'c')
            def option_handler_t(self, *options):
                "Expects multiple arguments."
                assert options == self.expected_options, \
                       "Option value does not match expected (%s)" % str(options)
            option_handler_option_list = option_handler_t

        CLAOptionListTest( [ '-t', 'a,b,c' ] ).run()
        CLAOptionListTest( [ '--option-list', 'a,b,c' ] ).run()
        CLAOptionListTest( [ '--option-list=a,b,c' ] ).run()
        return

    def test_long_options(self):
        class CLALongOptionTest(CommandLineApp):
            force_exit = False
            debugging = True
            def option_handler_test(self):
                "Expects no arguments."
                return
            def option_handler_test_args(self, args):
                "Expects some arguments"
                assert args == 'foo'
                return

        CLALongOptionTest( [ '--test' ] ).run()
        CLALongOptionTest( [ '--test-args', 'foo' ] ).run()
        CLALongOptionTest( [ '--test-args=foo' ] ).run()
        return

    def test_help_for_main_args(self):
        class CLAOneMainArg(CommandLineApp):
            def main(self, argname):
                return

        app = CLAOneMainArg([])
        self.failUnlessEqual(app.get_arguments_syntax_string(), 'argname')

        class CLAListMainArg(CommandLineApp):
            def main(self, *argname):
                return

        app = CLAListMainArg([])
        self.failUnlessEqual(app.get_arguments_syntax_string(), 'argname [argname...]')

        class CLAComboMainArg(CommandLineApp):
            def main(self, onearg, *listarg):
                return

        app = CLAComboMainArg([])
        self.failUnlessEqual(app.get_arguments_syntax_string(),
                             'onearg listarg [listarg...]')

        class CLATwoSinglesMainArg(CommandLineApp):
            def main(self, onearg, twoarg, *listarg):
                return

        app = CLATwoSinglesMainArg([])
        self.failUnlessEqual(app.get_arguments_syntax_string(),
                             'onearg twoarg listarg [listarg...]')
        return

    def test_args_to_main(self):
        class CLAArgsToMainTest(CommandLineApp):
            force_exit = False
            expected_args = ( 'a', 'b', 'c' )
            def option_handler_t(self):
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

    def test_args_to_main_invalid(self):
        class CLAArgsToMainInvalidTest(CommandLineApp):
            force_exit = False
            debugging = True
            called_help = False
            def show_help(self, message):
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

    def test_args_to_main_invalid_no_var_args(self):
        class CLAArgsToMainInvalidNoVarArgsTest(CommandLineApp):
            force_exit = False
            debugging = True
            called_help = False
            def show_help(self, message):
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

    def test_interrupt(self):
        class CLAInterruptTest(CommandLineApp):
            force_exit = False
            called = False
            def handle_interrupt(self):
                self.called = True
                return 99
            def main(self, *args):
                raise KeyboardInterrupt()

        app = CLAInterruptTest([])
        try:
            exit_code = app.run()
        except KeyboardInterrupt:
            self.fail('Should have trapped the exception')
        self.failUnless(app.called)
        self.failUnlessEqual(exit_code, 99)
        return

    def test_format_help_text_none(self):
        class CLAFormatHelpTextNone(CommandLineApp):
            force_exit = False
            called = False

        app = CLAFormatHelpTextNone()
        self.failUnlessEqual(app._format_help_text(None, ''), '')
        self.failUnlessEqual(app._format_help_text('', ''), '')
        return

    def test_main_exception(self):
        class CLAMainExceptionTest(CommandLineApp):
            force_exit = False
            called = False
            def handle_main_exception(self, err):
                self.called = True
                return 99
            def main(self, *args):
                raise RuntimeError()

        app = CLAMainExceptionTest([])
        try:
            exit_code = app.run()
        except RuntimeError:
            self.fail('Should have trapped the exception')
        self.failUnless(app.called)
        self.failUnlessEqual(exit_code, 99)
        return

    def test_raise_system_exit(self):
        class CLARaiseSystemExitTest(CommandLineApp):
            force_exit = False
            called = False
            def handle_main_exception(self):
                self.called = True
                return 99
            def main(self, *args):
                raise SystemExit(88)

        app = CLARaiseSystemExitTest([])
        try:
            exit_code = app.run()
        except SystemExit:
            self.fail('Should have trapped the exception')
        self.failIf(app.called)
        self.failUnlessEqual(exit_code, 88)
        return

    def test_simple_help_text(self):
        class CLAHelpTest(CommandLineApp):
            force_exit = False
            _app_name = 'CLAHelpTest'

            def option_handler_repeats(self, *arg):
                """Argument to this option can repeat.
                """
                return

        app = CLAHelpTest([])
        s = app.get_simple_syntax_help_string()
        self.failUnlessEqual(s, '''CLAHelpTest [<options>] args [args...]

    --debug
    -h
    --help
    --quiet
    --repeats=arg[,arg...]
    -v
    --verbose=level
''')
        return

    def test_verbose_help_text(self):
        class CLAHelpTest(CommandLineApp):
            """This is a test program to verify the help works
            as expected.
            """
            force_exit = False
            _app_name = 'CLAHelpTest'

            EXAMPLES_DESCRIPTION = '''
Describe a few examples here.
'''

            def main(self, arg1, *args):
                """arg1 - First argument.

                args - Remaining arguments.
                """
                return

        app = CLAHelpTest([])
        expected = '''This is a test program to verify the help works as expected.


SYNTAX:

  CLAHelpTest [<options>] arg1 args [args...]

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
        Increment the verbose level.

        Higher levels are more verbose. The default is 1.

    --verbose=level
        Set the verbose level.

EXAMPLES:


Describe a few examples here.
'''
        expected = expected.splitlines()
        actual = app.get_verbose_syntax_help_string().splitlines()
        for line_num, (actual_line, expected_line) in enumerate(zip(actual, expected)):
            # if this test fails, uncomment these lines to look for whitespace
            # differences.
            #actual_line = actual_line.replace(' ', '.')
            #expected_line = expected_line.replace(' ', '.')
            self.failUnlessEqual(actual_line, expected_line,
                                 "Line %d: %s does not match expected %s" % 
                                 (line_num, repr(actual_line), repr(expected_line)))
        return


if __name__ == '__main__':
    unittest.main()
