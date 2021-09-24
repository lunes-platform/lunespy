from lunespy.client.transactions.leasing.validators import validate_leasing
from lunespy.client.transactions.leasing.validators import mount_leasing
from lunespy.client.transactions.leasing.validators import send_leasing
from lunespy.client.transactions import BaseTransaction
from lunespy.client.wallet import Account
from lunespy.utils.settings import bcolors
from lunespy.server import NODE_URL

class CreateLeasing(BaseTransaction):
    """
    leasing_data: dict
        @params fee_asset: int
        @params timestamp: int
        @params asset_id: str
        @params tx_fee: int
        @params amount: int
    """
    def __init__(self, staker: Account, validator_address: str, **leasing_data) -> None:
        self.staker: Account = staker
        self.validator_address: str = validator_address
        self.leasing_data: dict = leasing_data
        self.history: list = []

    @property
    def ready(self) -> bool:
        return validate_leasing(
            self.staker,
            self.leasing_data
        )

    @property
    def transaction(self) -> dict:
        if self.ready:
            mount_tx = {'ready': True}
            mount_tx.update(mount_leasing(
                self.staker,
                self.validator_address,
                self.leasing_data
                )
            )
            return mount_tx
        else:
            print(bcolors.FAIL + 'Leasing Transactions bad formed', bcolors.ENDC)
            return {'ready': False}


    def send(self, http_node: str='') -> dict:
        mounted_tx = self.transaction
        if mounted_tx['ready']:
            node = http_node if http_node else NODE_URL
            tx_history = send_leasing(mounted_tx, node=node)
            self.history.append(tx_history)
            if tx_history['send']:
                self.successful(tx_history['response'])
                return tx_history
            else:
                print(bcolors.FAIL + f"Your leasing dont created because:\n└──{tx_history['response']}" +  bcolors.ENDC)
                return tx_history
        else:
            print(bcolors.FAIL + 'Leasing Transaction dont send', bcolors.ENDC)
            return mounted_tx

    def successful(self, created_leasing: dict) -> None:
        transaction_id = created_leasing['id']
        staker = self.staker.address
        validator_address = created_leasing['recipient']
        amount = created_leasing['amount']
        
        print(f"\
            \nstaker\n {bcolors.OKGREEN + '└──' +  staker + bcolors.ENDC}\
            \namount\n {bcolors.OKGREEN + '└──' +  str(amount) + bcolors.ENDC}\
            \nvalidator_address\n {bcolors.OKBLUE + '└──' + validator_address + bcolors.ENDC}\
            \ntransaction_id\n {bcolors.OKBLUE + '└──' + transaction_id + bcolors.ENDC}\
        ")
        

    