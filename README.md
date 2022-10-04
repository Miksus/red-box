
# Red Box: Advanced Email Box Reader
> Next generation email box reader/manager

---

[![Pypi version](https://badgen.net/pypi/v/redbox)](https://pypi.org/project/redbox/)
[![build](https://github.com/Miksus/red-box/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/Miksus/red-box/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/Miksus/red-box/branch/master/graph/badge.svg?token=IMR1CQT9PY)](https://codecov.io/gh/Miksus/red-box)
[![Documentation Status](https://readthedocs.org/projects/red-box/badge/?version=latest)](https://red-box.readthedocs.io)
[![PyPI pyversions](https://badgen.net/pypi/python/redbox)](https://pypi.org/project/redbox/)

- [Documentation](https://red-box.readthedocs.io)
- [Source code](https://github.com/Miksus/red-box)
- [Releases](https://pypi.org/project/redbox/)

## What is it?
Red Box is an advanced email box reader library. It is a sister library for [Red Mail, advanced email sender](https://github.com/Miksus/red-mail). It makes managing your email box in Python very easy.

Core features:

- Easy email searching
- Intuitive message manipulation
- Intuitive email box manipulation

Install it from PyPI:

```shell
pip install redbox
```

## Why Red Box?

Imaplib from standard library is complex to use and unintuitive. 
Red Box makes reading email boxes easy. 

With Red Box, it is simple as this:

```python
from redbox import EmailBox

# Create an email box instance
box = EmailBox(host="localhost", port=0)

# Select an email folder
inbox = box['INBOX']

# Get emails
emails = inbox.search(
    from_="mikael.koli@example.com",
    subject="Red Box released",
    unseen=True
)
```

## More Examples

There is also a query language for arbitrary search queries:

```python
from redbox.query import FROM, UNSEEN, FLAGGED

emails = inbox.search(
    FROM('mikael.koli@example.com') & (UNSEEN | FLAGGED)
)
```

Red Box also makes reading different parts of the email messages
easy:

```python
# Get one email
email = emails[0]

# String representation of the message
print(email.content)

# Email contents
print(email.text_body)
print(email.html_body)

# Email headers
print(email.from_)
print(email.to)
print(email.date)
```

Here is a complete example:

```python

from redbox import EmailBox

box = EmailBox(host="localhost", port=0)
inbox = box['INBOX']

for msg in inbox.search(subject="example 2", unseen=True):

    # Process the message
    print(msg.subject)
    print(msg.text_body)

    # Set the message as read/seen
    msg.read()
```

---

See more from the documentation.

If the library helped you save time, consider buying a coffee for the maintainer ☕.

## Author

* **Mikael Koli** - [Miksus](https://github.com/Miksus) - koli.mikael@gmail.com

