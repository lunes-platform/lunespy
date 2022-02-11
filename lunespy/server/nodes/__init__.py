from requests import get
from enum import Enum


class Node(Enum):
    mainnet: str = 'https://lunesnode.lunes.io'
    testnet: str = 'https://lunesnode-testnet.lunes.io'
    mainnet_supply: float = 150_728_537.61498705
    testnet_supply: float = 800_100_000.00000000


def all_node_conected_in_node_url(node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet.value}/peers/all'
    else:
        full_url = f'{node_url}/peers/all' # You have pass your node url with https or other contents

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


def node_version(node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet.value}/utils/lunesnode/version'
    else:
        full_url = f'{node_url}/utils/lunesnode/version' # You have pass your node url with https or other contents
    
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


def version_all_lunes_node_conected(node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet.value}/peers/connected'
    else:
        full_url = f'{node_url}/peers/connected' # You have pass your node url with https or other contents
    
    response = get(full_url)

    if response.status_code in range(200, 300):
        return {
            'status': 'ok',
            'response': [
                {
                    'node_url': data['address'][1:],
                    'version': data['applicationVersion']
                }
                for data in response.json()['peers']
            ]
        }
    else:
        return {
            'status': 'error',
            'response': response.text
        }

