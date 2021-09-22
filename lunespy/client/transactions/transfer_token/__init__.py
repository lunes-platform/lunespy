from lunespy.client.transactions.transfer_token.validators import validate_transfer
from lunespy.client.transactions.transfer_token.validators import mount_transfer
from lunespy.client.transactions.transfer_token.validators import send_transfer
from lunespy.client.transactions import BaseTransaction
from lunespy.client.wallet import Account
from lunespy.utils.settings import bcolors


class TransferToken(BaseTransaction):
    """
    data_transfer: dict
        @params fee_asset: int
        @params timestamp: int
        @params asset_id: str
        @params tx_fee: int
        @params amount: int
    """
    def __init__(self, sender: Account, receiver: Account, **data_transfer) -> None:
        self.sender: Account = sender
        self.receiver: Account = receiver
        self.data_transfer: dict = data_transfer
        self.history: list = []

    @property
    def ready(self) -> bool:
        return validate_transfer(
            self.sender,
            self.data_transfer
        )

    @property
    def transaction(self) -> dict:
        if self.ready:
            mount_tx = {'ready': True}
            mount_tx.update(mount_transfer(
                self.sender,
                self.receiver,
                self.data_transfer
                )
            )
            return mount_tx
        else:
            print(bcolors.FAIL + 'Transfer Transactions bad formed', bcolors.ENDC)
            return {'ready': False}
    @property
    def send(self) -> dict:
        mounted_tx = self.transaction
        if mounted_tx['ready']:
            tx_history = send_transfer(mounted_tx)
            self.history.append(tx_history)
            return tx_history
        else:
            print(bcolors.FAIL + 'Transfer Transactions dont send', bcolors.ENDC)
            return mounted_tx
