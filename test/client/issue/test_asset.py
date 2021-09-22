from lunespy.client.transactions.issue import IssueToken
from lunespy.client.wallet import Account

def test_asset_decimals():
    """
        can have decimals parameter more than 0
    """
    sender = Account()
    tx = IssueToken(sender, quantity=1, name='Asset', decimals=3)
    assert tx.issue_data['decimals'] == 3
