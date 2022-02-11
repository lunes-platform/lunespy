from requests import get
from lunespy.server.nodes import Node

def transaction_from_id(id: str) -> dict:
    full_url = f'http://lunesnode-testnet.lunes.io/transactions/info/{id}'
    response = get(full_url)

    if response.status_code in range(200, 300):
        return {
            'status': 'ok',
            'response': response.json()
        }
    else: 
        return {
            'status': 'error',
            'response': response.text
        }


def unconfirmed_transaction(node_url: str) -> dict:
    full_url = f'{node_url}/transactions/unconfirmed' # You have pass your node url with https or other contents
    response = get(full_url)

    if response.status_code in range(200, 300):
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'stauts': 'error',
            'response': response.text
        }


def transactions_from_address(address: str, limit_transactions: int, node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet.value}/transactions/address/{address}/limit/{limit_transactions}'
    else:
        full_url = f'{node_url}/transactions/address/{address}/limit/{limit_transactions}' # You have pass your node url with https or other contents
    
    response = get(full_url)

    if response.status_code in range(200, 300):
        return {
            'status': 'ok',
            'response': response.json()
        }
    else: 
        return {
            'status': 'error',
            'response': response.text
        }
