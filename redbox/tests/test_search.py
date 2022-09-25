from redbox import EmailBox

def test_search():
    box = EmailBox(host="localhost", port=0, cls_imap=)
    assert box.search(unseen=True, recent=True)