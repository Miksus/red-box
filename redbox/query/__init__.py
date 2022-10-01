from .query import Flag, ValueField, KeyValueField, ALL, OR, NOT, BaseField

HEADER = KeyValueField("HEADER")

ANSWERED = Flag("ANSWERED")
UNANSWERED = Flag("UNANSWERED")
DELETED = Flag("DELETED")
UNDELETED = Flag("UNDELETED")

DRAFT = Flag("DRAFT")
UNDRAFT = Flag("UNDRAFT")

FLAGGED = Flag("FLAGGED")
UNFLAGGED = Flag("UNFLAGGED")

NEW = Flag("NEW")

RECENT = Flag("RECENT")
OLD = Flag("OLD")

SEEN = Flag("SEEN")
UNSEEN = Flag("UNSEEN")


BCC = ValueField("BCC")
CC = ValueField("CC")

SUBJECT = ValueField("SUBJECT")
TEXT = ValueField("TEXT")
BODY = ValueField("BODY")

TO = ValueField("TO")
FROM = ValueField("FROM")

ON = ValueField("ON")


SENTON = ValueField("SENTON")
SENTBEFORE = ValueField("SENTBEFORE")
SENTSINCE = ValueField("SENTSINCE")

BEFORE = ValueField("BEFORE")
SINCE = ValueField("SINCE")

LARGER = ValueField("LARGER")
SMALLER = ValueField("SMALLER")

UID = ValueField("UID")
KEYWORD = ValueField("KEYWORD")
UNKEYWORD = ValueField("UNKEYWORD")

def _build(key:str, val):
    # Turning from_ --> "FROM", "to" --> "TO" etc.
    key = key.upper().rstrip("_")
    obj = BaseField._fields[key]
    if isinstance(obj, Flag) or obj is ALL:
        if val:
            yield obj
        else:
            yield NOT(obj)
    elif isinstance(obj, ValueField):
        yield obj(val)
    elif isinstance(obj, KeyValueField):
        if isinstance(val, dict):
            for key, subval in val.items():
                yield obj(key, subval)
        else:
            yield obj(*val)
    else:
        raise TypeError("Invalid field")

def build(**kwargs) -> str:
    qry = None
    for key, val in kwargs.items():
        for cmp in _build(key, val):
            if qry is None:
                qry = cmp
            else:
                qry &= cmp
    return str(qry)