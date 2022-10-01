.. _config:

Configuring for Different Providers
===================================

Configuring Red Box is easy.
If you have your own IMAP server, you just need to 
set the host address, port and possibly the credentials.
There are also pre-configured sender instances for 
common email providers:

=================== =================== ===================== ====
Provider            Sender instance     Host                  Port
=================== =================== ===================== ====
Gmail (Google)      ``redbox.gmail``    imap.gmail.com        993
Outlook (Microsoft) ``redbox.outlook``  outlook.office365.com 993          
=================== =================== ===================== ====

To use them, you may need to configure your account first (see below).

If you use custom email server (ie. your company's IMAP server),
you need to pass the host and port yourself. 

.. code-block:: python

    from redbox import EmailBox
    email = EmailBox(
        host='<your email server>', 
        port=993
    )

Depending on company policy, you might also need to pass the username 
and password:

.. code-block:: python

    from redbox import EmailBox
    email = EmailBox(
        host='<your IMAP server>', 
        port=993,
        username="me@example.com",
        password="<MY PASSWORD>"
    )

.. note::

    By default, Red Box uses ``IMAP4_SSL`` which should be suitable for majority of cases. 
    However, in some cases you may need to use other protocols. See :ref:`custom IMAP configuraiton <config-custom>`.


.. _config-gmail:

Gmail
-----

In order to send emails using Gmail, you need to:

- Set up `2-step verification <https://support.google.com/accounts/answer/185839>`_ (if not already)
- Generate `an App password <https://support.google.com/accounts/answer/185833>`_:

    - Go to your `Google account <https://myaccount.google.com/>`_
    - Go to *Security*
    - Go to *App passwords*
    - Generate a new one (you may use custom app and give it a custom name)

When you have your application password you can use Red Box's gmail object that has the Gmail
server pre-configured:

.. code-block:: python

    from redbox import gmail
    gmail.username = 'example@gmail.com' # Your Gmail address
    gmail.password = '<APP PASSWORD>'

    # And then you can send emails
    gmail.send(
        subject="Example email",
        receivers=['you@example.com'],
        text="Hi, this is an email."
    )


.. _config-outlook:

Outlook
-------

You may also send emails from MS Outlook. To do so, you just need to have a Microsoft
account. There is a pre-configured sender which you may use:

.. code-block:: python

    from redbox import outlook
    outlook.username = 'example@hotmail.com'
    outlook.password = '<YOUR PASSWORD>'

    # And then you can send emails
    outlook.send(
        subject="Example email",
        receivers=['you@example.com'],
        text="Hi, this is an email."
    )

.. _config-custom:

Custom Configuration
--------------------

You can also use other IMAP objects as well from 
`imaplib <https://docs.python.org/3/library/imaplib.html>`_.

.. code-block:: python

    import imaplib
    from redbox import EmailBox

    email = EmailBox(
        host='<your IMAP server>', 
        port=993,
        cls_imap=imaplib.IMAP4
    )

If your IMAP server uses **STARTTLS**:

.. code-block:: python

    import imaplib
    from redbox import EmailBox

    email = EmailBox(
        host='<your IMAP server>', 
        port=993,
        cls_imap=imaplib.IMAP4,
        starttls=True
    )