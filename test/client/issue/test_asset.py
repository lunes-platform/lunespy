from lunespy.client.transactions.issue import Token
from lunespy.client.wallet import Account

def test_asset_decimals():
    """
        can have decimals parameter more than 0
    """
    sender = Account()
    tx = Token(sender, quantity=1, name='Asset', decimals=3)
    assert tx.data_issue['decimals'] == 3
