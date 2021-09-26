from lunespy.client.transactions import BaseTransaction
from lunespy.client.transactions.reissue.validators import validate_reissue
from lunespy.client.transactions.reissue.validators import mount_reissue
from lunespy.client.transactions.reissue.validators import send_reissue
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account
from lunespy.server import NODE_URL

class ReissueToken(BaseTransaction):
    """
    data_reissue: dict
        asset_id: str
        quantity: int
        reissue_fee: int
    """
    def __init__(self, creator: Account, **reissue_data: dict) -> None:
        super().__init__('Reissue Token', reissue_data)
        self.creator = creator
        self.reissue_data = reissue_data
        self.reissue_data['token_type'] = 'Token'
        self.history = []

    @property
    def ready(self) -> bool:
        return validate_reissue(self.creator, self.reissue_data)
    
    @property
    def transaction(self) -> dict:
        return super().transaction(
            mount_tx=mount_reissue,
            creator=self.creator,
            reissue_data=self.reissue_data)

    def send(self, node_url_address: str = NODE_URL) -> dict:
        tx = super().send(send_reissue, node_url_address)
        self.history.append(tx)
        return tx


class ReissueAsset(ReissueToken):
    def __init__(self, creator: Account, **reissue_data: dict) -> None:
        reissue_data['token_type'] = 'Asset'
        BaseTransaction.__init__(self, tx_type='Reissue Asset', tx_data=reissue_data)
        ReissueToken.__init__(self, creator=creator, **reissue_data)


class ReissueNFT(ReissueToken):
    def __init__(self, creator: Account, **reissue_data: dict) -> None:
        reissue_data['token_type'] = 'NFT'
        reissue_data['decimals'] = 0
        BaseTransaction.__init__(self, tx_type='Reissue NFT', tx_data=reissue_data)
        ReissueToken.__init__(self, creator=creator, **reissue_data)
