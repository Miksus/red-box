from redbox.box import EmailBox
from . import _version
__version__ = _version.get_versions()['version']

gmail = EmailBox(
    host="imap.gmail.com",
    port=993,
)

outlook = EmailBox(
    host="outlook.office365.com",
    port=993,
)