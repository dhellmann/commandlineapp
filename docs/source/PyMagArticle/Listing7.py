#!/usr/bin/env python
# Initialize the database

from Listing5 import SQLiteAppBase

class showlog(SQLiteAppBase):
    """Show the contents of the log.
    """

    substring = None
    def optionHandler_message(self, substring):
        """Look for messages with the substring.
        """
        self.substring = substring
        return

    def takeAction(self):
        if self.substring:
            pattern = '%' + self.substring + '%'
            c = self.cursor.execute(
                "SELECT * FROM log WHERE message LIKE ?;", 
                (pattern,))
        else:
            c = self.cursor.execute("SELECT * FROM log;")

        for row in c:
            print '%-30s %s' % row
        return 0

if __name__ == '__main__':
    showlog().run()

        
