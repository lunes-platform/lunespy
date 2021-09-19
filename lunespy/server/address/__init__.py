from lunespy.server import NODE_URL
from requests import get


def aliases(address: str) -> str:
    pass


def balance(address: str) -> int:
    response = get(f'{NODE_URL}/addresses/balance/{address}')
    if response.ok:
        return response.json()['balance']
    else:
        return -1
