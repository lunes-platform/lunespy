from lunespy.client.transactions import BaseTransaction
from lunespy.client.account import Wallet


class ReissueToken(BaseTransaction):
    def __init__(self, sender: Account, asset_id: str = None, reissuable: bool = None,
                 quantity: int = None, timestamp: int = None, fee: int = None) -> None:
        from lunespy.utils import drop_none

        self.reissue_data = drop_none({
            "asset_id": asset_id,
            "reissuable": reissuable,
            "quantity": quantity,
            "timestamp": timestamp,
            "fee": fee
        })
        super().__init__('Reissue Token', self.reissue_data)
        self.sender = sender
        self.history = []


    @property
    def ready(self) -> bool:
        from lunespy.client.transactions.reissue.validators import validate_reissue

        return validate_reissue(self.sender, self.reissue_data)


    @property
    def transaction(self) -> dict:
        from lunespy.client.transactions.reissue.validators import mount_reissue

        return super().transaction(
            mount_tx=mount_reissue,
            sender=self.sender,
            reissue_data=self.reissue_data)



    def send(self, node_url: str = None) -> dict:
        from lunespy.client.transactions.reissue.validators import send_reissue

        tx = super().send(send_reissue, node_url)
        self.history.append(tx)
        return tx


class ReissueAsset(ReissueToken):
    def __init__(self, sender: Account, asset_id: str = None, reissuable: bool = None,
                 quantity: int = None, timestamp: int = None, fee: int = None) -> None:
        from lunespy.utils import drop_none

        reissue_data = drop_none({
            "asset_id": asset_id,
            "reissuable": reissuable,
            "quantity": quantity,
            "timestamp": timestamp,
            "fee": fee
        })
        BaseTransaction.__init__(self, tx_type='Reissue Asset', tx_data=reissue_data)
        ReissueToken.__init__(self, sender=sender, **reissue_data)


class ReissueNFT(ReissueToken):
    def __init__(self, sender: Account, asset_id: str = None, reissuable: bool = None,
                 quantity: int = None, timestamp: int = None, fee: int = None) -> None:
        from lunespy.utils import drop_none

        reissue_data = drop_none({
            "asset_id": asset_id,
            "reissuable": reissuable,
            "quantity": quantity,
            "timestamp": timestamp,
            "fee": fee
        })
        BaseTransaction.__init__(self, tx_type='Reissue NFT', tx_data=reissue_data)
        ReissueToken.__init__(self, sender=sender, **reissue_data)
