from lunespy.client.transactions.lease.constants import DEFAULT_CREATE_LEASE_FEE
from lunespy.client.transactions.lease.constants import BYTE_TYPE_CREATE_LEASE
from lunespy.client.transactions.lease.constants import INT_TYPE_CREATE_LEASE
from lunespy.utils.crypto.converters import sign
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account
from lunespy.server import NODE_URL
from datetime import datetime
from base58 import b58decode
from requests import post
import struct


def mount_lease(staker: Account, validator_address: str, lease_data: dict) -> dict:
    timestamp: int = lease_data.get('timestamp', int(datetime.now().timestamp() * 1000))
    amount: int = lease_data['amount']
    lease_fee: int = lease_data.get('lease_fee', DEFAULT_CREATE_LEASE_FEE)    

    bytes_data: bytes = BYTE_TYPE_CREATE_LEASE + \
        b58decode(staker.public_key) + \
        b58decode(validator_address) + \
        struct.pack(">Q", amount) + \
        struct.pack(">Q", lease_fee) + \
        struct.pack(">Q", timestamp)

    signature: bytes = sign(staker.private_key, bytes_data)
    mount_tx: dict = {
        "type": INT_TYPE_CREATE_LEASE,
        "senderPublicKey": staker.public_key,
        "signature": signature.decode(),
        "timestamp": timestamp,
        "fee": lease_fee,

        "recipient": validator_address,
        "amount": amount
    }
    return mount_tx


def validate_lease(staker: Account, lease_data: dict) -> bool:
    amount: int = lease_data.get('amount', -1)

    if not staker.private_key:
        print(bcolors.FAIL + 'Staker `Account` not have a private key' + bcolors.ENDC)
        return False
    elif amount <= 0:
        print(bcolors.FAIL + 'Leasing `amount` cannot be less than 0' + bcolors.ENDC)
        return False
    return True


# todo async
def send_lease(mount_tx: dict, node_url_address: str) -> dict:
    response = post(
        f'{node_url_address}/transactions/broadcast',
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