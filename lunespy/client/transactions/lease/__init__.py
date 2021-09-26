from lunespy.client.transactions.lease.validators import validate_lease
from lunespy.client.transactions.lease.validators import mount_lease
from lunespy.client.transactions.lease.validators import send_lease
from lunespy.client.transactions import BaseTransaction
from lunespy.client.wallet import Account
from lunespy.server import NODE_URL

class CreateLease(BaseTransaction):
    """
    lease_data: dict
        validator_address: str
        lease_fee: int
        timestamp: int
        amount: int
    """
    def __init__(self, staker: Account, validator_address: str, **lease_data: dict) -> None:
        super().__init__('Create Lease', lease_data)
        self.staker: Account = staker
        self.validator_address: str = validator_address
        self.lease_data: dict = lease_data
        self.history: list = []

    
    @property
    def ready(self) -> bool:
        return validate_lease(self.staker, self.lease_data)


    @property
    def transaction(self) -> dict:
        return super().transaction(
            mount_tx=mount_lease,
            staker=self.staker,
            validator_address=self.validator_address,
            lease_data=self.lease_data)

    def send(self, node_url_address: str=NODE_URL) -> dict:
        tx = super().send(send_lease, node_url_address)
        self.history.append(tx)
        return tx