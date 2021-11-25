from requests import get
from lunespy.server import Node


def block_from_height(height: int, node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet_url.value}/blocks/at/{height}'
    else:
        full_url = f'https://{node_url}/blocks/at/{height}'
    
    response = get(full_url)
    
    if response.ok:
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'status': 'error',
            'response': response.text
        }


def range_block(start_block: int, end_block: int, node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet_url.value}/blocks/seq/{start_block}/{end_block}'
    else:
        full_url = f'https://{node_url}/blocks/seq/{start_block}/{end_block}'
    
    response = get(full_url)

    if response.ok:
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'status': 'error',
            'response': response.text
        }


def last_block(node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet_url.value}/blocks/last'
    else:
        full_url = f'https://{node_url}/blocks/last'
    
    response = get(full_url)

    if response.ok:
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
                'status': 'error',
                'response': response.text
            }


def blocks_generated_by_specified_address(address: str, start_block: int, end_block: int, node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet_url.value}/blocks/address/{address}/{start_block}/{end_block}'
    else:
        full_url = f'https://{node_url}/blocks/address/{address}/{start_block}/{end_block}'
    
    response = get(full_url)

    if response.ok:
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'status': 'error',
            'response': response.text
        }
