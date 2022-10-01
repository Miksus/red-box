import pytest
from redbox import EmailBox
from redbox.models import EmailMessage
from redbox.testing import DummyGmailImap
from redbox.query import FROM, RECENT, SEEN, SUBJECT, UNSEEN

def test_box(IMAP4):
    box = EmailBox(host="localhost", port=0, cls_imap=IMAP4)
    assert box['INBOX'] is box.inbox

    with pytest.raises(KeyError):
        box['NOT-EXISTING']

def test_search_not_found(IMAP4):
    box = EmailBox(host="localhost", port=0, cls_imap=IMAP4)
    inbox = box.inbox
    assert inbox.search(subject="NOT FOUND") == []

def test_search_found(IMAP4):
    box = EmailBox(host="localhost", port=0, cls_imap=IMAP4)
    inbox = box.inbox
    assert inbox.search(subject="example 1") == [
        EmailMessage(uid=1, session=inbox.session, mailbox="INBOX")
    ]
    assert inbox.search(subject="example 2", unseen=True) == [
        EmailMessage(uid=2, session=inbox.session, mailbox="INBOX"),
    ]
    assert inbox.search(subject="example 2", seen=True, from_="miksus@example.com") == [
        EmailMessage(uid=2, session=inbox.session, mailbox="INBOX"),
    ]

def test_search_query(IMAP4):
    box = EmailBox(host="localhost", port=0, cls_imap=IMAP4)
    inbox = box.inbox
    assert inbox.search(SUBJECT("example 1")) == [
        EmailMessage(uid=1, session=inbox.session, mailbox="INBOX")
    ]
    assert inbox.search(SUBJECT("example 2") & UNSEEN) == [
        EmailMessage(uid=2, session=inbox.session, mailbox="INBOX"),
    ]
    assert inbox.search(SUBJECT("example 2") & SEEN & FROM('miksus@example.com')) == [
        EmailMessage(uid=2, session=inbox.session, mailbox="INBOX"),
    ]

def test_search_string(IMAP4):
    box = EmailBox(host="localhost", port=0, cls_imap=IMAP4)
    inbox = box.inbox
    assert inbox.search('(SUBJECT "example 1")') == [
        EmailMessage(uid=1, session=inbox.session, mailbox="INBOX")
    ]
    assert inbox.search('(ALL (SUBJECT "example 2") (UNSEEN))') == [
        EmailMessage(uid=2, session=inbox.session, mailbox="INBOX"),
    ]
    assert inbox.search('(ALL (ALL (SUBJECT "example 2") (SEEN)) (FROM "miksus@example.com"))') == [
        EmailMessage(uid=2, session=inbox.session, mailbox="INBOX"),
    ]