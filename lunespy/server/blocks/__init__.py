from requests import get

from lunespy.server import address


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


def all_peers_conected(node_url: str) -> dict:
    full_url = f'https://{node_url}/peers/all'
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


def node_version(node_url: str) -> dict:
    full_url = f'https://{node_url}/utils/lunesnode/version'
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


def unconfirmed_transaction(node_url: str) -> dict:
    full_url = f'https://{node_url}/transactions/unconfirmed'
    response = get(full_url)

    if response.ok:
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'stauts': 'error',
            'response': response.text
        }


def transactions_from_address(node_url: str, address: str, limit_transactions: int) -> dict:
    full_url = f'https://{node_url}/transactions/address/{address}/limit/{limit_transactions}'
    response = get(full_url)

    if response.ok:
        return {
            'status': 'ok',
            'response': response.json()
        }
    else: 
        return {
            'status': 'ok',
            'response': response.text
        }


def blocks_generated_by_specified_address(node_url: str, address: str, start_block: int, end_block: int) -> dict:
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


def version_all_lunes_node_conected(node_url: str) -> dict:
    full_url = f'https://{node_url}/peers/connected'
    response = get(full_url)
    dic_peers = response.json()['peers']
    for itens_nodes in dic_peers:
        iten_address = (itens_nodes['address'])[1:]
        iten_application_version = (itens_nodes['applicationVersion'])
        print(f'Address: {iten_address} \nNode Version: {iten_application_version}')
