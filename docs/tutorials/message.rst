.. _message:

Message
=======

This section covers how to use the Red Box message object.
An instance of the message object is returned from the 
search methods, for example:

.. code-block:: python

    msgs = inbox.search(unseen=True)

    # Get one message
    msg = msgs[0]

This instance contains the UID (unique identifier) of the 
email message and the connection object. The instance itself
fetches its content and other metadata when needed. 

Reading Content
---------------

Here is an example of how to read some relevant parts of
the content of the email:

.. code-block:: python

    # Get some header information
    print(msg.from_)
    print(msg.to)
    print(msg.subject)
    print(msg.date)

    # Get text body of the email
    print(msg.text_body)

    # Get HTML body of the email
    print(msg.html_body)

If you wish to have more low-level access to the message:

.. code-block:: python

    # Get raw message content
    print(msg.content)

    # Convert to email.messages.EmailMessage (from standard library)
    print(msg.email)

Reading Flags
-------------

Email messages also may have flags.

- ``\Seen``: The message has been read.
- ``\Flagged``: The message has been flagged (ie. it is important).
- ``\Deleted``: The message has been marked to be deleted.
- ``\Draft``: The message is draft.

These flags can also be read as boolean attributes:

.. code-block:: python

    msg.seen
    msg.flagged
    msg.deleted
    msg.draft

You can also get the flags as list:

.. code-block:: python

    msg.flags


Settings Flags
--------------

The flags can also be manipulated. For example:

.. code-block:: python

    # Read the message
    msg.read()

    # Set the message not read
    msg.unread()

    # Flag the message
    msg.flag()

    # Remove the flag from the message
    msg.unflag()

    # Mark the message as deleted
    msg.delete()

    # Unmark the message as deleted
    msg.undelete()

You can also 