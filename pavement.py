#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""
import os

# Set up Paver
import paver
import paver.misctasks
from paver.path import path
from paver.easy import *
import paver.setuputils
paver.setuputils.install_distutils_tasks()
import paver.doctools

try:
    import nose
except ImportError:
    # We may not have nose during installation,
    # but that's OK because we just import it
    # to enable the test tasks.
    pass

# What project are we building?
PROJECT = 'CommandLineApp'
VERSION = '3.0.7'

# Scan the input for package information
# to grab any data files (text, images, etc.) 
# associated with sub-packages.
# PACKAGE_DATA = paver.setuputils.find_package_data(PROJECT, 
#                                                   package=PROJECT,
#                                                   only_in_packages=True,
#                                                   )

options(
    setup=Bunch(
        name = PROJECT,
        version = VERSION,
        
        description = 'Base class for command line applications',
        long_description = '''Base class for building command line applications.

        The CommandLineApp class makes creating command line applications as
        simple as defining callbacks to handle options when they appear in
        sys.argv.
        ''',

        author = 'Doug Hellmann',
        author_email = 'doug.hellmann@gmail.com',

        classifiers = [ 'Development Status :: 5 - Production/Stable',
                        'License :: OSI Approved :: BSD License',
                        'Programming Language :: Python',
                        'Intended Audience :: Developers',
                        'Environment :: Console',
                        ],

        platforms = ['Any'],

        url = 'http://www.doughellmann.com/projects/%s/' % PROJECT,
        download_url = 'http://www.doughellmann.com/downloads/%s-%s.tar.gz' % \
                        (PROJECT, VERSION),

        py_modules=['commandlineapp'],

        provides=['commandlineapp',
                  ],

        # It seems wrong to have to list recursive packages explicitly.
        # packages = sorted(PACKAGE_DATA.keys()),
        # package_data=PACKAGE_DATA,

        zip_safe=False,

        ),
    
    sphinx = Bunch(
        docroot='docs',
        builddir='build',
        sourcedir='source',
    ),
    
    # Tell Paver to include extra parts that we use
    # but it doesn't ship in the minilib by default.
    minilib = Bunch(
        extra_files=['doctools'],
    ),
    
)

def run_script(input_file, script_name, 
                interpreter='python',
                include_prefix=True, 
                ignore_error=False, 
                trailing_newlines=True,
                ):
    """Run a script in the context of the input_file's directory, 
    return the text output formatted to be included as an rst
    literal text block.
    
    Arguments:
    
     input_file
       The name of the file being processed by cog.  Usually passed as cog.inFile.
     
     script_name
       The name of the Python script living in the same directory as input_file to be run.
       If not using an interpreter, this can be a complete command line.  If using an
       alternate interpreter, it can be some other type of file.
     
     include_prefix=True
       Boolean controlling whether the :: prefix is included.
     
     ignore_error=False
       Boolean controlling whether errors are ignored.  If not ignored, the error
       is printed to stdout and then the command is run *again* with errors ignored
       so that the output ends up in the cogged file.
     
     trailing_newlines=True
       Boolean controlling whether the trailing newlines are added to the output.
       If False, the output is passed to rstrip() then one newline is added.  If
       True, newlines are added to the output until it ends in 2.
    """
    # rundir = path(input_file).dirname()
    # if interpreter:
    #     cmd = '%(interpreter)s %(script_name)s' % vars()
    # else:
    #     cmd = script_name
    # real_cmd = 'cd %(rundir)s; %(cmd)s 2>&1' % vars()
    rundir = path(input_file).dirname()
    full_script_name = rundir / script_name
    if interpreter:
        cmd = '%(interpreter)s %(full_script_name)s' % vars()
    else:
        cmd = full_script_name
    real_cmd = cmd
    try:
        output_text = sh(real_cmd, capture=True, ignore_error=ignore_error)
    except Exception, err:
        print '*' * 50
        print 'ERROR run_script(%s) => %s' % (real_cmd, err)
        print '*' * 50
        output_text = sh(real_cmd, capture=True, ignore_error=True)
        print output_text
        print '*' * 50
    if include_prefix:
        response = '\n::\n\n'
    else:
        response = ''
    response += '\t$ %(cmd)s\n\t' % vars()
    response += '\n\t'.join(output_text.splitlines())
    if trailing_newlines:
        while not response.endswith('\n\n'):
            response += '\n'
    else:
        response = response.rstrip()
        response += '\n'
    return response

# Stuff commonly used symbols into the builtins so we don't have to
# import them in all of the cog blocks where we want to use them.
__builtins__['path'] = path
__builtins__['run_script'] = run_script


@task
@needs(['html', 'generate_setup', 'minilib', 
        'setuptools.command.sdist'
        ])
def sdist():
    """Create a source distribution.
    """
    pass


@task
def html(options):
    """Run sphinx to produce the documentation.
    """
    # First, fix up our path so cog can find the source
    current_path = os.environ.get('PYTHONPATH', '')
    updated_path = os.pathsep.join([os.getcwd(), current_path])
    os.environ['PYTHONPATH'] = updated_path

    paver.doctools.cog(options)
    paver.doctools.html(options)
    return

@task
def installwebsite(options):
    html(options)
    sh('rsync --rsh=ssh --archive --delete --verbose docs/build/html/* www.doughellmann.com:/var/www/doughellmann/DocumentRoot/docs/commandlineapp/')
