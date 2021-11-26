from lunespy.client.transactions import BaseTransaction
from lunespy.client.wallet import Account

class TransferToken(BaseTransaction):
    """
    transfer_data: dict
        fee: int
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
        from lunespy.client.transactions.transfer.validators import validate_transfer

        return validate_transfer(self.sender, self.receiver, self.transfer_data)


    @property
    def transaction(self) -> dict:
        from lunespy.client.transactions.transfer.validators import mount_transfer

        return super().transaction(
            mount_tx=mount_transfer,
            sender=self.sender,
            receiver=self.receiver,
            transfer_data=self.transfer_data)


    def send(self, node_url: str = None) -> dict:
        from lunespy.client.transactions.transfer.validators import send_transfer

        tx = super().send(send_transfer, node_url)
        self.history.append(tx)
        return tx
