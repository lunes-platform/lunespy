from lunespy.blockchain.nodes import Node
from http.client import OK
from httpx import Response
import httpx

def transaction_from_id(id: str) -> Response:
    full_url = f'http://lunesnode-testnet.lunes.io/transactions/info/{id}'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')


def unconfirmed_transaction(node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/transactions/unconfirmed'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')


def transactions_from_address(address: str, limit_transactions: int, node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/transactions/address/{address}/limit/{limit_transactions}'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')
