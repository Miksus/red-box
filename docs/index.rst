
.. meta::
   :description: Red Box is an advanced email reading for Python.
   :keywords: read, email, mailbox, IMAP, Python

.. raw:: html
   :file: header.html

- `Documentation <https://red-box.readthedocs.io/>`_
- `Source code (Github) <https://github.com/Miksus/red-box>`_
- `Releases (PyPI) <https://pypi.org/project/redbox/>`_

This is a sister library for `Red Mail, advanced email sender <https://red-mail.readthedocs.io/>`_.

Why Red Box?
-------------

Reading emails **SHOULD NOT** look like this:

.. code-block:: python

    import imaplib

    # Get message IDs
    s = imaplib.IMAP4_SSL('localhost', port=0)
    s.select("INBOX")
    typ, data = s.search(None, '(ALL (SUBJECT "example 2") (UNSEEN))')
    msg_ids = list(data[0].decode("UTF-8").split(" "))

    # Get message contents
    msgs = []
    for msg_id in msg_ids:
        typ, data = s.fetch(str(msg_id), '(RFC822)')
        content = data[0][1].decide("UTF-8")
        msgs.append(content)

It should look like this:

.. code-block:: python

    from redbox import EmailBox

    box = EmailBox(host="localhost", port=0)
    msgs = box['INBOX'].search(subject="example 2", unseen=True)

Red Box has several features:

- :ref:`Easy email search <querying>`
- :ref:`Easy email message manipulation <message>`
- :ref:`Easy email configuration <config>`

Furthermore, Red Box has custom message type that makes manipulating 
the messages easy:

.. code-block:: python

    # Get one email
    msg = msgs[0]

    # String representation of the message
    print(msg.content)

    # Email contents
    print(msg.text_body)
    print(msg.html_body)

    # Email headers
    print(msg.from_)
    print(msg.to)
    print(msg.date)

Here is a more complete example:

.. code-block:: python

    from redbox import EmailBox

    box = EmailBox(host="localhost", port=0)
    inbox = box['INBOX']

    for msg in inbox.search(subject="example 2", unseen=True):

        # Process the message
        print(msg.subject)
        print(msg.text_body)

        # Set the message as read/seen
        msg.read()

Interested?
-----------

Install the package:

.. code-block:: console

    pip install redbox

:ref:`and get started. <getting-started>`


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorials/index
   versions


Indices and tables
==================

* :ref:`genindex`
