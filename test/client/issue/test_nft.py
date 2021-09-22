from lunespy.client.transactions.issue import NFT
from lunespy.client.wallet import Account

def test_nft_ready():
    """
        always decimals parameter should be 0
    """
    sender = Account()
    tx = NFT(sender, name="NFT!", quantity=1, decimals=10)
    assert tx.data_issue['decimals'] == 0
