from lunespy.client.transactions.issue.validators import validate_issue
from lunespy.client.transactions.issue.validators import send_issue
from lunespy.client.transactions.issue.validators import mount_issue
from lunespy.client.transactions import BaseTransaction
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account
from lunespy.server import NODE_URL

class Token(BaseTransaction):
    """
    data_issue: dict
        @params description: str
        @params reissuable: bool
        @params quantity: int
        @params decimals: int
        @params tx_fee: int
        @params name: str
    """
    def __init__(self, creator: Account, **data_issue: dict) -> None:
        self.creator = creator
        self.data_issue = data_issue
        self.history = []

    @property
    def ready(self) -> bool:
        return validate_issue(
            self.creator,
            self.data_issue
        )

    @property
    def transaction(self) -> dict:
        if self.ready:
            mount_tx = {'ready': True}
            mount_tx.update(mount_issue(self.creator, self.data_issue))
            return mount_tx
        else:
            print(bcolors.FAIL + 'Issue Transaction bad formed', bcolors.ENDC)
            mount_tx = {'ready': False}
            return mount_tx


    def send(self, http_node: str='') -> dict:
        mounted_tx = self.transaction
        if mounted_tx['ready']:
            node = http_node if http_node else NODE_URL
            tx_history = send_issue(mounted_tx, node=node)
            self.history.append(tx_history)
            if tx_history['send']:
                self.successful(tx_history['response'], self.data_issue['token_type'])
            else:
                print(bcolors.FAIL + f'Your {self.data_issue["token_type"]} dont issued because:\n', bcolors.ENDC)
                print(tx_history['response'])   
            return tx_history
        else:
            print(bcolors.FAIL + 'Issue Transaction dont send', bcolors.ENDC)
            return mounted_tx

    def successful(self, asset_issued: dict, token_type: str) -> None:
        description = asset_issued['description']
        reissuable = asset_issued['reissuable']
        quantity = asset_issued['quantity']
        decimals = asset_issued['decimals']
        transaction_id = asset_issued['id']
        asset_id = asset_issued['assetId']
        creator = asset_issued['sender']
        name = asset_issued['name']
        asset_issued.update({'token_type': token_type})

        print(f"\
            \nname\n {bcolors.OKGREEN + '└──' +  name + bcolors.ENDC}\
            \ntype\n {bcolors.OKGREEN + '└──' +  token_type + bcolors.ENDC}\
            \nasset_id\n {bcolors.OKBLUE + '└──' + asset_id + bcolors.ENDC}\
            \nquantity\n {bcolors.OKBLUE + '└──' + str(quantity) + bcolors.ENDC}\
            \ncreator\n {bcolors.OKBLUE + '└──' + creator + bcolors.ENDC}\
            \ndescription\n {bcolors.OKBLUE + '└──' + description + bcolors.ENDC}\
            \nreissuable\n {bcolors.OKBLUE + '└──' + str(reissuable) + bcolors.ENDC}\
            \ndecimals\n {bcolors.OKBLUE + '└──' + str(decimals) + bcolors.ENDC}\
            \ntransaction_id\n {bcolors.OKBLUE + '└──' + transaction_id + bcolors.ENDC}\
        ")
        
        import json
        with open(f'./token-{name}.json', 'w') as file:
            file.write(json.dumps(asset_issued))

        print(f"\n{bcolors.OKGREEN}Your {token_type} has been issued and saved in `./asset_info.json`{bcolors.ENDC}")


class Asset(Token):
    def __init__(self,
        creator: Account,
        **data_issue: dict
        ) -> None:
        data_issue['token_type'] = data_issue['token_type'] if data_issue.get('token_type', False) else 'Asset'
        super().__init__(creator, **data_issue)


class NFT(Asset):
    def __init__(self,
        creator: Account,
        **data_issue: dict
        ) -> None:
        data_issue['token_type'] = 'NFT'
        data_issue['decimals'] = 0
        super().__init__(creator, **data_issue)