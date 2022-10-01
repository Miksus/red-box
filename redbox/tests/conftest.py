from pathlib import Path
import pytest
from redbox.testing import DummyGmailImap

ROOT = Path(__file__).parent

@pytest.fixture()
def IMAP4():
    DummyGmailImap.update_emails_()
    return DummyGmailImap