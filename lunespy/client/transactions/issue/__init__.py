from lunespy.client.transactions.issue.validators import validate_issue
from lunespy.client.transactions.issue.validators import send_issue
from lunespy.client.transactions.issue.validators import mount_issue
from lunespy.client.transactions import BaseTransaction
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account


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

    @property
    def send(self) -> dict:
        mounted_tx = self.transaction
        if mounted_tx['ready']:
            tx_history = send_issue(mounted_tx)
            self.history.append(tx_history)
            self.successful(tx_history['response'])
            return tx_history
        else:
            print(bcolors.FAIL + 'Issue Transaction dont send', bcolors.ENDC)
            return mounted_tx

    def successful(self, asset_issued: dict) -> None:
        asset_id = asset_issued['assetId']
        name = asset_issued['name']
        quantity = asset_issued['quantity']
        creator = asset_issued['sender']
        description = asset_issued['description']
        reissuable = asset_issued['reissuable']
        decimals = asset_issued['decimals']
        transaction_id = asset_issued['id']

        print(f"\
            \nname\n {bcolors.OKGREEN + '└──' +  name + bcolors.ENDC}\
            \nasset_id\n {bcolors.OKBLUE + '└──' + asset_id + bcolors.ENDC}\
            \nquantity\n {bcolors.OKBLUE + '└──' + str(quantity) + bcolors.ENDC}\
            \ncreator\n {bcolors.OKBLUE + '└──' + creator + bcolors.ENDC}\
            \ndescription\n {bcolors.OKBLUE + '└──' + description + bcolors.ENDC}\
            \nreissuable\n {bcolors.OKBLUE + '└──' + str(reissuable) + bcolors.ENDC}\
            \ndecimals\n {bcolors.OKBLUE + '└──' + str(decimals) + bcolors.ENDC}\
            \ntransaction_id\n {bcolors.OKBLUE + '└──' + transaction_id + bcolors.ENDC}\
        ")

        print(f"{bcolors.OKGREEN}Your Asset has been saved in `./asset_info.json`{bcolors.ENDC}")


class Asset(Token):
    def __init__(self,
        creator: Account,
        **data_nft: dict
        ) -> None:
        super().__init__(creator, **data_nft)


class NFT(Asset):
    def __init__(self,
        creator: Account,
        **data_nft: dict
        ) -> None:
        data_nft['decimals'] = 0
        super().__init__(creator, **data_nft)