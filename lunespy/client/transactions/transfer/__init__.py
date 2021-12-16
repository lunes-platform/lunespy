from lunespy.client.transactions import BaseTransaction
from lunespy.client.wallet import Account
from lunespy.utils import drop_none

class TransferToken(BaseTransaction):
    def __init__(self, sender: Account, receiver: Account, asset_fee:int = None,
                 asset_id = None, amount:float = None, timestamp: int = None,
                 fee: int = None) -> None:
        self.transfer_data: dict = drop_none({
            'timestamp': timestamp,
            'asset_fee': asset_fee,
            'asset_id': asset_id,
            'amount': amount,
            'fee': fee
        })
        super().__init__('Transfer', self.transfer_data)
        self.sender: Account = sender
        self.receiver: Account = receiver
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
