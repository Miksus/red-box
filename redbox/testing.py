import imaplib
import json
from pathlib import Path

class PlaceHolder: pass

def get_some_number(num):
    "Get a number (unknown yet what it is for)"
    return '1234'

class DummyGmailImap(imaplib.IMAP4):
    "Imitates imaplib.IMAP4 for testing purposes"
    _users = []

    _emails = {}
    _flags = {}

    def open(self, host = '', port = 134, timeout=None):
        """Setup connection to remote server on "host:port"
            (default: localhost:standard IMAP4 port).
        This connection will be used by the routines:
            read, readline, send, shutdown.
        """
        self.host = host
        self.port = port
        self.sock = PlaceHolder()
        self.file = PlaceHolder()

    def _connect(self):
        self.capabilities = ('IMAP4REV1', 'UNSELECT', 'IDLE', 'NAMESPACE', 'QUOTA', 'ID', 'XLIST', 'CHILDREN', 'X-GM-EXT-1', 'XYZZY', 'SASL-IR', 'AUTH=XOAUTH2', 'AUTH=PLAIN', 'AUTH=PLAIN-CLIENTTOKEN', 'AUTH=OAUTHBEARER', 'AUTH=XOAUTH')
        self.PROTOCOL_VERSION = 'IMAP4REV1'

    def shutdown(self):
        ...

    def _simple_command(name, *args):
        ...

    def list(self):
        # ('OK', [b'(\\HasNoChildren) "/" "INBOX"', ...])
        boxes = self._emails.keys()
        return (
            'OK', 
            [f'(\\HasNoChildren) "/" "{box_name}"'.encode() for box_name in boxes]
        )

    def select(self, mailbox='INBOX', readonly=False):
        self._current_box = mailbox

    def search(self, charset, *criteria):
        if charset not in ("UTF-8", "ascii", None):
            return _fetch_bad_charset()
        if criteria in [("(ALL)",)]:
            # Should return like:
            # ('OK', [b'1 2 3 4'])
            ids = ' '.join(self._emails)
            return ('OK', [ids.encode()])
        elif criteria in [('(SUBJECT "NOT FOUND")',)]:
            return _fetch_missing()

        elif criteria in [('(SUBJECT "example 1")',)]:
            return ('OK', [b'1'])

        elif criteria in [('(ALL (SUBJECT "example 2") (UNSEEN))',)]:
            return ('OK', [b'2'])
        elif criteria == ('(ALL (ALL (SUBJECT "example 2") (SEEN)) (FROM "miksus@example.com"))',):
            return ('OK', [b'2'])
        raise NotImplementedError(criteria)

    def fetch(self, message_set, message_parts):
        """Fetch (parts of) messages.

        (typ, [data, ...]) = <instance>.fetch(message_set, message_parts)

        'message_parts' should be a string of selected parts
        enclosed in parentheses, eg: "(UID BODY[TEXT])".

        'data' are tuples of message part envelope and data.
        """
        if not isinstance(message_set, str):
            raise TypeError("can't concat int to bytes")
        elif message_parts == '(RFC822)':
            # (RFC822) is the message itself
            num = message_set
            # Return messages
            message = self.get_emails_(self._current_box).get(num)
            is_message_found = message is not None
            if not is_message_found:
                # No message found
                return ('OK', [None])
            else:
                # Found a message
                return (
                    'OK',
                    [
                        # No idea why it seems to return this sh*t (with Gmail) but whatever
                        (f'{num} (RFC822 {"{"+get_some_number(num)+"}"}'.encode(), message.encode()),
                        b')'
                    ]
                )
        elif message_parts == '(FLAGS)':
            # ie.: [b'18919 (FLAGS (\\Flagged \\Seen))']
            id = message_set
            flags = ' '.join(self._flags[self._current_box][id])
            return (
                'OK',
                [f'{id} (FLAGS ({flags}))']
            )
        else:
            raise self.error("FETCH command error: BAD [b'Could not parse command']")

    def store(self, message_set, command, flags):
        if command == '+FLAGS':
            self._flags[self._current_box][message_set] += flags.split(" ")
            return
        elif command == '-FLAGS':
            for flag in flags.split(" "):
                self._flags[self._current_box][message_set].remove(flag)
            return
        raise NotImplementedError

    def login(self, user, password):
        if (user, password) not in self._users:
            raise self.error()
        self.state = 'AUTH'

    @classmethod
    def update_emails_(cls):
        for item in (Path(__file__).parent / "tests/examples").glob('**/*'):
            if item.is_dir():
                cls._update_emails(item, box=item.name)

    @classmethod
    def _update_emails(cls, path:Path, box:str="INBOX"):
        "Update the messages in the local store"
        msgs = []
        for i, msg in enumerate(path.glob("*.eml")):
            msgs.append((msg.name, msg.read_text()))
        msgs = sorted(msgs)
        cls._emails[box] = {str(i): msg for i, (name, msg) in enumerate(msgs, start=1)}

        flags = json.loads((path / "flags.json").read_text())
        cls._flags[box] = {str(i): flags.get(name, []) for i, (name, msg) in enumerate(msgs, start=1)}

    def get_emails_(self, box):
        return self._emails[box]

# Verified Calls
# --------------

def _fetch_bad_charset():
    # imap.search("X", "SUBJECT ...")
    return ('NO', [b'[BADCHARSET]'])

def _fetch_missing():
    # imap.search(None, 'SUBJECT "NON EXISTENT"')
    return ('OK', [b''])