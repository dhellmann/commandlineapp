#!/usr/bin/env python
"""Concatenate csv files.
"""

import csv
import sys
import commandlineapp

class csvcat(commandlineapp.CommandLineApp):
    """Concatenate comma separated value files.
    """
    
    _app_name = 'csvcat'

    EXAMPLES_DESCRIPTION = '''
To concatenate 2 files, including all columns and headers:

  $ csvcat file1.csv file2.csv

To concatenate 2 files, skipping the headers in the second file:

  $ csvcat --skip-headers file1.csv file2.csv

To concatenate 2 files, including only the first and third columns:

  $ csvcat --col 0,2 file1.csv file2.csv
'''

    def showVerboseHelp(self):
        commandlineapp.CommandLineApp.showVerboseHelp(self)
        print
        print 'OUTPUT DIALECTS:'
        print
        for name in csv.list_dialects():
            print '\t%s' % name
        print
        return

    skip_headers = False
    def option_handler_skip_headers(self):
        """Treat the first line of each file as a header,
        and only include one copy in the output.
        """
        self.skip_headers = True
        return

    dialect = "excel"
    def option_handler_dialect(self, name):
        """Specify the output dialect name.
        Defaults to "excel".
        """
        self.dialect = name
        return
    option_handler_d = option_handler_dialect

    columns = []
    def option_handler_columns(self, *col):
        """Limit the output to the specified columns.
        Columns are identified by number, starting with 0.
        """
        self.columns.extend([int(c) for c in col])
        return
    option_handler_c = option_handler_columns

    def getPrintableColumns(self, row):
        """Return only the part of the row which should be printed.
        """
        if not self.columns:
            return row

        # Extract the column values, in the order specified.
        response = ()
        for c in self.columns:
            response += (row[c],)
        return response

    def getWriter(self):
        return csv.writer(sys.stdout, dialect=self.dialect)
        
    def main(self, *filename):
        """
        The names of comma separated value files, such as might be
        exported from a spreadsheet or database program.
        """
        headers_written = False

        writer = self.getWriter()

        # process the files in order
        for name in filename:
            f = open(name, 'rt')
            try:
                reader = csv.reader(f)

                if self.skip_headers:
                    if not headers_written:
                        # This row must include the headers for the output
                        headers = reader.next()
                        writer.writerow(self.getPrintableColumns(headers))
                        headers_written = True
                    else:
                        # We have seen headers before, and are skipping,
                        # so do not write the first row of this file.
                        ignore = reader.next()

                # Process the rest of the file
                for row in reader:
                    writer.writerow(self.getPrintableColumns(row))
            finally:
                f.close()
        return

if __name__ == '__main__':
    csvcat().run()
