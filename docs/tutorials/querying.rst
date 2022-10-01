.. _querying:

Querying Mails
==============

There are three ways to query Red Box:

- Using keyword arguments
- Using query language
- Using raw IMAP language

All of these methods use the method ``search``
but the arguments are different. 

Keyword arguments are converted to the query language
and the query language is converted to raw IMAP language.
Here is an illustration of these options:

.. code-block:: python

    from redbox.query import SUBJECT, UNSEEN

    # Keywords
    inbox.search(subject="example 2", unseen=True)

    # Query language
    inbox.search(SUBJECT("example 2") & UNSEEN)

    # Raw IMAP
    inbox.search('(ALL (SUBJECT "example 2") (UNSEEN))')

These all result to the same query.

Using Keyword Arguments
-----------------------

Keyword arguments are converted to the query language
by turning their keys to upper case. Also, because 
``from`` is a Python keyword, the trailing underscores
are removed. For example, 

Those fields that don't take arguments, boolean value 
should be passed. If the field do take an argument,
the argument should be passed as the value. 

Here are some examples:

.. code-block:: python

    # Get all unread emails
    inbox.search(unseen=True)

    # Get all emails from specific email
    inbox.search(from_="friend@example.com")

You can also pass multiple keyword arguments. 
These are combined with **AND** operator.

.. code-block:: python

   inbox.search(subject="Could we talk?", to="brother@example.com")

Read more about the fields from :ref:`query fields <query-fields>`.

Using Query Language
--------------------

The query language is a set of instances that can be
combined. Some of the 

Here are some examples:

.. code-block:: python

    from redbox.query import SEEN, FROM, HEADER

    inbox.search(SEEN)
    inbox.search(FROM('parents@example.com'))

There are also logical operations. 

.. code-block:: python

    from redbox.query import TO, TEXT, FROM

    # AND operation
    inbox.search(TO('mother@example.com') & TEXT('I miss you.'))

    # OR operation
    inbox.search(FROM('mother@example.com') | FROM('father@example.com'))

    # NOT operation
    inbox.search(~FROM('crush@example.com'))

Read more about the fields from :ref:`query fields <query-fields>`.

Using Raw IMAP Language
-----------------------

To use raw IMAP search language, just pass the query in
string: 

.. code-block:: python

    inbox.search('(ALL (SUBJECT "I'm sorry") (UNSEEN))')

Read more about the keywords from 
`RFC3501 <https://www.rfc-editor.org/rfc/rfc3501#section-6.4.4>`_.