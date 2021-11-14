from requests import get


def all_node_conected(node_url: str) -> dict:
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
    dic_peers = response.json()['peers']
    for itens_nodes in dic_peers:
        item_address = (itens_nodes['address'])[1:]
        item_application_version = (itens_nodes['applicationVersion'])
        print(f'Address: {item_address} \nNode Version: {item_application_version}')
