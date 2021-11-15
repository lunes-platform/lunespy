from lunespy.client.transactions import BaseTransaction
from lunespy.client.transactions.alias.validators import validate_alias
from lunespy.client.transactions.alias.validators import mount_alias
from lunespy.client.transactions.alias.validators import send_alias
from lunespy.utils import bcolors
from lunespy.client.wallet import Account

class CreateAlias(BaseTransaction):
    """
    alias_data: dict
        timestamp: int    
        alias_fee: int
        alias: str
    """
    def __init__(self, sender: Account, **alias_data: dict) -> None:
        super().__init__('Alias', alias_data)
        self.sender: Account = sender
        self.alias_data: dict = alias_data
        self.history: list = []

   
    @property
    def ready(self) -> bool:
        return validate_alias(self.sender, self.alias_data)
    
    @property
    def transaction(self) -> dict:
        return super().transaction(
            mount_tx=mount_alias,
            sender=self.sender,
            alias_data=self.alias_data)

    def send(self, node_url: str = None) -> dict:
        tx = super().send(send_alias, node_url)
        self.history.append(tx)
        return tx