from lunespy.server import MAINNET_TOTAL_SUPPLY
from lunespy.server import TESTNET_TOTAL_SUPPLY
from lunespy.utils import export_json
from requests import get


def aliases(address: str) -> str:
    pass


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


def all_address_balance(node_ip: str, node_api_key: str) -> dict:    
    url = f"http://{node_ip}/debug/state"
    header = {"X-API-key": node_api_key}


    try:
        all_address: dict = get(url, headers=header).json()
    except:
        return False

    for addr, amount in all_address.items():
        all_address[addr] = amount / 10e7

    return all_address


def balance_from_address(address: str, node_url: str) -> int:
    response = get(f'{node_url}/addresses/balance/{address}')
    if response.ok:
        return response.json()['balance']
    else:
        return -1




def rich_list(**kargs: dict) -> dict:
    """
    Example:
        quantity=30,
        node_ip="127.0.0.1",
        node_api_key="",
        export=True,
        path='.'
    """
    def percent_total(amount: float, supply: float) -> float:
        percent = amount / supply
        return round(float(percent) * 100, 5)

    supply = MAINNET_TOTAL_SUPPLY if kargs['net'] == 'mainnet' else TESTNET_TOTAL_SUPPLY
    wallets = all_address_balance(
        kargs['node_ip'],
        kargs['node_api_key']
    )
    only_address = sorted(wallets, key=wallets.get, reverse=True)
    
    wallets = {
        addr: wallets[addr]
        for addr in only_address[:kargs['quantity']] 
    }    

    rich_list = [
        {
            "address": address,
            "amount": amount,
            "percent": percent_total(amount, supply),
            "link": f"https://lunesnode.lunes.io/addresses/balance/details/{address}"
        }
        for address, amount in wallets.items()
    ]

    total_percent = round(
        sum([
            float(addr['percent'])
            for addr in rich_list
        ]),
        5
    )

    report = {
        "total_supply": supply,
        "total_percent": total_percent,
        "wallet_list": rich_list
    }

    if kargs.get('export', False):
        export_json(
            report,
            "rich_list",
            kargs.get('path', '.')
        )
    return report


def node_leased_list_addres(node_address: str) -> list:
    return [

    ]
   

def reward_amount(node_address: str, time_interval: int, dividend: int) -> float:
    # pegar as taxas do periodo
    # calcula a porcentagem
    pass


def address_score(node_address: str, address: str) -> int:
    total_lease = balance(node_address)
    lease = balance(address)
    response = int(
        ( lease / (total_lease - lease) ) * 100
    )
    return response


def distributing_lease_dividend(leaser, time_interval: int, list_address: list, dividend: int) -> dict:
    from lunespy.client.transactions.mass import MassTransferToken

    if len(list_address) > 100:
        def listasMenores(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
            return lst
    else:
        list_address = [
            {
                "receiver": address,
                "amount": reward_amount(leaser, time_interval, dividend) * address_score(address)
            }
            for address in list_address
        ]
    tx = MassTransferToken(leaser, list_adress).send()

