Base class for building command line applications.

The CommandLineApp class makes creating command line applications as
simple as defining callbacks to handle options when they appear in
'sys.argv'.

To do:

- enhance intelligence of option handling

- boolean options should not need to be implemented as functions

- enable/disable with/without options

- type checking for option arguments

- rewrite using modern python features such as inspect
