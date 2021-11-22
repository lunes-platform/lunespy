from lunespy.client.transactions import BaseTransaction
from lunespy.client.transactions.reissue.validators import validate_reissue
from lunespy.client.transactions.reissue.validators import mount_reissue
from lunespy.client.transactions.reissue.validators import send_reissue
from lunespy.utils import bcolors
from lunespy.client.wallet import Account


class ReissueToken(BaseTransaction):
    """
    reissue_data: dict
        reissuable: bool
        fee: int
        asset_id: str
        quantity: int
    """
    def __init__(self, sender: Account, **reissue_data: dict) -> None:
        super().__init__('Reissue Token', reissue_data)
        self.sender = sender
        self.reissue_data = reissue_data
        self.reissue_data['token_type'] = 'Token'
        self.history = []

    @property
    def ready(self) -> bool:
        return validate_reissue(self.sender, self.reissue_data)
    
    @property
    def transaction(self) -> dict:
        return super().transaction(
            mount_tx=mount_reissue,
            sender=self.sender,
            reissue_data=self.reissue_data)

    def send(self, node_url: str = None) -> dict:
        tx = super().send(send_reissue, node_url)
        self.history.append(tx)
        return tx


class ReissueAsset(ReissueToken):
    def __init__(self, sender: Account, **reissue_data: dict) -> None:
        reissue_data['token_type'] = 'Asset'
        BaseTransaction.__init__(self, tx_type='Reissue Asset', tx_data=reissue_data)
        ReissueToken.__init__(self, sender=sender, **reissue_data)


class ReissueNFT(ReissueToken):
    def __init__(self, sender: Account, **reissue_data: dict) -> None:
        reissue_data['token_type'] = 'NFT'
        reissue_data['decimals'] = 0
        BaseTransaction.__init__(self, tx_type='Reissue NFT', tx_data=reissue_data)
        ReissueToken.__init__(self, sender=sender, **reissue_data)
