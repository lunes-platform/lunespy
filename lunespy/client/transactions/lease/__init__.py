from lunespy.client.transactions import BaseTransaction
from lunespy.client.wallet import Account


class CreateLease(BaseTransaction):
    """
    lease_data: dict
        validator_address: str
        fee: int
        timestamp: int
        amount: int
    """
    def __init__(self, sender: Account, validator_address: str, **lease_data: dict) -> None:
        super().__init__('Create Lease', lease_data)
        self.sender: Account = sender
        self.validator_address: str = validator_address
        self.lease_data: dict = lease_data
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
            validator_address=self.validator_address,
            lease_data=self.lease_data)

    def send(self, node_url: str = None) -> dict:
        from lunespy.client.transactions.lease.validators import send_lease

        tx = super().send(send_lease, node_url)
        self.history.append(tx)
        return tx
