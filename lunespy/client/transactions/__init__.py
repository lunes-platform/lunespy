from lunespy.utils.crypto.converters import sha256
from lunespy.utils import export_json, log_data
from lunespy.utils import bcolors
from abc import abstractmethod
from abc import ABCMeta


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
            tx.update(mount_tx( **extra ))
            return tx
        else:
            print(bcolors.FAIL + f'{self.tx_type} Transactions bad formed', bcolors.ENDC)
            return {'ready': False}


    def sign(self, sign_tx, private_key, **tx) -> dict:
        return sign_tx(private_key, **tx)


    def broadcast(self, send_tx, node_url: str, chain: str) -> dict:
        from lunespy.server.nodes import Node

        if node_url == None:
            if self.sender.chain == chain:
                node_url = Node.mainnet.value
            else:
                node_url = Node.testnet.value


        if self._tx['ready']:
            tx_response = send_tx(self._tx, node_url=node_url)

            if tx_response['send']:
                id = tx_response['response'].get('id', sha256(tx_response))
                msg = f'tx-{self.tx_type.replace(" ", "-")}-{id}'
                self.show(
                    name=msg,
                    data=tx_response
                )
                return tx_response
            else:
                print(bcolors.FAIL + f"Your {self.tx_type} dont sended because:\n└──{tx_response['response']}" + bcolors.ENDC)
                return tx_response

        else:
            print(bcolors.FAIL + f'{self.tx_type} Transaction dont send', bcolors.ENDC)
            return self._tx


    def show(self, name: str, data: dict, path: str = './') -> None:
        log_data(data)
        export_json(data, name, path)

