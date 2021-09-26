from lunespy.client.transactions.transfer.validators import validate_transfer
from lunespy.client.transactions.transfer.validators import mount_transfer
from lunespy.client.transactions.transfer.validators import send_transfer
from lunespy.client.transactions import BaseTransaction
from lunespy.client.wallet import Account
from lunespy.utils.settings import bcolors
from lunespy.server import NODE_URL

class TransferToken(BaseTransaction):
    """
    transfer_data: dict
        transfer_fee: int
        timestamp: int
        asset_fee: int
        asset_id: str
        amount: int
    """
    def __init__(self, sender: Account, receiver: Account, **transfer_data: dict) -> None:
        super().__init__('Transfer', transfer_data)
        self.sender: Account = sender
        self.receiver: Account = receiver
        self.transfer_data: dict = transfer_data
        self.history: list = []

    @property
    def ready(self) -> bool:
        return validate_transfer(self.sender,self.transfer_data)

    @property
    def transaction(self) -> dict:
        return super().transaction(
            mount_tx=mount_transfer,
            sender=self.sender,
            receiver=self.receiver,
            transfer_data=self.transfer_data)

    def send(self, node_url_address: str=NODE_URL) -> dict:
        tx = super().send(send_transfer, node_url_address)
        self.history.append(tx)
        return tx