from lunespy.client.transactions.cancel.validators import validate_cancel
from lunespy.client.transactions.cancel.validators import mount_cancel
from lunespy.client.transactions.cancel.validators import send_cancel
from lunespy.client.transactions import BaseTransaction
from lunespy.client.wallet import Account
from lunespy.server import NODE_URL

class CancelLease(BaseTransaction):
    """
    cancel_data: dict
        lease_tx_id: str
        cancel_fee: int
        timestamp: int
    """
    def __init__(self, staker: Account, **cancel_data: dict) -> None:
        super().__init__('Create Lease', cancel_data)
        self.staker: Account = staker
        self.cancel_data: dict = cancel_data
        self.history: list = []

    
    @property
    def ready(self) -> bool:
        return validate_cancel(self.staker, self.cancel_data)


    @property
    def transaction(self) -> dict:
        return super().transaction(
            mount_tx=mount_cancel,
            staker=self.staker,
            cancel_data=self.cancel_data)

    def send(self, node_url_address: str=NODE_URL) -> dict:
        tx = super().send(send_cancel, node_url_address)
        self.history.append(tx)
        return tx