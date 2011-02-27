Command line programs are classes, too!
=======================================

.. note::

    This article was originally published in the November 2007 issue of `Python Magazine <http://www.pythonmagazine.com/>`_.  It has been updated to match the more recent versions of :class:`CommandLineApp`.

*Most OOP discussions focus on GUI or domain-specific development areas, completely ignoring the workhorse of computing: command line programs. This article examines CommandLineApp, a base class for creating command line programs as objects, with option and argument validation, help text generation, and more.*

.. highlight:: python
    :linenothreshold: 5

Although many of the hot new development topics are centered on web technologies like AJAX, regular command line programs are still an important part of most systems.  Many system administration tasks still depend on command line programs, for example.  Often, a problem is simple enough that there is no reason to build a graphical or web user interface when a straightforward command line interface will do the job.  Command line programs are less glamorous than programs with fancy graphics, but they are still the workhorses of modern computing.

The Python standard library includes two modules for working with command line options.  The **getopt** module presents an API that has been in use for decades on some platforms and is commonly available in many programming languages, from C to bash. The **optparse** module is more modern than **getopt**, and offers features such as type validation, callbacks, and automatic help generation.  Both modules elect to use a procedural-style interface, though, and as a result neither has direct support for treating your command line application as a first class object.  There is no facility for sharing common options between related programs using **getopt**.  And, while it is possible to reuse ``optparse.OptionParser`` instances in different programs, it is not as natural as inheritance.

`CommandLineApp <http://www.doughellmann.com/projects/CommandLineApp/>`_ is a base class for command line programs.  It handles the repetitive aspects of interacting with the user on the command line such as parsing options and arguments, generating help messages, error handling, and printing status messages.  To create your application, just make a subclass of :class:`CommandLineApp` and concentrate on your own code.  All of the information about switches, arguments, and help text necessary for your program to run is derived through introspection.  Common options and behavior can be shared by applications through inheritance.

csvcat Requirements
-------------------

Recently, I needed to combine data from a few different sources, including a database and a spreadsheet, to summarize the results. I wanted to import the merged data into a spreadsheet where I could perform the analysis.  All of the sources were able to save data to comma-separated-value (CSV) files; the challenge was merging the files together.  Using the **csv** module in the Python standard library, and :class:`CommandLineApp`, I wrote a small program to read multiple CSV files and concatenate them into a single output file.  The program, `csvcat <http://www.doughellmann.com/projects/csvcat/>`_, is a good illustration of how to create applications with :class:`CommandLineApp`.

The requirements for **csvcat** were fairly simple.  It needed to read one or more CSV files and combine them, without repeating the column headers that appeared in each input source.  In some cases, the input data included columns I did not want, so I needed to be able to select the columns to include in the output.  No sort feature was needed, since I was going to import it into a spreadsheet when I was done and I could sort the data after importing it.  To make the program more generally useful, I also included the ability to select the output format using a **csv** module feature called "dialects".

Analyzing the Help
------------------

Listing 1 shows the help output for the final version of **csvcat**, produced by running ``csvcat --help``.  Listing 2 shows the source for the program.  All of the information in the help output is derived from the **csvcat** class through introspection.  The help text follows a fairly standard layout.  It begins with a description of the application, followed by increasingly more detailed descriptions of the syntax, arguments, and options.  Application-specific help such as examples and argument ranges appears at the end.

Listing 1
~~~~~~~~~

.. [[[cog
.. cog.out(run_script(cog.inFile, 'Listing2.py --help'))
.. ]]]

::

	$ python docs/source/PyMagArticle/Listing2.py --help
	Concatenate comma separated value files.
	
	
	SYNTAX:
	
	  csvcat [<options>] filename [filename...]
	
	    -c col[,col...], --columns=col[,col...]
	    -d name, --dialect=name
	    --debug
	    -h
	    --help
	    --quiet
	    --skip-headers
	    -v
	    --verbose=level
	
	
	ARGUMENTS:
	
	    The names of comma separated value files, such as might be
	    exported from a spreadsheet or database program.
	
	
	OPTIONS:
	
	    -c col[,col...], --columns=col[,col...]
	        Limit the output to the specified columns. Columns are
	        identified by number, starting with 0.
	
	    -d name, --dialect=name
	        Specify the output dialect name. Defaults to "excel".
	
	    --debug
	        Set debug mode to see tracebacks.
	
	    -h
	        Displays abbreviated help message.
	
	    --help
	        Displays verbose help message.
	
	    --quiet
	        Turn on quiet mode.
	
	    --skip-headers
	        Treat the first line of each file as a header, and only
	        include one copy in the output.
	
	    -v
	        Increment the verbose level.
	
	        Higher levels are more verbose. The default is 1.
	
	    --verbose=level
	        Set the verbose level.
	
	EXAMPLES:
	
	
	To concatenate 2 files, including all columns and headers:
	
	  $ csvcat file1.csv file2.csv
	
	To concatenate 2 files, skipping the headers in the second file:
	
	  $ csvcat --skip-headers file1.csv file2.csv
	
	To concatenate 2 files, including only the first and third columns:
	
	  $ csvcat --col 0,2 file1.csv file2.csv
	

.. [[[end]]]

Listing 2
~~~~~~~~~

.. literalinclude:: Listing2.py
    :linenos:

The program description is taken from the docstring of the **csvcat** class.  Before it is printed, the text is split into paragraphs and reformatted using **textwrap**, to ensure that it is no wider than 80 columns of text.

The program description is followed by a syntax summary for the program.  The options listed in the syntax section correspond to methods with names that begin with ``option_handler_``.  For example, ``option_handler_skip_headers()`` indicates that **csvcat** should accept a ``--skip-headers`` option on the command line.

The names of any non-optional arguments to the program appear in the syntax summary.  In this case, **csvcat** needs the names of the files containing the input data.  At least one file name is necessary, and multiple names can be given, as indicated by the fact that the ``filename`` argument to ``main()`` uses the variable argument notation: ``*filename``.  A longer description of the arguments, taken from the docstring of the ``main()`` method (lines 79-82), follows the syntax summary.  As with the general program summary, the description of the arguments is reformatted with **textwrap** to fit the screen.

Options and Their Arguments
---------------------------

Following the argument description is a detailed explanation of all of the options to the program.  :class:`CommandLineApp` examines each option handler method to build the option description, including the name of the option, alternative names for the same option, and the name and description of any arguments the option accepts.  There are three variations of option handlers, based on the arguments used by the option. 

The simplest kind of option does not take an argument at all, and is used as a "switch" to turn a feature on or off.  The method ``option_handler_skip_headers`` (lines 38-43) is an example of such a switch.  The method takes no argument, so :class:`CommandLineApp` recognizes that the option being defined does not take an argument either.  To create the option name, the prefix is stripped from the method name, and the underscore is converted to a dash (``-``); ``option_handler_skip_headers`` becomes ``--skip-headers``.

Other options accept a single argument.  For example, the ``--dialect`` option requires the name of the CSV output dialect.  The method ``option_handler_dialect`` (lines 46-51) takes one argument, called ``name``.  The suggested syntax for the option, as seen in Listing 1, is ``--dialect=name``.  The name of the method's argument is used as the name of the argument to the option in the help text.

The ``-d`` option has the same meaning as ``--dialect``, because ``option_handler_d`` is an alias for ``option_handler_dialect``.  :class:`CommandLineApp` recognizes aliases, and combines the forms in the documentation so the alternative forms ``-d name`` and ``--dialect=name`` are described together.

It is often useful for an option to take multiple arguments, as with ``--columns``.  The user could repeat the option on the command line, but it is more compact to allow them to list multiple values in one argument list.  When :class:`CommandLineApp` sees an option handler method that takes a variable argument list, it treats the corresponding option as accepting a list of arguments.  When the option appears on the command line, the string argument is split on any commas and the resulting list of strings is passed to the option handler method.  

For example, ``option_handler_columns`` (lines 55-60) takes a variable length argument named ``col``.  The option ``--columns`` can be followed by several column numbers, separated by commas.  The option handler is called with the list of values pre-parsed.  In the syntax description, the argument is shown repeating: ``--columns=col[,col...]``.

For all cases, the docstring from the option handler method serves as the help text for the option.  The text of the docstring is reformatted using **textwrap** so both the code and help output are easy to read without extra effort on the part of the developer.

Application-specific Detailed Help
----------------------------------

The general syntax and option description information is produced in the same way for all :class:`CommandLineApp` programs.  There are times when an application needs to include additional information in the help output, though, and there are two ways to add such information.

The first way is by providing examples of how to use the program on the command line.  Although it is optional, including examples of how to apply different combinations of arguments to your program to achieve various results enhances the usefulness of the help as a reference manual.  When the ``EXAMPLES_DESCRIPTION`` class attribute is set, it is used as the source for the examples.  Unlike the other documentation strings, the ``EXAMPLES_DESCRIPTION`` is printed directly without being reformatted. This preserves the indentation and other formatting of the examples, so the user sees an accurate representation of the program's inputs and outputs.

Occasionally, a program may need to include information in its help output which cannot be statically defined in a docstring or derived by :class:`CommandLineApp`.  At the very end of its help, **csvcat** includes a list of available CSV dialects which can be used with the ``--dialect`` option.  Since the list of dialects must be constructed at runtime based on what dialects have been registered with the **csv** module, **csvcat** overrides ``showVerboseHelp()`` to print the list itself (lines 27-35).

Using csvcat
------------

The inputs to **csvcat** are any number of CSV files, and the output is CSV data printed to standard output.  To test **csvcat** during development, I created two small files with test data.  Each file contains three columns of data: a number, a string, and a date.

::

    $ cat testdata1.csv
    "Title 1","Title 2","Title 3"
    1,"a",08/18/07
    2,"b",08/19/07
    3,"c",08/20/07

The second file does not include quotes around any of the string fields.  I chose to include this variation because **csvcat** does not quote its output, so using unquoted test data simulates re-processing the output of **csvcat**.

::

    $ cat testdata2.csv
    Title 1,Title 2,Title 3
    40,D,08/21/07
    50,E,08/22/07
    60,F,08/23/07

The simplest use of **csvcat** is to print the contents of an input file to standard output.  Notice that the output does not include quotes around the string fields.

::

    $ csvcat testdata1.csv
    Title 1,Title 2,Title 3
    1,a,08/18/07
    2,b,08/19/07
    3,c,08/20/07

It is also possible to select which columns should be included in the output using the ``--columns`` option.  Columns are identified by their number, beginning with ``0``.  Column numbers can be listed in any order, so it is possible to reorder the columns of the input data, if needed.

::

    $ csvcat --columns 2,0 testdata1.csv
    Title 3,Title 1
    08/18/07,1
    08/19/07,2
    08/20/07,3

Switching to tab-separated columns instead of comma-separated is easily accomplished by using the ``--dialect`` option.  There are only two dialects available by default, but the the **csv** module API supports registering additional dialects.

::

    $ csvcat --dialect excel-tab testdata1.csv
    Title 1 Title 2 Title 3
    1       a       08/18/07
    2       b       08/19/07
    3       c       08/20/07

For my project, there were input files with several columns, but only two of them needed to be included in the output.  Each file had a single row of column headers. I only wanted one set of headers in the output, so the headers from subsequent files needed to be skipped.  And the output had to be in a format I could import into a spreadsheet, for which the default "excel" dialect worked fine.  The data was merged with a command like this:

::

    $ csvcat --skip-headers --columns 2,0 testdata1.csv testdata2.csv
    Title 3,Title 1
    08/18/07,1
    08/19/07,2
    08/20/07,3
    08/21/07,40
    08/22/07,50
    08/23/07,60

Running a CommandLineApp Program
--------------------------------

Most of the work for **csvcat** is being done in the ``main()`` method.  To invoke the application, however, the caller does not invoke ``main()`` directly.  The program should be started by calling ``run()``, so the options are validated and exceptions from ``main()`` are handled.  The ``run()`` method is one of several methods that are not intended to be overridden by derived classes, since they implement the core features of a command line program.  The source for :class:`CommandLineApp` appears in Listing 3.

Listing 3
~~~~~~~~~

.. include:: ../../../commandlineapp.py
    :literal:


The available and supported options are examined when the instance is initialized.  By default, the contents of ``sys.argv`` are used as the options and arguments passed in from the command line to the program.  It is easy to pass a different list of options when writing automated tests for your program, by passing a list of strings to ``__init__()`` as ``command_line_options``.  The options supported by the program are determined by scanning the class for option handler methods.  No options are actually evaluated until ``run()`` is called.

When the program is run, the first thing it does is use **getopt** to validate the options it has been given.  In ``callGetopt()``, the arguments needed by **getopt** are constructed based on the option handlers discovered for the class.  Options are processed in the order they are passed on the command line, and the option handler method for each option encountered is called.  When an option handler requires an argument that is not provided on the command line, **getopt** detects the error.  When an argument is provided, the option handler is responsible for determining whether the value is the correct type or otherwise valid.  When the argument is not valid, the option handler can raise an exception with an error message to be printed for the user.

After all of the options are handled, the remaining arguments to the program are checked to be sure there are enough to satisfy the requirements, based on the argspec of the ``main()`` function.  The number of arguments is checked explicitly to avoid having to handle a ``TypeError`` if the user does not pass the right number of arguments on the command line.  If :class:`CommandLineApp` depended on catching a ``TypeError`` when it passed too few arguments to ``main()``, it could not tell the difference between a coding error and a user error.  If a mistake inside ``main()`` caused a ``TypeError`` to occur, it might look like the user had passed an incorrect number of arguments to the program.

Error Handling
--------------

When an exception is raised during option processing or inside ``main()``, the exception is caught by one of the ``except`` clauses and given to an error handling method.  Subclasses can change the error handling behavior by overriding these methods.

``KeyboardInterrupt`` exceptions are handled by calling ``handleInterrupt()``.  The default behavior is to print a message that the program has been interrupted and cause the program to exit with an error code.  A subclass could override the method to clean up an in-progress task, background thread, or other operation which otherwise might not be automatically stopped when the ``KeyboardInterrupt`` is received.

When a lower level library tries to exit the program, ``SystemExit`` may be raised.  :class:`CommandLineApp` traps the ``SystemExit`` exception and exits normally, using the exit status taken from the exception.  If the ``force_exit`` attribute of the application is false, ``run()`` returns instead of exiting.  Trapping attempts to exit makes it easier to integrate :class:`CommandLineApp` programs with ``unittest`` or other testing frameworks.  The test can instantiate the application, set ``force_exit`` to a false value, then run it.  If any errors occur, a status code is returned but the test process does not exit.

All other types of exceptions are handled by calling ``handleMainException()`` and passing the exception as an argument.  The default implementation of ``handleMainException()`` (lines 62-70) prints a simple error message based on the exception, unless debugging mode is turned on.  Debugging mode prints the entire traceback for the exception.

::

    $ csvcat file_does_not_exist.csv
    ERROR: [Errno 2] No such file or directory:
    'file_does_not_exist.csv'

Option Definitions
------------------

The standard library module **inspect** provides functions for performing introspection operations on classes and objects at runtime.  The API supports basic querying and type checking so it is possible, for example, to get a list of the methods of a class, including all inherited methods.  

``CommandLineApp.scan_for_options()`` uses **inspect** to scan an application class for option handler methods.  All of the methods of the class are retrieved with ``inspect.getmembers()``, and those whose name starts with ``option_handler_`` are added to the list of supported options.  Since most command line options use dashes instead of underscores, but method names cannot contain dashes, the underscores in the option handler method names are converted to dashes when creating the option name.

The ``__init__()`` method of the **OptionDef** class does all of the work of determining the command line switch name and what type of arguments the switch takes.  The option handler method is examined with ``inspect.getargspec()``, and the result is used to initialize the **OptionDef**.

An "argspec" for a function is a tuple made up of four values: a list of the names of all regular arguments to the function, including ``self`` if the function is a method; the name of the argument to receive the variable argument values, if any; the name of the argument to receive the keyword arguments, if any; and a list of the default values for the arguments, in they order they appear in the list of option names.

The argspecs for the option handlers in **csvcat** illustrate the variations of interest to **OptionDef**.  First, ``option_handler_skip_headers``:

::

    >>> import Listing2
    >>> import inspect
    >>> print inspect.getargspec(
    ... Listing2.csvcat.option_handler_skip_headers)
    (['self'], None, None, None)

Since the only positional argument to the method is ``self``, and there is no variable argument name given, the option handler is treated as a simple command line switch without any arguments.

The ``option_handler_dialect``, on the other hand, does include an additional argument:

::

    >>> print inspect.getargspec(
    ... Listing2.csvcat.option_handler_dialect)
    (['self', 'name'], None, None, None)

The ``name`` argument is listed in the argspec as a single regular argument.  The result, when a program is run, is that while the options are being processed by :class:`CommandLineApp` and **OptionDef**, the value for ``name`` is passed directly to the option handler method.

The ``option_handler_columns`` method illustrates variable argument handling:

::

    >>> print inspect.getargspec(
    ... Listing2.csvcat.option_handler_columns)
    (['self'], 'col', None, None)

The ``col`` argument from ``option_handler_columns`` is named in the argspec as the variable argument identifier.  Since ``option_handler_columns`` accepts variable arguments, the **OptionDef** splits the argument value into a list of strings, and the list is passed to the option handler method using the variable argument syntax.

The other variable argument configuration, using unidentified keyword arguments, does not make sense for an option handler.  The user of the command line program has no standard way to specify named arguments to options, so they are not supported by **OptionDef**.

Status Messages
---------------

In addition to command line option and argument parsing, and error handling, :class:`CommandLineApp` provides a "status message" interface for giving varying levels of feedback to the user.  Status messages are printed by calling ``self.status_message()``.  Each message must indicate the verbose level setting at which the message should be printed.  If the current verbose level is at or higher than the desired level, the message is printed.  Otherwise, it is ignored.  The ``-v``, ``--verbose``, and ``--quiet`` flags let the user control the ``verbose_level`` setting for the application, and are defined in the :class:`CommandLineApp` so that all subclasses inherit them.

Listing 4
~~~~~~~~~

.. literalinclude:: Listing4.py
    :linenos:

Listing 4 contains another sample application which uses ``status_message()`` to illustrate how the verbose level setting is applied.  The default verbose level is 1, so when the program is run without any additional arguments only a single message is printed:

::

    $ python Listing4.py            
    Level 1
    $

The ``--quiet`` option silences all status messages by setting the verbose level to ``0``:

::

    $ python Listing4.py --quiet
    $ 

Using the ``-v`` option increases the verbose setting, one level at a time.  The option can be repeated on the command line:

::

    $ python Listing4.py -v     
    Level 1
    Level 2
    $ python Listing4.py -vv
    New verbose level is 3
    Level 1
    Level 2
    Level 3
    $

And the ``--verbose`` option sets the verbose level directly to the desired value:

::

    $ python Listing4.py --verbose 4
    New verbose level is 4
    Level 1
    Level 2
    Level 3
    Level 4
    $

Error messages can be printed to the standard error stream using the ``error_message()`` method.  The message is prefixed with the word "ERROR", and error messages are always printed, no matter what verbose level is set.  Most programs will not need to use ``errorMessage()`` directly, because raising an exception is sufficient to have an error message displayed for the user.

CommandLineApp and Inheritance
------------------------------

When creating a suite of related programs, it is usually desirable for all of the programs to use the same options and, in many cases, share other common behavior.  For example, when working with a database the connection and transaction must be managed reliably.  Rather than re-implementing the same database handling code in each program, by using :class:`CommandLineApp`, you can create an intermediate base class for your programs and share a single implementation.  Listing 5 includes a skeleton base class called **SQLiteAppBase** for working with an ``sqlite3`` database in this way.

Listing 5
~~~~~~~~~

.. literalinclude:: Listing5.py
    :linenos:


**SQLiteAppBase** defines a single option handler for the ``--db`` option to let the user choose the database file.  The default database is a file in the current directory called "sqlite.db".  The ``main()`` method establishes a connection to the database, opens a cursor for working with the connection, then calls ``takeAction()`` to do the work.  When ``takeAction()`` raises an exception, all database changes it may have made are discarded and the transaction is rolled back.  When there is no error, the transaction is committed and the changes are saved.

Listing 6
~~~~~~~~~

.. literalinclude:: Listing6.py
    :linenos:


A subclass of **SQLiteAppBase** can override ``takeAction()`` to do some actual work using the database connection and cursor created in ``main()``.  Listing 6 contains one such program, called ``initdb``.  In ``initdb``, the ``takeAction()`` method creates a "log" table using the database cursor established in the base class.  It then inserts two rows into the new table, using the same cursor.  There is no need for ``initdb`` to commit the transaction, since the base class will do that after ``takeAction()`` returns without raising an exception.

::

    $ python Listing6.py
    Initializing database sqlite.db

Listing 7
~~~~~~~~~

.. literalinclude:: Listing7.py
    :linenos:


The ``showlog`` program in Listing 7 also uses **SQLiteAppBase**.  It reads records from the log table and prints them out to the screen.  When no options are given, it uses the cursor opened by the base class to find all of the records in the "log" table, and print them:

::

    $ python Listing7.py
    Sat Aug 25 19:09:41 2007       Created database
    Sat Aug 25 19:09:41 2007       Created log table

The ``--message`` option to ``showlog`` can be used to filter the output to include only records whose message column matches the pattern given.  When a message substring is specified, the select statement is altered to include only messages containing the substring.  In this example, only log messages with the word "table" in the message are printed: 

::

    $ python Listing7.py --message table
    Sat Aug 25 19:09:41 2007       Created log table

The ``updatelog`` program in Listing 8 inserts new records into the database.  Each time ``updatelog`` is called, the message passed on the command line is saved as an instance attribute by ``main()`` so it can be used later when a new row is inserted into the ``log`` table by ``takeAction()``.

Listing 8
~~~~~~~~~

.. literalinclude:: Listing8.py
    :linenos:


::

    $ python Listing8.py "another new message"
    $ python Listing7.py
    Sat Aug 25 19:09:41 2007       Created database
    Sat Aug 25 19:09:41 2007       Created log table
    Sat Aug 25 19:10:29 2007       another new message

As with ``initdb``, because the base class commits changes to the database after ``takeAction()`` returns, ``updatelog`` does not need to manage the database connection in any way.  Since all of the example programs use the database connection and cursor created by their base class, they could be updated to use a Postgresql or MySQL database by modifying the base class, without having to make those changes to each program separately.

Future Work
-----------

I have been using :class:`CommandLineApp` in my own work for several years now, and continue to find ways to enhance it. The two primary features I would still like to add are the ability to print the help for a command in formats other than plain text, and automatic type conversion for arguments.

It is difficult to prepare attractive printed documentation from plain text help output like what is produced by the current version of :class:`CommandLineApp`.  Parsing the text output directly is not necessarily straightforward, since the embedded help may contain characters or patterns that would confuse a simple parser.  A better solution is to use the option data gathered by introspection to generate output in a format such as DocBook, which could then be converted to PDF or HTML using other tool sets specifically designed for that purpose.  There is a prototype of a program to create DocBook output from an application class, but it is not robust enough to be released - yet.

:class:`CommandLineApp` is based on the older option parsing module, **getopt**, rather than the new **optparse**.  This means it does not support some of the newer features available in **optparse**, such as type conversion for arguments.  Type conversion could be added to :class:`CommandLineApp` by inferring the types from default values for arguments.  The **OptionDef** already discovers default values, but they are not used.  The ``OptionDef.invoke()`` method needs to be updated to look at the default for an option before calling the option handler.  If the default is a type object, it can be used to convert the incoming argument.  If the default is a regular object, the type of the object can be determined using ``type()``.  Then, once the type is known, the argument can be converted.

Conclusion
~~~~~~~~~~

I hope this article encourages you to think about your command line programs in a different light, and to treat them as first class objects.  Using inheritance to share code is so common in other areas of development that it is hardly given a second thought in most cases.  As has been shown with the **SQLiteAppBase** programs, the same technique can be just as powerful when applied to building command line programs, saving development time and testing effort as a result.  :class:`CommandLineApp` has been used as the foundation for dozens of types of programs, and could be just what you need the next time you have to write a new command line program.
