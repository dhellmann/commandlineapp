#!/usr/bin/env
# Base class for sqlite programs.

import sqlite3
import commandlineapp

class SQLiteAppBase(commandlineapp.CommandLineApp):
    """Base class for accessing sqlite databases.
    """

    dbname = 'sqlite.db'
    def optionHandler_db(self, name):
        """Specify the database filename.
        Defaults to 'sqlite.db'.
        """
        self.dbname = name
        return

    def main(self):
        # Subclasses can override this to control the arguments
        # used by the program.
        self.db_connection = sqlite3.connect(self.dbname)
        try:
            self.cursor = self.db_connection.cursor()
            exit_code = self.takeAction()
        except:
            # throw away changes
            self.db_connection.rollback()
            raise
        else:
            # save changes
            self.db_connection.commit()
        return exit_code

    def takeAction(self):
        """Override this in the actual application.
        Return the exit code for the application
        if no exception is raised.
        """
        raise NotImplementedError('Not implemented!')

if __name__ == '__main__':
    SQLiteAppBase().run()
