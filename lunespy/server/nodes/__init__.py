from requests import get


def all_node_conected_in_node_url(node_url: str) -> dict:
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


def version_all_lunes_node_conected(node_url: str) -> dict:
    full_url = f'https://{node_url}/peers/connected'
    response = get(full_url)
    if response.ok:
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
