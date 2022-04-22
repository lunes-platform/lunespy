from http.client import OK
from lunespy.blockchain.nodes import Node
from lunespy.utils import unes_to_lunes
from lunespy.utils import export_json
from httpx import Response
import httpx

def address_associated_with_an_alias(alias: str, node_url: str = Node.mainnet.value) -> Response:
    """
    In this function you find out if there a alias associated with an address.

    Just passing a alias and url of your node.
    """
    full_url = f'{node_url}/addresses/alias/by-alias/{alias}'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')


def asset_distribution(asset_id: str, node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/assets/{asset_id}/distribution'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')


def balance_all_assets_of_address(address: str, node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/assets/balance/{address}'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')


def balance_for_especify_asset_of_address(address: str, asset_id: str, node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/assets/balance/{address}/{asset_id}' 

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')


def balance_of_all_address(node_ip: str, node_api_key: str) -> Response:    
    full_url = f"{node_ip}/debug/state"
    header = {"X-API-key": node_api_key}
    return httpx.get(full_url, headers=header)


def balance_of_address(address: str, node_url: str = Node.mainnet.value) -> int:
    full_url = f'{node_url}/addresses/balance/{address}'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')


def list_of_rich(**kargs: dict) -> dict:
    """
    Example:
        quantity=30,
        node_ip_port="127.0.0.1:555",
        net="mainnet" or "testnet"
        node_api_key="",
        export=True or False,
        path='./data/'
    """
    def percent(amount: float) -> float:
        return round((amount / supply) * 100, 5)

    def percent_total(wallets: list) -> float:
        total = sum([
            i['amount']
            for i in wallets
        ])
        return percent(total)

    response = balance_of_all_address(kargs['node_ip'], kargs['node_api_key'])
    supply = Node.mainnet_total_supply.value if kargs['net'] == 'mainnet' else Node.testnet_total_supply.value
    link = Node.mainnet_blockexplorer.value if kargs['net'] == 'mainnet' else Node.testnet_blockexplorer.value

    if response['status'] != 'ok':
        return  {
            'status': 'error',
            'response': response['response']
        }
    else:
        wallets_lunes = dict(zip(
            response['response'],
            list(map(
                lambda item: unes_to_lunes(item),
                response['response'].values()
            ))
        ))

        wallets = sorted(
            [
                {
                    'address': address,
                    'amount': amount,
                    'percent': percent(amount),
                    'link': f'{link}/address/{address}'
                }
                for address, amount in list(
                    wallets_lunes.items()
                )
            ],
            key = lambda item: item.get('amount'),
            reverse = True
        )[:kargs.get('quantity')]

        report = {
            "total_supply": supply,
            "chain": kargs['net'],
            "total_percent": percent_total(wallets),
            "wallet_list": wallets
        }

        if kargs.get('export', False):
            export_json(
                report,
                "rich_list",
                kargs.get('path', './data/')
            )

        return  {
            'status': 'ok',
            'response': report
        }


def leasing_active_by_address(address: str, node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/leasing/active/{address}'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')


def address_of_node_from_url(node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/addresses'        

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')


def aliases_associated_with_an_address(address: str, node_url: str = Node.mainnet.value) -> Response:
    full_url = f'{node_url}/addresses/alias/by-address/{address}'

    if httpx.get(full_url).status_code == OK:
        return httpx.get(full_url).json()

    else:
        print('Something wrong with your request')
