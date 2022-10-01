import datetime
import email
from email.message import EmailMessage
import imaplib
import re
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, PrivateAttr, validator
from redbox.utils.inspector import Inspector

# https://datatracker.ietf.org/doc/html/rfc2060.html

class EmailMessage(BaseModel):
    """Simplified representation of an email"""
    class Config:
        arbitrary_types_allowed = True

    session: imaplib.IMAP4 = Field(description="Connection session.")
    uid: int = Field(description="ID of the message.")
    mailbox: str = Field(description="Mailbox in which the message is in.")

    _content: str = PrivateAttr(default=None)
    _flags: List[str] = PrivateAttr(default=None)

    def __str__(self):
        return self.content

    def fetch_all(self):
        msg, flags = self._fetch("(RFC822 FLAGS)")
        self._content = msg
        self._flags = self._parse_flags(flags)

# Email content related

    @property
    def content(self) -> List[str]:
        if self._content is None:
            self._content = self._fetch_content()
        return self._content

    @property
    def email(self) -> EmailMessage:
        return email.message_from_string(self.content)

    @property
    def html_body(self) -> str:
        msg = self.email
        insp = Inspector(msg)
        return insp.get_html_body()

    @property
    def text_body(self) -> str:
        msg = self.email
        insp = Inspector(msg)
        return insp.get_text_body()

# Content headers

    @property
    def headers(self) -> Dict[str, str]:
        msg = self.email
        insp = Inspector(msg)
        return insp.get_headers()

    @property
    def from_(self) -> str:
        headers = {k.lower(): v for k, v in self.headers.items()}
        return headers['from']

    @property
    def to(self) -> List[str]:
        headers = {k.lower(): v for k, v in self.headers.items()}
        to = headers['to']
        return re.split(r", ?", to)

    @property
    def subject(self) -> str:
        headers = {k.lower(): v for k, v in self.headers.items()}
        return headers['subject']

    @property
    def date(self) -> Dict[str, str]:
        headers = {k.lower(): v for k, v in self.headers.items()}
        date = headers['date']
        return datetime.datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")

    def read(self):
        "Read the message (set flag '\Seen')"
        self.set(seen=True)

    def unread(self):
        "Unread the message (remove flag '\Seen')"
        self.set(seen=False)

    def flag(self):
        "Flag the message (set flag '\Flagged')"
        self.set(flagged=True)

    def unflag(self):
        "Remove flag from the message (remove flag '\Flagged')"
        self.set(flagged=False)

    def delete(self):
        "Delete the message (set flag '\Deleted')"
        self.set(deleted=True)

    def undelete(self):
        "Undelete the message (remove flag '\Deleted')"
        self.set(deleted=False)

# Flags

    @property
    def flags(self) -> List[str]:
        if self._flags is None:
            self.update_flags()
        return self._flags

    @property
    def seen(self):
        "Whether the email is read"
        return r"\Seen" in self.flags

    @property
    def flagged(self):
        "Whether the email is read"
        return r"\Flagged" in self.flags

    @property
    def deleted(self):
        "Whether the email is read"
        return r"\Deleted" in self.flags

    @property
    def draft(self):
        "Whether the email is read"
        return r"\Draft" in self.flags

# Utils

    def _fetch(self, part:str) -> list:
        self.session.select(self.mailbox)
        typ, data = self.session.fetch(str(self.uid), part)
        if typ != "OK":
            raise ConnectionError(f"Error with IMAP: {typ}")

        outputs = []
        for output in data:
            if isinstance(output, tuple):
                # Probably message which are in form:
                # (b'12345 (RFC822 {123456}', b'Return-Path: <...0759==--\r\n')
                output = output[1].decode("UTF-8")
            elif isinstance(output, bytes):
                # Probably byte string
                output = output.decode("UTF-8")
            outputs.append(output)
        return outputs

    def _store(self, command, flags):
        self.session.select(self.mailbox)
        self.session.store(str(self.uid), command, flags)

    def update_flags(self):
        self._flags = self._fetch_flags()

# Modify flags

    def add_flag(self, *flags:str):
        # \Deleted \Flagged \Seen
        flag_set = ' '.join(flags) 
        self._store('+FLAGS', flag_set)

    def set_flag(self, *flags:str):
        # \Deleted \Flagged \Seen
        flag_set = ' '.join(flags) 
        self._store('FLAGS', flag_set)

    def remove_flag(self, *flags:str):
        flag_set = ' '.join(flags) 
        self._store('-FLAGS', flag_set)

    def set(self, seen:bool=None, flagged:bool=None, answered:bool=None, draft:bool=None, deleted:bool=None):
        "Set/unset flags"
        kwargs = {
            r'\Seen': seen,
            r'\Flagged': flagged,
            r'\Answered': answered,
            r'\Draft': draft,
            r'\Deleted': deleted,
        }
        add_flags = [key for key, val in kwargs.items() if val]
        del_flags = [key for key, val in kwargs.items() if not val and val is not None]
        if add_flags:
            self.add_flag(*add_flags)
        if del_flags:
            self.remove_flag(*del_flags)

        self.update_flags()

    def _fetch_content(self):
        # Equivalent to BODY[]
        return self._fetch('(RFC822)')[0]

    def _fetch_flags(self) -> List[str]:
        out = self._fetch('(FLAGS)')[0]
        return self._parse_flags(out)

    def _parse_flags(self, flags:str) -> List[str]:
        flags = re.sub(r'^[0-9]* [(]FLAGS [(]', '', flags)
        return flags.strip("()").split(" ")

