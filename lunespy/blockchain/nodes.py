from enum import Enum
from http.client import OK
from httpx import Response
import httpx

class Node(Enum):
    mainnet: str = 'https://lunesnode.lunes.io'
    testnet: str = 'https://lunesnode-testnet.lunes.io'
    mainnet_supply: float = 150_728_537.61498705
    testnet_supply: float = 800_100_000.00000000


def all_peers_conected_in_node_url(node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/peers/all'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')


def node_version(node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/utils/lunesnode/version'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')


def version_all_lunes_node_conected(node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/peers/connected'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')
