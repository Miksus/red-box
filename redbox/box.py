import imaplib
import email
import re
from typing import Dict, Generator, List, Union

from redbox.models.mailbox import MailBox
from .query import build
from redbox.models.message import EmailMessage

class EmailBox:
    
    cls_message = EmailMessage
    _mailboxes: List[MailBox]

    def __init__(self, host, port, username=None, password=None, cls_imap=imaplib.IMAP4_SSL, use_starttls=False):
        
        self.host = host
        self.port = port
        self.username = username
        self.__password = password
        
        self.use_starttls = use_starttls
        self.cls_imap = cls_imap
        self.kws_imap = {}

        self._connection = None
        self._mailboxes = None
        
    def __enter__(self):
        self.connect()

    def __exit__(self, *args):
        self.close()
        
    def __getitem__(self, name: str) -> MailBox:
        "Get an existing mailbox"
        for mailbox in self.mailboxes:
            if mailbox.name == name:
                return mailbox
        raise KeyError(f"Mailbox {mailbox!r} not found")

    @property
    def mailboxes(self) -> List[MailBox]:
        if self._mailboxes is None:
            self.update()
        return self._mailboxes

    def get(self, name:str) -> MailBox:
        "Get mailbox. If not found, not existing mailbox is returned"
        try:
            self[name]
        except KeyError:
            return self._construct_mailbox(name=name)

    @property
    def inbox(self) -> MailBox:
        "The main email box"
        return self["INBOX"]

    def update(self):
        "Update list of mailboxes"
        self._mailboxes = []
        typ, data = self.connection.list()
        for box_data in data:
            s = box_data.decode("UTF-8")
            match = re.match(r'^[(](?P<flags>.+)[)] "/" "(?P<name>.+)"', s)
            items = match.groupdict()
            name = items['name']
            flags = items.get('flags').split(' ')
            mailbox = self._construct_mailbox(name=name, flags=flags)

            self._mailboxes.append(mailbox)

    def _construct_mailbox(self, **kwargs) -> MailBox:
        return MailBox(**kwargs, cls_message=self.cls_message, session=self.connection)

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