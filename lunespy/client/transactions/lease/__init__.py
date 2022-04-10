from lunespy.client.transactions import BaseTransaction
from lunespy.client.account import Wallet


class CreateLease(BaseTransaction):
    def __init__(self, sender: Account, node_address: str, amount: float = None,
                 timestamp: int = None, fee: int = None) -> None:
        from lunespy.utils import drop_none

        self.lease_data = drop_none({
            "node_address": node_address,
            "amount": amount,
            "timestamp": timestamp,
            "fee": fee
        })
        super().__init__('Create Lease', self.lease_data)
        self.sender: Account = sender
        self.history: list = []


    @property
    def ready(self) -> bool:
        from lunespy.client.transactions.lease.validators import validate_lease

        return validate_lease(self.sender, self.lease_data)


    @property
    def transaction(self) -> dict:
        from lunespy.client.transactions.lease.validators import mount_lease

        return super().transaction(
            mount_tx=mount_lease,
            sender=self.sender,
            lease_data=self.lease_data)

    def send(self, node_url: str = None) -> dict:
        from lunespy.client.transactions.lease.validators import send_lease

        tx = super().send(send_lease, node_url)
        self.history.append(tx)
        return tx
