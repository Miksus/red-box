import datetime
from email.message import Message
from pathlib import Path
from textwrap import dedent
import pytest
from redbox import EmailBox
from redbox.models import EmailMessage
from redbox.testing import DummyGmailImap
from redbox.query import FROM, RECENT, SEEN, SUBJECT, UNSEEN
from redbox.tests import __file__ as PATH_TEST

ROOT = Path(PATH_TEST).parent / "examples"

def test_fetch(IMAP4):
    box = EmailBox(host="localhost", port=0, cls_imap=DummyGmailImap)
    
    msg = EmailMessage(uid=1, session=box.inbox.session, mailbox="MYBOX")
    assert msg.content == (ROOT / "MYBOX/1.eml").read_text()
    assert isinstance(msg.email, Message)

    assert msg.text_body == dedent("""
        Hi,

        this is an example.

        - Mikael
        """
    )[1:]
    assert msg.html_body == """<div dir="ltr">Hi,<div><br></div><div>this is an example.</div><div><br></div><div>- Mikael</div></div>\n"""
    assert msg.from_ == "Mikael Koli <miksus@example.com>"
    assert msg.to == ["Receiver <receiver@example.com>"]
    assert msg.headers == {
        'MIME-Version':'1.0',
        'Date':'Sat, 1 Oct 2022 00:23:04 +0300',
        'Message-ID':'<CA+kW7VxrFDRYL=toDadUGpQxYKUHmUji9qQoV2-pSfn9_=BX_w@mail.gmail.com>',
        'Subject':'Example 2',
        'From':'Mikael Koli <miksus@example.com>',
        'To':'Receiver <receiver@example.com>',
        'Content-Type':'multipart/alternative; boundary="00000000000078e58e05e9eb99a5"',
    }
    assert msg.date == datetime.datetime(2022, 10, 1, 0, 23, 4, tzinfo=datetime.timezone(datetime.timedelta(hours=3)))

    # Flags
    assert msg.flags == ['\\Flagged', '\\Seen']
    assert msg.flagged
    assert msg.seen
    assert not msg.deleted
    assert not msg.draft

def test_set_flags(IMAP4):
    box = EmailBox(host="localhost", port=0, cls_imap=DummyGmailImap)
    
    msg = EmailMessage(uid=1, session=box.inbox.session, mailbox="MYBOX")
    assert msg.seen
    assert msg.flagged
    assert not msg.deleted
    msg.set(seen=False, flagged=True, deleted=True)

    assert not msg.seen
    assert msg.flagged
    assert msg.deleted

def test_set_flags_methods(IMAP4):
    box = EmailBox(host="localhost", port=0, cls_imap=DummyGmailImap)
    
    msg = EmailMessage(uid=2, session=box.inbox.session, mailbox="MYBOX")
    assert not msg.seen
    assert not msg.flagged
    assert not msg.deleted
    
    msg.read()
    msg.delete()
    msg.flag()
    assert msg.seen
    assert msg.flagged
    assert msg.deleted

    msg.unread()
    msg.undelete()
    msg.unflag()
    assert not msg.seen
    assert not msg.flagged
    assert not msg.deleted