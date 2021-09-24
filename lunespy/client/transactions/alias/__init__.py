from lunespy.client.transactions import BaseTransaction
from lunespy.client.transactions.alias.validators import validate_alias
from lunespy.client.transactions.alias.validators import mount_alias
from lunespy.client.transactions.alias.validators import send_alias
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account

class CreateAlias(BaseTransaction):
    def __init__(self, creator: Account, **alias_data: dict) -> None:
        self.creator: Account = creator
        self.alias_data: dict = alias_data
        self.history: list = []

    @property
    def ready(self) -> bool:
        return validate_alias(
            self.creator,
            self.alias_data
        )
    
    @property
    def transaction(self) -> dict:
        if self.ready:
            mount_tx = {'ready': True}
            mount_tx.update(mount_alias(self.creator, self.alias_data))
            return mount_tx
        else:
            print(bcolors.FAIL + 'Alias Transaction bad formed', bcolors.ENDC)
            mount_tx = {'ready': False}
            return mount_tx


    def send(self, http_node: str='') -> dict:
        mounted_tx = self.transaction
        if mounted_tx['ready']:
            node = http_node if http_node else NODE_URL
            tx_history = send_alias(mounted_tx, node=node)
            self.history.append(tx_history)
            if tx_history['send']:
                self.successful(tx_history['response'])
            else:
                print(bcolors.FAIL + f"Your Alias dont created because:\n└──{tx_history['response']}" +  bcolors.ENDC)
                return tx_history
        else:
            print(bcolors.FAIL + 'Alias Transaction dont send', bcolors.ENDC)
            return mounted_tx

    def successful(self, created_alias: dict, token_type: str) -> None:
        transaction_id = created_alias['id']
        asset_id = created_alias['assetId']
        creator = created_alias['sender']
        
        print(f"\
            \nname\n {bcolors.OKGREEN + '└──' +  name + bcolors.ENDC}\
            \ntype\n {bcolors.OKGREEN + '└──' +  token_type + bcolors.ENDC}\
            \ncreator\n {bcolors.OKBLUE + '└──' + creator + bcolors.ENDC}\
            \ntransaction_id\n {bcolors.OKBLUE + '└──' + transaction_id + bcolors.ENDC}\
        ")
        
        import json
        with open(f'./alias-{alias}.json', 'w') as file:
            file.write(json.dumps(created_alias))

        print(f"\n{bcolors.OKGREEN}Your Alias has been created and saved in `./alias-{alias}.json`{bcolors.ENDC}")


    