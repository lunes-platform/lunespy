from lunespy.client.transactions.lunex.validators import validate_lunex
from lunespy.client.transactions.lunex.validators import mount_lunex
from lunespy.client.transactions.lunex.validators import send_lunex
from lunespy.client.transactions import BaseTransaction
from lunespy.client.wallet import Account


class Lunex(BaseTransaction):
    def __init__(self, sender: Account, **lunex_data: dict):
        super().__init__("Lunex Orders", lunex_data)
        self.sender: Account = sender
        self.lunex_data: dict = lunex_data
    
    @property
    def ready(self) -> bool:
        return validate_lunex(self.sender, self.lunex_data)

    @property
    def transaction(self) -> dict:
        return super().transaction(
            mount_tx=mount_lunex,
            sender=self.sender,
            lunex_data=self.lunex_data)

    def send(self, node_url: str = None) -> dict:
        tx = super().send(send_lunex, node_url)
        self.history.append(tx)
        return tx

