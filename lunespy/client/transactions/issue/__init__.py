from lunespy.client.transactions.issue.validators import validate_issue
from lunespy.client.transactions.issue.validators import send_issue
from lunespy.client.transactions.issue.validators import mount_issue
from lunespy.client.transactions import BaseTransaction
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account


class IssueToken(BaseTransaction):
    """
    issue_data: dict
        description: str
        reissuable: bool
        issue_fee: int
        quantity: int
        decimals: int
        name: str
    """
    def __init__(self, sender: Account, **issue_data: dict) -> None:
        super().__init__('Issue Token', issue_data)
        self.sender = sender
        self.issue_data = issue_data
        self.issue_data['token_type'] = 'Token'
        self.history = []


    @property
    def ready(self) -> bool:
        return validate_issue(self.sender, self.issue_data)
    
    @property
    def transaction(self) -> dict:
        return super().transaction(
            mount_tx=mount_issue,
            sender=self.sender,
            issue_data=self.issue_data)

    def send(self, node_url: str = None) -> dict:
        tx = super().send(send_issue, node_url)
        self.history.append(tx)
        return tx

class IssueAsset(IssueToken):
    def __init__(self, sender: Account, **issue_data: dict) -> None:   
        issue_data['token_type'] = 'Asset'
        IssueToken.__init__(self, sender=sender, **issue_data)
        BaseTransaction.__init__(self, tx_type='Issue Asset', tx_data=issue_data)
    

class IssueNFT(IssueToken):
    def __init__(self, sender: Account, **issue_data: dict) -> None:
        issue_data['token_type'] = 'NFT'
        issue_data['decimals'] = 0
        IssueToken.__init__(self, sender=sender, **issue_data)
        BaseTransaction.__init__(self, tx_type='Issue NFT', tx_data=issue_data)
