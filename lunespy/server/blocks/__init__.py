from requests import get 


def block_from_height(node_url: str, height: int) -> dict:
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


def range_block(node_url: str, start_block: int, end_block: int) -> dict:
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


def asset_distribution(node_url: str, asset_id: str) -> dict:
    full_url = f'https://{node_url}/assets/{asset_id}/distribution'
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


def balance_asset_from_address(node_url: str, adress: str) -> dict:
    full_url = f'https://{node_url}/assets/balance/{adress}'
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


def balance_for_especify_asset_from_address(node_url: str, address: str, asset_id: str) -> dict:
    full_url = f'https://{node_url}/assets/balance/{address}/{asset_id}'
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