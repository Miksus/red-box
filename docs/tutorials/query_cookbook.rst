
Query Cookbook
==============

This section contains useful examples for 
querying messages.

Querying
--------

Here are various ways to query all messages
from the email box:

.. code-block:: python

    from redbox.query import ALL

    mailbox.search(all=True)
    mailbox.search(ALL)
    mailbox.search("ALL")