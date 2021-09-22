from lunespy.client.transactions.burn.validators import validate_burn
from lunespy.client.transactions.burn.validators import mount_burn
from lunespy.client.transactions.burn.validators import send_burn
from lunespy.client.transactions import BaseTransaction
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account


class BurnToken(BaseTransaction):
    """
    burn_data: dict
        @params asset_id: str, 
        @params quantity: int, 
        @params reissuable: bool, 
        @params tx_fee: int
    """
    def __init__(self, burner: Account, **burn_data: dict) -> None:
        self.burner = burner
        self.burn_data = burn_data
        self.burn_data['token_type'] = 'Token'
        self.history = []

    @property
    def ready(self) -> bool:
        return validate_burn(self.burner, self.burn_data)
    

    @property
    def transaction(self) -> dict:
        if self.ready:
            mount_tx = {'ready': True}
            mount_tx.update(mount_burn(self.burner, self.burn_data))
            return mount_tx
        else:
            print(bcolors.FAIL + 'Burn Transaction bad formed', bcolors.ENDC)
            mount_tx = {'ready': False}
            return mount_tx

    def send(self, http_node: str='') -> dict:
        mounted_tx = self.transaction
        if mounted_tx['ready']:
            node = http_node if http_node else NODE_URL
            tx_history = send_burn(mounted_tx, node=node)
            self.history.append(tx_history)
            if tx_history['send']:
                self.successful(tx_history['response'], self.burn_data['token_type'])
            else:
                print(bcolors.FAIL + f'Your {self.burn_data["token_type"]} dont burned because:\n', bcolors.ENDC)
                print(tx_history['response'])   
            return tx_history
        else:
            print(bcolors.FAIL + 'burn Transaction dont send', bcolors.ENDC)
            return mounted_tx

    def successful(self, asset_burned: dict, token_type: str) -> None:
        amount = asset_burned['amount']
        transaction_id = asset_burned['id']
        asset_id = asset_burned['assetId']
        burner = asset_burned['sender']
        asset_burned.update({'token_type': token_type})

        print(f"\
            \ntype\n {bcolors.OKGREEN + '└──' +  token_type + bcolors.ENDC}\
            \nasset_id\n {bcolors.OKGREEN + '└──' + asset_id + bcolors.ENDC}\
            \namount burned\n {bcolors.FAIL + '└──' + str(amount) + bcolors.ENDC}\
            \nburner\n {bcolors.FAIL + '└──' + burner + bcolors.ENDC}\
            \ntransaction_id\n {bcolors.OKBLUE + '└──' + transaction_id + bcolors.ENDC}\
        ")
        
        import json
        with open(f'./burn-{token_type}.json', 'w') as file:
            file.write(json.dumps(asset_burned))

        print(f"\n{bcolors.OKGREEN}Your {token_type} has been burnd and saved in `./burn-{token_type}.json`{bcolors.ENDC}")


class BurnAsset(BurnToken):
    def __init__(self,
        burner: Account,
        **burn_data: dict
        ) -> None:
        burn_data['token_type'] = burn_data['token_type'] if burn_data.get('token_type', False) else 'Asset'
        super().__init__(burner, **burn_data)


class BurnNFT(BurnAsset):
    def __init__(self,
        burner: Account,
        **burn_data: dict
        ) -> None:
        burn_data['token_type'] = 'NFT'
        burn_data['decimals'] = 0
        super().__init__(burner, **burn_data)