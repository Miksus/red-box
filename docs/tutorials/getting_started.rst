.. meta::
   :description: Send email in Python. 
   :keywords: send, email, Python

.. _getting-started:

Getting started
===============

Install the package from `Pypi <https://pypi.org/project/redbox/>`_:

.. code-block:: console

    pip install redbox

.. _configure:

Configuring Email Box
---------------------

You can configure your email box by:

.. code-block:: python

   from redbox import EmailBox

   box = EmailBox(
       host='<IMAP HOST>',
       port='<IMAP PORT>',
       username='<USERNAME>',
       password='<PASSWORD>'
   )

.. note::

    The correct IMAP port is typically 993.

There are guides to set up the following email providers:

- :ref:`config-gmail`
- :ref:`config-outlook`

.. note::

    By default, Red Box uses **IMAP4_SSL** as the protocol.
    This is suitable for majority of cases but if you need
    to use other protocols, see :ref:`config-custom`.

List of Folders
---------------

Get list of available email folders:

.. code-block:: python

   box.mailfolders

Selecting a Folder
------------------

To select a folder, you can index the box: 

.. code-block:: python

   inbox = box["INBOX"]

Alternatively you can choose the inbox using:

.. code-block:: python

   inbox = box.inbox

Reading Emails
--------------

To query emails, you can just use ``search`` method:

.. code-block:: python

   inbox.search(unseen=True)

Next tutorial covers reading emails more thoroughly.
