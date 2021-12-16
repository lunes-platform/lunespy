from lunespy.client.transactions import BaseTransaction
from lunespy.client.wallet import Account


class IssueToken(BaseTransaction):
    """
    issue_data: dict
        description: str
        reissuable: bool
        fee: int
        quantity: int
        decimals: int
        name: str
    """
    def __init__(self, sender: Account, name: str = None, reissuable: bool = None,
                 quantity: int = None, decimals: int = None, description: str = None,
                 timestamp: int = None, fee: int = None) -> None:
        from lunespy.utils import drop_none

        self.issue_data = drop_none({
            "name": name,
            "reissuable": reissuable,
            "quantity": quantity,
            "decimals": decimals,
            "description": description,
            "timestamp": timestamp,
            "fee": fee
        })
        super().__init__('Issue Token', self.issue_data)
        self.sender = sender
        self.history = []


    @property
    def ready(self) -> bool:
        from lunespy.client.transactions.issue.validators import validate_issue

        return validate_issue(self.sender, self.issue_data)
    

    @property
    def transaction(self) -> dict:
        from lunespy.client.transactions.issue.validators import mount_issue

        return super().transaction(
            mount_tx=mount_issue,
            sender=self.sender,
            issue_data=self.issue_data)


    def send(self, node_url: str = None) -> dict:
        from lunespy.client.transactions.issue.validators import send_issue

        tx = super().send(send_issue, node_url)
        self.history.append(tx)
        return tx


class IssueAsset(IssueToken):
    def __init__(self, sender: Account, name: str = None, reissuable: bool = None,
                 quantity: int = None, decimals: int = None, description: str = None,
                 timestamp: int = None, fee: int = None) -> None:
        from lunespy.utils import drop_none

        issue_data = drop_none({
            "name": name,
            "reissuable": reissuable,
            "quantity": quantity,
            "decimals": decimals,
            "description": description,
            "timestamp": timestamp,
            "fee": fee
        })
        IssueToken.__init__(self, sender=sender, **issue_data)
        BaseTransaction.__init__(self, tx_type='Issue Asset', tx_data=issue_data)


class IssueNFT(IssueToken):
    def __init__(self, sender: Account, name: str = None, reissuable: bool = None,
                 quantity: int = None, description: str = None, timestamp: int = None,
                 fee: int = None) -> None:
        from lunespy.utils import drop_none

        NFT_is_unique: int = 0
        issue_data = drop_none({
            "name": name,
            "reissuable": reissuable,
            "quantity": quantity,
            "decimals": NFT_is_unique,
            "description": description,
            "timestamp": timestamp,
            "fee": fee
        })
        IssueToken.__init__(self, sender=sender, **issue_data)
        BaseTransaction.__init__(self, tx_type='Issue NFT', tx_data=issue_data)
