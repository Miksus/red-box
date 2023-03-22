from copy import copy
from typing import Dict
from datetime import date


class BaseQuery:
    def __and__(self, other):
        return ALL(self, other)

    def __or__(self, other):
        return OR(self, other)

    def __invert__(self):
        return NOT(self)


class BaseField(BaseQuery):
    _fields = {}

    def __init__(self, name):
        self._fields[name] = self
        self._name = name


class Flag(BaseField):
    def __str__(self):
        return f"({self._name})"


class ValueField(BaseField):
    "Field that contains a value"

    def __call__(self, value):
        return ValueFilled(self, value)

    def __str__(self):
        raise ValueError(f"Field {self._name} needs a value")


class DateField(ValueField):
    "Field that contains a date value"

    def __call__(self, datelike: date):
        if isinstance(datelike, date):
            # see date-month token (section 9.0 Formal Syntax)
            # https://www.rfc-editor.org/rfc/rfc3501
            imap_months = [
                "",
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]
            return ValueFilled(
                self, f"{datelike.day:02}-{imap_months[datelike.month]}-{datelike.year}"
            )
        return ValueFilled(self, str(datelike))

    def __str__(self):
        raise ValueError(f"Field {self._name} needs a value")


class KeyValueField(BaseField):
    "Field that contains a key and a value"

    def __call__(self, key, value):
        return KeyValueFilled(self, key, value)

    def __str__(self):
        raise ValueError(f"Field {self._name} needs a value")


class CompareField(BaseField):
    "Field that contains a statement"

    def __call__(self, a, b):
        return LogicalFilled(self, (a, b))

    def __str__(self):
        if self._name == "ALL":
            return f"({self._name})"
        raise ValueError(f"{self._name} requires statement")


class NotField(BaseField):
    "NOT field"

    def __call__(self, value):
        return LogicalFilled(self, value)

    def __str__(self):
        raise ValueError(f"{self._name} requires statement")


class LogicalFilled(BaseField):
    def __init__(self, field, values: tuple):
        self._field = field
        self._values = values

    def __str__(self):
        if isinstance(self._values, tuple):
            a, b = self._values
            return f"({self._field._name} {a} {b})"
        else:
            value = self._values
            return f"({self._field._name} {value})"


class ValueFilled(BaseQuery):
    "Field that has already a value"

    def __init__(self, field, value):
        self._field = field
        self._value = value

    def __str__(self):
        return f'({self._field._name} "{self._value}")'


class KeyValueFilled(BaseQuery):
    "Field that has already a key and a value"

    def __init__(self, field, key, value):
        self._field = field
        self._key = key
        self._value = value

    def __str__(self):
        return f'({self._field._name} "{self._key}" "{self._value}")'


ALL = CompareField("ALL")
OR = CompareField("OR")
NOT = NotField("NOT")
