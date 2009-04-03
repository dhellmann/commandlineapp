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

import nose

# What project are we building?
PROJECT = 'CommandLineApp'
VERSION = '3.0.4'

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

        platforms = ('Any',),

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
    
    sdist = Bunch(
        dist_dir=os.path.expanduser('~/Desktop'),
    ),
    
)

@task
@needs(['docs', 'generate_setup', 'minilib', 
        'setuptools.command.sdist'
        ])
def sdist():
    """Create a source distribution.
    """
    pass

@task
def docs():
    path('docs').rmtree()
    sh('epydoc -v --docformat restructuredtext --output docs commandlineapp.py')
    return
