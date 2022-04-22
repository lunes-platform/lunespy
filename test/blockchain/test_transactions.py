from lunespy.blockchain.transactions import transactions_from_address
from lunespy.blockchain.transactions import unconfirmed_transaction
from pytest import mark


@mark.transactions
@mark.requests
def test_transactions_from_address():
    assert transactions_from_address('37nX3hdCt1GWeSsAMNFmWgbQWZZhbvBG3mX', 2) != []


@mark.transactions
@mark.requests
def test_transactions_from_address_with_wrong_address():
    assert type(transactions_from_address('37nX3hdCt1GWeSMNFmWgbQWZZhbvBG3mX', 2)) == type(None)
