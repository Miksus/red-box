import imaplib
import email
from typing import Union
from .query import build
from redbox.models import EmailMessage as RedEmailMessage

from email.message import EmailMessage

class EmailBox:
    
    cls_message = EmailMessage

    def __init__(self, host, port, username, password, mailbox="INBOX", cls_imap=imaplib.IMAP4_SSL, use_starttls=False):
        
        self.host = host
        self.port = port
        self.username = username
        self.__password = password
        
        self.use_starttls = use_starttls
        self.cls_imap = cls_imap
        self.kws_imap = {}
        
        self.mailbox = mailbox

        self._connection = None
        
    def __enter__(self):
        self.connect()

    def __exit__(self, *args):
        self.close()
        
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
        
        server.select(self.mailbox)
        return server

    def search(self, _query:Union['QueryBase', str]=None, **kwargs):
        qry = self._format_query(_query, **kwargs)
        typ, msg_ids = self.connection.search(None, qry)
        ids_messages = list(msg_ids[0].decode("UTF-8").split(" "))
        for id in ids_messages:
            yield self._fetch(id)
    
    def _fetch(self, num):
        typ, data = self.connection.fetch(str(num),'(RFC822)')
        cls = self.cls_message
        msg_string = data[0][1].decode("UTF-8")
        if cls is EmailMessage:
            msg = cls.message_from_string(msg_string)
        else:
            # Custom class
            msg = cls.from_string(msg_string)
        msg.message_num = num
        return msg
    
    def _format_query(self, _query=None, **kwargs) -> str:
        if _query is None:
            return build(**kwargs)
        else:
            return str(_query)