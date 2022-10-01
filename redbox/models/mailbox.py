import imaplib
from typing import List, Type, Union
from pydantic import BaseModel
from redbox.models.message import EmailMessage

from redbox.query import build
from redbox.query.query import BaseQuery


class MailFolder(BaseModel):
    class Config:
        arbitrary_types_allowed=True

    session: imaplib.IMAP4
    name: str
    flags: List[str] = []
    readonly: bool = False

    cls_message: Type[EmailMessage]

    def __str__(self):
        return self.mailbox

    def select(self):
        "Select this mailbox"
        self.session.select(self.name, readonly=self.readonly)

    def create(self):
        "Create the mailbox"
        self.session.create(self.name)

    def rename(self, new_name:str):
        "Set a new name for the mailbox"
        self.session.rename(self.name, new_name)
        self.name = new_name

    def delete(self):
        "Delete the mailbox"
        self.session.delete(self.name)

    def subscribe(self):
        "Subsribe to the mailbox"
        self.session.subscribe(self.name)

    def unsubscribe(self):
        "Unsubscribe to the mailbox"
        self.session.unsubscribe(self.name)

    def search(self, _query:Union[BaseQuery, str]=None, **kwargs) -> List[EmailMessage]:
        "Search the mailbox using given query"
        self.select()

        qry = self._format_query(_query, **kwargs)
        typ, msg_ids = self.session.search(None, qry)
        ids_messages = list(msg_ids[0].decode("UTF-8").split(" "))
        if ids_messages == ['']:
            # No messages found
            return []
        return [
            self.cls_message(uid=int(uid), session=self.session, mailbox=self.name)
            for uid in ids_messages
        ]
    
    def _format_query(self, _query=None, **kwargs) -> str:
        if _query is None:
            return build(**kwargs)
        else:
            return str(_query)