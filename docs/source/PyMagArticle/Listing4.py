#!/usr/bin/env python
# Illustrate verbose level controls.

import commandlineapp

class verbose_app(commandlineapp.CommandLineApp):
    "Demonstrate verbose level controls."

    def main(self):
        for i in range(1, 10):
            self.status_message('Level %d' % i, i)
        return 0

if __name__ == '__main__':
    verbose_app().run()


