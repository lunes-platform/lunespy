from requests import get
from lunespy.server.nodes import Node


def block_from_height(height: int, node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet.value}/blocks/at/{height}'
    else:
        full_url = f'{node_url}/blocks/at/{height}' # You have pass your node url with https or other contents
    
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


def range_block(start_block: int, end_block: int, node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet.value}/blocks/seq/{start_block}/{end_block}'
    else:
        full_url = f'{node_url}/blocks/seq/{start_block}/{end_block}' # You have pass your node url with https or other contents
    
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


def last_block(node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet.value}/blocks/last'
    else:
        full_url = f'{node_url}/blocks/last' # You have pass your node url with https or other contents
    
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


def blocks_generated_by_specified_address(address: str, start_block: int, end_block: int, node_url: str = None) -> dict:
    if node_url == None:
        full_url = f'{Node.mainnet.value}/blocks/address/{address}/{start_block}/{end_block}'
    else:
        full_url = f'{node_url}/blocks/address/{address}/{start_block}/{end_block}' # You have pass your node url with https or other contents
    
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
