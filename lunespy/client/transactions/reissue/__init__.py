from lunespy.client.transactions import BaseTransaction
from lunespy.client.transactions.reissue.validators import validate_reissue
from lunespy.client.transactions.reissue.validators import mount_reissue
from lunespy.client.transactions.reissue.validators import send_reissue
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account


class ReissueToken(BaseTransaction):
    """
    data_reissue: dict
        @params asset_id: str, 
        @params quantity: int, 
        @params reissuable: bool, 
        @params tx_fee: int
    """
    def __init__(self, creator: Account, **reissue_data: dict) -> None:
        self.creator = creator
        self.reissue_data = reissue_data
        self.reissue_data['token_type'] = 'Token'
        self.history = []

    @property
    def ready(self) -> bool:
        return validate_reissue(self.creator, self.reissue_data)
    

    @property
    def transaction(self) -> dict:
        if self.ready:
            mount_tx = {'ready': True}
            mount_tx.update(mount_reissue(self.creator, self.reissue_data))
            return mount_tx
        else:
            print(bcolors.FAIL + 'Reissue Transaction bad formed', bcolors.ENDC)
            mount_tx = {'ready': False}
            return mount_tx

    def send(self, http_node: str='') -> dict:
        mounted_tx = self.transaction
        if mounted_tx['ready']:
            node = http_node if http_node else NODE_URL
            tx_history = send_reissue(mounted_tx, node=node)
            self.history.append(tx_history)
            if tx_history['send']:
                self.successful(tx_history['response'], self.reissue_data['token_type'])
            else:
                print(bcolors.FAIL + f'Your {self.reissue_data["token_type"]} dont reissued because:\n', bcolors.ENDC)
                print(tx_history['response'])   
            return tx_history
        else:
            print(bcolors.FAIL + 'Reissue Transaction dont send', bcolors.ENDC)
            return mounted_tx

    def successful(self, asset_reissued: dict, token_type: str) -> None:
        reissuable = asset_reissued['reissuable']
        quantity = asset_reissued['quantity']
        transaction_id = asset_reissued['id']
        asset_id = asset_reissued['assetId']
        creator = asset_reissued['sender']
        asset_reissued.update({'token_type': token_type})

        print(f"\
            \ntype\n {bcolors.OKGREEN + '└──' +  token_type + bcolors.ENDC}\
            \nasset_id\n {bcolors.OKBLUE + '└──' + asset_id + bcolors.ENDC}\
            \nquantity\n {bcolors.OKBLUE + '└──' + str(quantity) + bcolors.ENDC}\
            \ncreator\n {bcolors.OKBLUE + '└──' + creator + bcolors.ENDC}\
            \nreissuable\n {bcolors.OKBLUE + '└──' + str(reissuable) + bcolors.ENDC}\
            \ntransaction_id\n {bcolors.OKBLUE + '└──' + transaction_id + bcolors.ENDC}\
        ")
        
        import json
        with open(f'./reissue-token.json', 'w') as file:
            file.write(json.dumps(asset_reissued))

        print(f"\n{bcolors.OKGREEN}Your {token_type} has been reissued and saved in `./reissuetoken.json`{bcolors.ENDC}")


class ReissueAsset(ReissueToken):
    def __init__(self,
        creator: Account,
        **reissue_data: dict
        ) -> None:
        reissue_data['token_type'] = reissue_data['token_type'] if reissue_data.get('token_type', False) else 'Asset'
        super().__init__(creator, **reissue_data)


class ReissueNFT(ReissueAsset):
    def __init__(self,
        creator: Account,
        **reissue_data: dict
        ) -> None:
        reissue_data['token_type'] = 'NFT'
        reissue_data['decimals'] = 0
        super().__init__(creator, **reissue_data)