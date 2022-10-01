.. _query-fields:

Query Fields
============

This section contains the query keywords which 
can be used with ``inbox.select``. The keywords
can be imported from ``redbox.query``.

Some of the fields take arguments and some of them
don't. The arguments should be passed as a call, 
for example ``FROM('mikael.koli@example.com')``.
Those that don't take arguments should be passed 
as is, for example ``SEEN``.

Read more about the keywords from 
`RFC3501 <https://www.rfc-editor.org/rfc/rfc3501#section-6.4.4>`_.

Field Definitions
-----------------

.. glossary::

    ALL
        All messages.


**Generic Flags**

.. glossary::

    ANSWERED
        Messages with ``\Answered`` flag set.

    UNANSWERED
        Messages without ``\Answered`` flag set.

    DELETED
        Messages with ``\Deleted`` flag set.

    UNDELETED
        Messages without ``\Deleted`` flag.

    DRAFT
        Messages with ``\Draft`` flag set.

    UNDRAFT
        Messages without ``\Draft`` flag.

    FLAGGED
        Messages with ``\Flagged`` flag set.

    UNFLAGGED
        Messages without ``\Flagged`` flag.


**Recency Flags**

.. glossary::

    NEW
        New unread messages. These are messages that have 
        ``\Recent`` flag but not ``\Seen`` flag.

    RECENT
        Messages with ``\RECENT`` flag set.

    OLD
        Messages without ``\RECENT`` flag.

    SEEN
        Messages that have been read. These are 
        messages that have ``\Seen`` flag.

    UNSEEN
        Messages that have been read. These are 
        messages that don't have ``\Seen`` flag.


**Headers**

.. glossary::

    SUBJECT('string')
        Message subject contains the given string.

    TO('string')
        Message's receivers contain given string.

    FROM('string')
        Message's sender contains given string.

    CC('string')
        Message's CC field contains given string.

    BCC('string')
        Message's BCC field contains given string.

    TEXT('string')
        Message's header or body contains given string.

    BODY('string')
        Message's body contains given string.


**Time related**

.. glossary::

    BEFORE('date-like')
        Message's internal date before given date.

    ON('date-like')
        Message's internal date on given date.

    SINCE('date-like')
        Message's internal date on or after given date.

    SENTBEFORE('date-like')
        Message's sent date before given date.

    SENTON('date-like')
        Message's sent date on given date.

    SENTSINCE('date-like')
        Message's sent date on or after given date.


**Size related**

.. glossary::

    LARGER('n')
        Message's ``SIZE`` larger than specified number of octets.

    SMALLER('n')
        Message's ``SIZE`` smaller than specified number of octets.

**Logical**

.. glossary::

    ALL(a, b)
        Both expressions ``a`` and ``b`` is true.

    OR(a, b)
        Either expression ``a`` or expression ``b`` is true.

    NOT(a)
        Expression ``a`` is not true.

**Other**

.. glossary::

    UID('message set')
        Message's unique identifier is in given set.

    KEYWORD('flag')
        Message has given flag.

    UNKEYWORD('flag')
        Message has not given flag.

    HEADER('header', 'value')
        Message has the given header and the header's value
        is the given value.