from lunespy.blockchain.nodes import Node
from http.client import OK
from httpx import Response
import httpx


def block_from_height(height: int, node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/blocks/at/{height}'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')


def range_block(start_block: int, end_block: int, node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/blocks/seq/{start_block}/{end_block}'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')


def last_block(node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/blocks/last'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')


def blocks_generated_by_specified_address(address: str, start_block: int, end_block: int, node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/blocks/address/{address}/{start_block}/{end_block}'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')
