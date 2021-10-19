from lunespy.server import TOTAL_SUPPLY
from lunespy.server import NODE_URL
from lunespy.utils import export_dict
from requests import get


def aliases(address: str) -> str:
    pass


def all_address_balance(node_ip: str, node_api_key: str) -> dict:    
    url = f"http://{node_ip}:5555/debug/state"
    header = {"X-API-key": node_api_key}

    all_address: dict = get(url, headers=header).json()

    for addr, amount in all_address.items():
        all_address[addr] = amount / 10e7

    return all_address


def balance(address: str) -> int:
    response = get(f'{NODE_URL}/addresses/balance/{address}')
    if response.ok:
        return response.json()['balance']
    else:
        return -1


def percent_total(amount: float) -> float:
    percent = amount / TOTAL_SUPPLY
    return round(float(percent) * 100, 5)


def rich_list(**kargs: dict) -> dict:
    """
    Example:
        quantity=30,
        node_ip="127.0.0.1",
        node_api_key="",
        export=True,
        path='.'
    """
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
            "percent": percent_total(amount),
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
        "total_supply": TOTAL_SUPPLY,
        "total_percent": total_percent,
        "wallet_list": rich_list
    }

    if kargs.get('export', False):
        export_dict(
            kargs.get('path', '.'),
            "rich_list.json",
            report)
    return report


from lunespy.client.transactions.mass import MassTransferToken


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


def distributing_lease_dividend(leaser: Account, time_interval: int, list_address: list, dividend: int) -> dict:
    if len(list_address) > 100:
        def listasMenores(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
            return lst
    else:
        list_address = [
            {
                "receiver": address
                "amount": reward_amount(leaser, time_interval, dividend) * address_score(address)
            }
            for address in list_address
        ]
    tx = MassTransferToken(leaser, list_adress).send()


fee = 10
list_address = node_leased_list_addres(node_address)
distributing_lease_dividend(node, time_interval, list_address, fee)