#!/usr/bin/env python
# Initialize the database

import time
from Listing5 import SQLiteAppBase

class updatelog(SQLiteAppBase):
    """Add to the contents of the log.
    """

    def main(self, message):
        """Provide the new message to add to the log.
        """
        # Save the message for use in takeAction()
        self.message = message
        return SQLiteAppBase.main(self)

    def takeAction(self):
        self.cursor.execute(
            "INSERT INTO log (date, message) VALUES (?, ?)",
            (time.ctime(), self.message))
        return 0

if __name__ == '__main__':
    updatelog().run()

        
