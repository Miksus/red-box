import pytest

import imaplib

imaplib.IMAP4

class DummyClass: pass

class DummyImap(imaplib.IMAP4):

    _users = [
        ("")
    ]

    def open(self, host = '', port = 134):
        """Setup connection to remote server on "host:port"
            (default: localhost:standard IMAP4 port).
        This connection will be used by the routines:
            read, readline, send, shutdown.
        """
        self.host = host
        self.port = port
        self.sock = DummyClass()
        self.file = DummyClass()

    def _connect(self):
        self.welcome = ""
        if 'PREAUTH' in self.untagged_responses:
            self.state = 'AUTH'
        elif 'OK' in self.untagged_responses:
            self.state = 'NONAUTH'
        else:
            raise self.error(self.welcome)

    def shutdown(self):
        ...

    def _simple_command(name, *args):
        ...

    def select(self, mailbox='INBOX', readonly=False):
        ...

    def search(self, charset, *criteria):
        ...

    def login(self, user, password):
        if (user, password) not in self._users:
            raise self.error()
        self.state = 'AUTH'
