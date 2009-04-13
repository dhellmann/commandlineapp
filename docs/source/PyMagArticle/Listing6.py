#!/usr/bin/env python
# Initialize the database

import time
from Listing5 import SQLiteAppBase

class initdb(SQLiteAppBase):
    """Initialize a database.
    """

    def takeAction(self):
        self.statusMessage('Initializing database %s' % self.dbname)
        # Create the table
        self.cursor.execute("CREATE TABLE log (date text, message text)")
        # Log the actions taken
        self.cursor.execute(
            "INSERT INTO log (date, message) VALUES (?, ?)",
            (time.ctime(), 'Created database'))
        self.cursor.execute(
            "INSERT INTO log (date, message) VALUES (?, ?)",
            (time.ctime(), 'Created log table'))
        return 0

if __name__ == '__main__':
    initdb().run()

        
