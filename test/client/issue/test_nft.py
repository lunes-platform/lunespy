from lunespy.client.transactions.issue import IssueNFT
from lunespy.client.wallet import Account

def test_nft_ready():
    """
        always decimals parameter should be 0
    """
    sender = Account()
    tx = IssueNFT(sender, name="NFT!", quantity=1, decimals=10)
    assert tx.issue_data['decimals'] == 0
