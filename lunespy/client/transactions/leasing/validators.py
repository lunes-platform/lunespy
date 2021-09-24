from lunespy.client.transactions.leasing.constants import DEFAULT_LEASING_FEE
from lunespy.client.transactions.leasing.constants import BYTE_TYPE_LEASING
from lunespy.client.transactions.leasing.constants import INT_TYPE_LEASING
from lunespy.utils.crypto.converters import sign
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account
from lunespy.server import NODE_URL
from datetime import datetime
from base58 import b58decode
from requests import post
import struct


def mount_leasing(staker: Account, validator_address: str, tx_data: dict) -> dict:
    timestamp: int = tx_data.get('timestamp', int(datetime.now().timestamp() * 1000))
    amount: int = tx_data['amount']
    leasing_fee: int = tx_data.get('leasing_fee', DEFAULT_LEASING_FEE)    

    bytes_data: bytes = BYTE_TYPE_LEASING + \
        b58decode(staker.public_key) + \
        b58decode(validator_address) + \
        struct.pack(">Q", amount) + \
        struct.pack(">Q", leasing_fee) + \
        struct.pack(">Q", timestamp)

    signature: bytes = sign(staker.private_key, bytes_data)
    mount_tx: dict = {
        "senderPublicKey": staker.public_key,
        "signature": signature.decode(),
        "recipient": validator_address,
        "type": INT_TYPE_LEASING,
        "timestamp": timestamp,
        "fee": leasing_fee,
        "amount": amount,
    }
    return mount_tx


def validate_leasing(staker: Account, tx_data: dict) -> bool:
    amount: int = tx_data.get('amount', -1)

    if not staker.private_key:
        print(bcolors.FAIL + 'Staker `Account` not have a private key' + bcolors.ENDC)
        return False
    elif amount <= 0:
        print(bcolors.FAIL + 'Leasing `amount` cannot be less than 0' + bcolors.ENDC)
        return False
    return True


# todo async
def send_leasing(mount_tx: dict, node: str) -> dict:
    response = post(
        f'{node}/transactions/broadcast',
        json=mount_tx,
        headers={
            'content-type':
            'application/json'
        })

    if response.ok:
        mount_tx['send'] = True
        mount_tx['response'] = response.json()
        return mount_tx
    else:
        mount_tx['send'] = False
        mount_tx['response'] = response.text
        return mount_tx
