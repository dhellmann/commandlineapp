#######
History
#######

3.0.7

    - Repackage the documentation

3.0.6

    - Bug fix from Cezary Statkiewicz for handling default arguments.

3.0.5
    - Fixed packaging problems that prevented installation with easy_install and pip.

3.0.4
    - Switched to sphinx for documentation.

3.0.3
    - Updated the build to work with Mercurial and migrated the source to bitbucket host. No code changes.

3.0.2
    - source file encoding patch from Ben Finney

3.0.1
    - replace the test script missing from the 3.0 release

3.0
    - `Ben Finney <http://benfinney.id.au/>`_ provided a patch to convert the names of the module, method, etc. to be PEP8-compliant.  Thanks, Ben!

    These changes are obviously backwards incompatible.

2.6
    - Add initialization hooks to make application setup easier without overriding ``__init__()``.

2.5
    - Updated to handle Unicode status messages more reliably.

2.4
    - Code clean up and error handling changes.

2.3
    - Refine help output a little more.

2.2
    - Handle missing docstrings for main() and the class.

2.1
    - Add automatic detection and validation of main function arguments, including help text generation. Also includes the main function docstring in :option:`--help` output.
    
2.0
    - Substantial rewrite using inspect and with modified API.

1.0
    - This is the old version, which was developed with and works under Python 1.5.4-2.5.
    
