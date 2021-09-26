from lunespy.client.transactions.low_level import save_transaction
from lunespy.client.transactions.low_level import log_transaction
from lunespy.utils.settings import bcolors
from abc import ABCMeta, abstractmethod


class BaseTransaction(metaclass=ABCMeta):
    def __init__(self, tx_type: str, tx_data: dict):
        self.tx_type: str = tx_type
        self.tx_data: str = tx_data

    @abstractmethod
    def ready(self) -> bool:
        raise NotImplementedError


    def transaction(self, mount_tx, **extra) -> dict:
        if self.ready:
            tx = {'ready': True}
            tx.update( mount_tx( **extra ) )
            return tx
        else:
            print(bcolors.FAIL + f'{self.tx_type} Transactions bad formed', bcolors.ENDC)
            return {'ready': False}


    def send(self, send_tx, node_url_address: str) -> dict:
        mounted_tx = self.transaction
        if mounted_tx['ready']:
            tx_response = send_tx(mounted_tx, node_url_address=node_url_address)
            if tx_response['send']:
                self.show(**tx_response)
                return tx_response
            else:
                print(bcolors.FAIL + f"Your {self.tx_type} dont sended because:\n└──{tx_response['response']}" + bcolors.ENDC)
                return tx_response
        else:
            print(bcolors.FAIL + f'{self.tx_type} Transaction dont send', bcolors.ENDC)
            return mounted_tx
        

    def show(self, **data: dict) -> None:
        log_transaction(data)
        save_transaction(data)
