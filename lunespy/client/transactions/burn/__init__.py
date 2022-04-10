from lunespy.client.transactions import BaseTransaction
from lunespy.client.account import Wallet
from lunespy.utils import drop_none


class BurnToken(BaseTransaction):
    def __init__(self, sender: Account, asset_id: str = None, quantity: int = None,
                 timestamp: int = None, fee: int = None) -> None:
        from lunespy.utils import drop_none
        self.burn_data: dict = drop_none({
            "timestamp": timestamp,
            "asset_id": asset_id,
            "quantity": quantity,
            "fee": fee
        })
        super().__init__('Burn Token', self.burn_data)
        self.sender = sender
        self.history = []

    @property
    def ready(self) -> bool:
        from lunespy.client.transactions.burn.validators import validate_burn

        return validate_burn(self.sender, self.burn_data)

    @property
    def transaction(self) -> dict:
        from lunespy.client.transactions.burn.validators import mount_burn

        return super().transaction(
            mount_tx=mount_burn,
            sender=self.sender,
            burn_data=self.burn_data)

    def send(self, node_url: str = None) -> dict:
        from lunespy.client.transactions.burn.validators import send_burn

        tx = super().send(send_burn, node_url)
        self.history.append(tx)
        return tx


class BurnAsset(BurnToken):
    def __init__(self, sender: Account, timestamp: int = None, asset_id: str = None,
                 quantity: int = None, fee: int = None) -> None:
        from lunespy.utils import drop_none
        burn_data: dict = drop_none({
            "timestamp": timestamp,
            "asset_id": asset_id,
            "quantity": quantity,
            "fee": fee
        })
        BaseTransaction.__init__(self, tx_type='Burn Asset', tx_data=burn_data)
        BurnToken.__init__(self, sender=sender, **burn_data)


class BurnNFT(BurnAsset):
    def __init__(self, sender: Account, timestamp: int = None, asset_id: str = None,
                 quantity: int = None, fee: int = None) -> None:
        from lunespy.utils import drop_none
        burn_data: dict = drop_none({
            "timestamp": timestamp,
            "asset_id": asset_id,
            "quantity": quantity,
            "fee": fee
        })
        BaseTransaction.__init__(self, tx_type='Burn NFT', tx_data=burn_data)
        BurnToken.__init__(self, sender=sender, **burn_data)
