
import pytest
from redbox.query import ALL, NEW, OR, TO, UNSEEN, SINCE, RECENT, NOT, TEXT, HEADER, SUBJECT, SEEN, build

# A282 SEARCH FLAGGED SINCE 1-Feb-1994 NOT FROM "Smith"

# NOT (NEW TEXT "hello")

# ((TO "one@mail.ru") (TO "two@mail.ru"))

@pytest.mark.parametrize(
    "qry,expected",
    [
        pytest.param(ALL, '(ALL)'),
        pytest.param(UNSEEN, '(UNSEEN)'),
        pytest.param(NOT(UNSEEN), '(NOT (UNSEEN))'),
        pytest.param(~UNSEEN, '(NOT (UNSEEN))'),

        pytest.param(SINCE("2022-01-01"), '(SINCE "2022-01-01")'),
        pytest.param(HEADER("Mime-Version", "1.0"), '(HEADER "Mime-Version" "1.0")'),

        pytest.param(NOT(NEW & TEXT("hello")), '(NOT (ALL (NEW) (TEXT "hello")))'),
        pytest.param((SUBJECT('Example 1') & SEEN) | (SUBJECT('Example 2') & ~~SEEN), '(OR (ALL (SUBJECT "Example 1") (SEEN)) (ALL (SUBJECT "Example 2") (NOT (NOT (SEEN)))))'),
        pytest.param(TO("me@example.com") & TO("you@example.com"), '(ALL (TO "me@example.com") (TO "you@example.com"))'),

    ], ids=lambda x: x if isinstance(x, str) else ""
)
def test_expression(qry, expected):
    assert str(qry) == expected

@pytest.mark.parametrize(
    "qry,expected",
    [
        pytest.param(dict(all=True), '(ALL)'),
        pytest.param(dict(unseen=True), '(UNSEEN)'),
        pytest.param(dict(unseen=False), '(NOT (UNSEEN))'),
        pytest.param(dict(seen=True), '(SEEN)'),
        pytest.param(dict(seen=False), '(NOT (SEEN))'),
        pytest.param(dict(since="2022-01-01"), '(SINCE "2022-01-01")'),
        pytest.param(dict(header=('Mime-Version', '1.0')), '(HEADER "Mime-Version" "1.0")'),
        pytest.param(dict(since="2022-01-01", seen=True), '(ALL (SINCE "2022-01-01") (SEEN))'),

        pytest.param(dict(from_="me@example.com"), '(FROM "me@example.com")'),

    ], ids=lambda x: x if isinstance(x, str) else ""
)
def test_compile(qry, expected):
    assert str(build(**qry)) == expected


@pytest.mark.parametrize(
    "qry,expected",
    [
        pytest.param(dict(header={'Mime-Version': '1.0', 'Precedence': 'list'}), '(ALL (HEADER "Mime-Version" "1.0") (HEADER "Precedence" "list"))'),

    ]
)
def test_compile_verbose(qry, expected):
    assert str(build(**qry)) == expected
