from lunespy.server.transactions import transactions_from_address
from lunespy.server.transactions import unconfirmed_transaction
from pytest import mark


@mark.requests
def test_unconfirmed_transaction():
    assert unconfirmed_transaction('http://lunesnode.lunes.io')['status'] == 'ok'


@mark.requests
def test_transactions_from_address():
    assert transactions_from_address('37nX3hdCt1GWeSsAMNFmWgbQWZZhbvBG3mX', 2, 'http://lunesnode.lunes.io')['status'] == 'ok'
