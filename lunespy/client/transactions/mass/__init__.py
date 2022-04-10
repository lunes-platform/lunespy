from lunespy.client.transactions import BaseTransaction
from lunespy.client.account import Wallet


class MassTransferToken(BaseTransaction):
    """
    receivers_list: list
        tx: dict
            receiver: str
            amount: float

    transfer_data: dict
        timestamp: int
        asset_id: str
    """
    def __init__(self, sender: Account, receivers_list: list, **mass_transfer_data: dict) -> None:
        super().__init__("Mass", {'receivers_list': receivers_list, 'mass_transfer_data': mass_transfer_data})
        self.sender: Account = sender
        self.receivers_list: list[dict] = receivers_list
        self.mass_transfer_data: dict = mass_transfer_data
        self.history: list = []


    @property
    def ready(self) -> bool:
        from lunespy.client.transactions.mass.validators import validate_mass_transfer

        return validate_mass_transfer(self.sender, self.receivers_list)


    @property
    def transaction(self) -> dict:
        from lunespy.client.transactions.mass.validators import mount_mass_transfer

        return super().transaction(
            mount_tx=mount_mass_transfer,
            sender=self.sender,
            receivers_list=self.receivers_list,
            mass_transfer_data=self.mass_transfer_data)


    def send(self, node_url: str = None) -> dict:
        from lunespy.client.transactions.mass.validators import send_mass_transfer

        tx = super().send(send_mass_transfer, node_url)
        self.history.append(tx)
        return tx
