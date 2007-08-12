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

class TestApp(CommandLineApp):
    """    This is a simple test application.

    It defines several optionHandler methods to handle
    some example options.  One option of each type is
    handled by an example.

    The __doc__ string for the class should contain
    the info about how to use the application. """

    examplesDescription = \
"""    a description of how to use the program 
    in various ways goes here.
"""                

    argumentsDescription = \
"""    a description of other arguments goes here
"""

    defaultLongFormOption='<default value>'

    force_exit = 0

    def optionHandler_a(self, optValue):
        'get a value for a'
        print '%s: handling a: %s' % (self.__class__.__name__, optValue)

    def optionHandler_b(self):
        'toggle the value of b'
        print '%s: handling b' % (self.__class__.__name__,)

    def optionHandler_long_form_option(self):
        'boolean option'
        print '%s: handling long-form-option' % (self.__class__.__name__,)

    def optionHandler_long_form_with_value(self, optValue):
        """First line of help.
            get a value for long form option

            Default:<manually inserted>"""
        print '%s: handling long-form-with-value: %s' % (self.__class__.__name__,
                                 optValue)

    def optionHandler_report(self, reportName):
        """Test options with same prefix.
        """
        self.statusMessage('REPORT: %s' % reportName)
        return

    def optionHandler_report_group(self, reportGroupName):
        """Test options with same prefix.
        """
        self.statusMessage('REPORT_GROUP: %s' % reportGroupName)
        return

    def optionHandler_reportgroup(self, reportGroupName):
        """Test options with same prefix.
        """
        self.statusMessage('REPORTGROUP: %s' % reportGroupName)
        return

    def main(self, *args):
        'main loop'
        print '%s: LEFT OVERS: ' % (self.__class__.__name__,), self.remainingOpts


class SubClassTestApp(TestApp):
    'new doc string'

    def optionHandler_a(self, newA):
        'Doc string for SubClassTestApp'
        print 'New A:', newA
        TestApp.optionHandler_a(self, newA)

    def optionHandler_z(self):
        'Doc string for SubClassTestApp'
        print '%s -z' % self.__class__.__name__

    def optionHandler_option_list(self, optionList):
        'Doc string for SubClassTestApp'
        if type(optionList) == type([]):
            print '%s -z list: ' % self.__class__.__name__, optionList
        else:
            print '%s -z string: %s' % (self.__class__.__name__, optionList)

    def main(self, *args):
        apply(TestApp.main, (self,) + args)
        raise Exception('not an error')


class CLATestCase(unittest.TestCase):

    def testScanForOptions(self):
        class CLAScanForOptionsTest(CommandLineApp):
            force_exit = False
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
             ('-h', 'h', None, None, False),
             ('--help', 'help', None, None, False),
             ('--kwd', 'kwd', 'default', 'value', False),
             ('--multi-args', 'multi_args', 'options', None, True),
             ('-n', 'n', None, None, False),
             ('-q', 'q', None, None, False),
             ('-v', 'v', None, None, False),
             ])
        return

    def testShortHelpDoesNotRunMain(self):
        class CLAShortHelpDoesNotRunMain(CommandLineApp):
            force_exit = False
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
            force_exit = 0
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
            force_exit = 0
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

    def testArgsToMain(self):
        class CLALongOptionTest(CommandLineApp):
            force_exit = 0
            expected_args = ( 'a', 'b', 'c' )
            def optionHandler_t(self):
                pass
            def main(self, *args):
                assert args == self.expected_args, \
                       'Got %s instead of expected values.' % str(args)

        CLALongOptionTest( [ 'a', 'b', 'c' ] ).run()
        CLALongOptionTest( [ '-t', 'a', 'b', 'c' ] ).run()
        CLALongOptionTest( [ '-t', '--', 'a', 'b', 'c' ] ).run()
        CLALongOptionTest( [ '--', 'a', 'b', 'c' ] ).run()
        new_test = CLALongOptionTest( [ '--', '-t', 'a', 'b', 'c' ] )
        new_test.expected_args = ('-t',) + new_test.expected_args
        new_test.run()
        return


if __name__ == '__main__':
    unittest.main()
