from lunespy.client.transactions import BaseTransaction
from lunespy.client.wallet import Account
from lunespy.utils import drop_none


class CreateAlias(BaseTransaction):
    def __init__(self, sender: Account, fee: int = None,
                 timestamp: int = None, alias: str = None) -> None:
        alias_data: dict = drop_none({
            'timestamp': timestamp,
            'alias': alias,
            'fee': fee
        })
        super().__init__('Alias', alias_data)
        self.sender: Account = sender
        self.alias_data: dict = alias_data
        self.history: list = []

   
    @property
    def ready(self) -> bool:
        from lunespy.client.transactions.alias.validators import validate_alias

        return validate_alias(self.sender, self.alias_data)
    
    @property
    def transaction(self) -> dict:
        from lunespy.client.transactions.alias.validators import mount_alias

        return super().transaction(
            mount_tx=mount_alias,
            sender=self.sender,
            alias_data=self.alias_data)

    def send(self, node_url: str = None) -> dict:
        from lunespy.client.transactions.alias.validators import send_alias

        tx = super().send(send_alias, node_url)
        self.history.append(tx)
        return tx