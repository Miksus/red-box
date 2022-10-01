import imaplib
import email
import re
from typing import Dict, Generator, List, Union

from redbox.models.mailbox import MailFolder
from .query import build
from redbox.models.message import EmailMessage

class EmailBox:
    
    cls_message = EmailMessage
    _mailfolders: List[MailFolder]

    def __init__(self, host, port, username=None, password=None, cls_imap=imaplib.IMAP4_SSL, use_starttls=False):
        
        self.host = host
        self.port = port
        self.username = username
        self.__password = password
        
        self.use_starttls = use_starttls
        self.cls_imap = cls_imap
        self.kws_imap = {}

        self._connection = None
        self._mailfolders = None
        
    def __enter__(self):
        self.connect()

    def __exit__(self, *args):
        self.close()
        
    def __getitem__(self, name: str) -> MailFolder:
        "Get an existing mailbox"
        for mailbox in self.mailfolders:
            if mailbox.name == name:
                return mailbox
        raise KeyError(f"Mailbox {mailbox!r} not found")

    @property
    def mailfolders(self) -> List[MailFolder]:
        if self._mailfolders is None:
            self.update()
        return self._mailfolders

    def get(self, name:str) -> MailFolder:
        "Get mailbox. If not found, not existing mailbox is returned"
        try:
            self[name]
        except KeyError:
            return self._construct_mailbox(name=name)

    def create(self, name:str) -> MailFolder:
        "Create a mailbox"
        mailbox = self._construct_mailbox(name=name)
        mailbox.create()
        return mailbox

    @property
    def inbox(self) -> MailFolder:
        "The main email box"
        for name in ('INBOX', 'Inbox', 'inbox'):
            try:
                return self[name]
            except KeyError:
                pass
        raise KeyError("Inbox not found")

    def update(self):
        "Update list of mailfolders"
        # Outlook: b'(\\HasNoChildren) "/" Archive'
        # Gmail: b'(\\HasNoChildren) "/" "INBOX"'
        self._mailfolders = []
        typ, data = self.connection.list()
        for box_data in data:
            s = box_data.decode("UTF-8")
            # box_data is in form: 
            # - '(\\HasNoChildren) "/" INBOX'
            # - '(\\HasNoChildren) "/" "Inbox"'
            match = re.match(r'^[(](?P<flags>[^")]+)[)] "/" "?(?P<name>[^"]+)', s)
            items = match.groupdict()
            name = items['name']
            flags = items.get('flags').split(' ')
            mailbox = self._construct_mailbox(name=name, flags=flags)

            self._mailfolders.append(mailbox)

    def _construct_mailbox(self, **kwargs) -> MailFolder:
        return MailFolder(**kwargs, cls_message=self.cls_message, session=self.connection)

    def connect(self):
        "Connect to the SMTP Server"
        self._connection = self.get_server()

    def close(self):
        "Close (quit) the connection"
        self._connection.logout()
        self._connection = None
        
    @property
    def connection(self):
        if self._connection is None:
            self.connect()
            return self._connection
        else:
            return self._connection
        
    def get_server(self) -> imaplib.IMAP4:
        "Connect and get the IMAP Server"
        user = self.username
        password = self.__password
        
        server = self.cls_imap(self.host, self.port, **self.kws_imap)
        if self.use_starttls:
            server.starttls()

        if user is not None or password is not None:
            server.login(user, password)
        
        return server
    
    def _format_query(self, _query=None, **kwargs) -> str:
        if _query is None:
            return build(**kwargs)
        else:
            return str(_query)

    @property
    def password(self):
        return '*****'

    @password.setter
    def password(self, value):
        self.__password = value