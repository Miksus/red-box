        
from typing import Dict

class Query:
    



class QueryBase:
    
    _components:Dict[str, 'QueryBase'] = {}


    def __init__(self, name):
        self._components[self.name]
        self.name = name

    def __and__(self, other):

        return And(self, other)

    def __or__(self, other):
        comps = []
        for c in (self, other):
            if isinstance(c, Or):
                ...
            if isinstance(c, And):
                raise ValueError("Nested queries not supported")
        return Or(self, other)
        
class Flag(QueryBase):
    def __str__(self):
        return f'{self.name}'
        
class Field(QueryBase):
    def __init__(self, name, value=None):
        super().__init__(name)
        self.value = value
        
    def __call__(self, value):
        self.value = value
        
    def __str__(self):
        return f'{self.name} "{self.value}"'
        
class Or(QueryBase):
        
    def __call__(self, a, b):
        self.left = a
        self.right = b
    
    def __str__(self):
        return f'OR ({self.left} {self.right})'
        
class And(QueryBase):
        
    def __call__(self, a, b):
        self.left = a
        self.right = b
    
    def __str__(self):
        return f'{self.left} {self.right}'

ALL = Flag("ALL")
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


BCC = Field("BCC")
CC = Field("CC")

SUBJECT = Field("SUBJECT")
TEXT = Field("TEXT")
BODY = Field("BODY")

TO = Field("TO")
FROM = Field("FROM")

NOT = Field("NOT")
OR = Or("OR")
ON = Field("ON")


SENTON = Field("SENTON")
SENTBEFORE = Field("SENTBEFORE")
SENTSINCE = Field("SENTSINCE")

BEFORE = Field("BEFORE")
SINCE = Field("SINCE")

LARGER = Field("LARGER")
SMALLER = Field("SMALLER")

UID = Field("UID")
KEYWORD = Field("KEYWORD")
UNKEYWORD = Field("UNKEYWORD")