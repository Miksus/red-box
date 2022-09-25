
# Red Box: Advanced Email Manager (UNDER DEVELOPMENT)
> Next generation email box manager

---

[![Pypi version](https://badgen.net/pypi/v/redmail)](https://pypi.org/project/redbox/)
[![build](https://github.com/Miksus/red-mail/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/Miksus/red-box/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/Miksus/red-mail/branch/master/graph/badge.svg?token=IMR1CQT9PY)](https://codecov.io/gh/Miksus/red-box)
[![Documentation Status](https://readthedocs.org/projects/red-mail/badge/?version=latest)](https://red-box.readthedocs.io/en/latest/)
[![PyPI pyversions](https://badgen.net/pypi/python/redmail)](https://pypi.org/project/redmail/)


## What is it?
Red Box is an advanced email reader library. It is a sister project for Red Mail (advanced email sender).

Install it from PyPI:

```shell
pip install redbox
```

## Why Red Box?

Imaplib from standard library is complex to use and unintuitive. 
Red Box makes reading email boxes easy. 

With Red Box, it is simple as this:

```python
from redmail import EmailSender

box = EmailBox(host="localhost", port=0)

emails = box.search(
    since="2022-01-01",
    sender="you@example.com"
)
```

---

## Author

* **Mikael Koli** - [Miksus](https://github.com/Miksus) - koli.mikael@gmail.com

