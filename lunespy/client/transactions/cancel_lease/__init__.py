from lunespy.client.transactions import BaseTransaction
from lunespy.client.account import Wallet


class CancelLease(BaseTransaction):
    def __init__(self, sender: Account, lease_tx_id: str = None,
                 timestamp: int = None, fee: int = None) -> None:
        from lunespy.utils import drop_none

        self.cancel_data = drop_none({
            "timestamp": timestamp,
            "lease_tx_id": lease_tx_id,
            "fee": fee
        })
        super().__init__('Create Lease', self.cancel_data)
        self.sender: Account = sender
        self.history: list = []


    @property
    def ready(self) -> bool:
        from lunespy.client.transactions.cancel_lease.validators import validate_cancel

        return validate_cancel(self.sender, self.cancel_data)


    @property
    def transaction(self) -> dict:
        from lunespy.client.transactions.cancel_lease.validators import mount_cancel

        return super().transaction(
            mount_tx=mount_cancel,
            sender=self.sender,
            cancel_data=self.cancel_data)

    def send(self, node_url: str = None) -> dict:
        from lunespy.client.transactions.cancel_lease.validators import send_cancel

        tx = super().send(send_cancel, node_url)
        self.history.append(tx)
        return tx