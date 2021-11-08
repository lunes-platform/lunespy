from lunespy.client.transactions.cancel_lease.validators import validate_cancel
from lunespy.client.transactions.cancel_lease.validators import mount_cancel
from lunespy.client.transactions.cancel_lease.validators import send_cancel
from lunespy.client.transactions import BaseTransaction
from lunespy.client.wallet import Account


class CancelLease(BaseTransaction):
    """
    cancel_data: dict
        lease_tx_id: str
        cancel_fee: int
        timestamp: int
    """
    def __init__(self, sender: Account, **cancel_data: dict) -> None:
        super().__init__('Create Lease', cancel_data)
        self.sender: Account = sender
        self.cancel_data: dict = cancel_data
        self.history: list = []

    
    @property
    def ready(self) -> bool:
        return validate_cancel(self.sender, self.cancel_data)


    @property
    def transaction(self) -> dict:
        return super().transaction(
            mount_tx=mount_cancel,
            sender=self.sender,
            cancel_data=self.cancel_data)

    def send(self, node_url: str = None) -> dict:
        tx = super().send(send_cancel, node_url)
        self.history.append(tx)
        return tx