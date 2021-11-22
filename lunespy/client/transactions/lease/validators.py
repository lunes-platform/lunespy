from lunespy.client.transactions.constants import LeaseType
from lunespy.utils.crypto.converters import sign
from lunespy.utils import bcolors
from lunespy.client.wallet import Account

from lunespy.utils import now
from base58 import b58decode
from requests import post
import struct


def mount_lease(sender: Account, validator_address: str, lease_data: dict) -> dict:
    timestamp: int = lease_data.get('timestamp', int(now() * 1000))
    amount: int = lease_data['amount']
    fee: int = lease_data.get('fee', LeaseType.fee.value)

    bytes_data: bytes = LeaseType.to_byte.value + \
        b58decode(sender.public_key) + \
        b58decode(validator_address) + \
        struct.pack(">Q", amount) + \
        struct.pack(">Q", fee) + \
        struct.pack(">Q", timestamp)

    signature: bytes = sign(sender.private_key, bytes_data)
    mount_tx: dict = {
        "type": LeaseType.to_int.value,
        "senderPublicKey": sender.public_key,
        "signature": signature.decode(),
        "timestamp": timestamp,
        "fee": fee,

        "recipient": validator_address,
        "amount": amount
    }
    return mount_tx


def validate_lease(sender: Account, lease_data: dict) -> bool:
    amount: int = lease_data.get('amount', -1)

    if not sender.private_key:
        print(bcolors.FAIL + 'Staker `Account` not have a private key' + bcolors.ENDC)
        return False
    elif amount <= 0:
        print(bcolors.FAIL + 'Leasing `amount` cannot be less than 0' + bcolors.ENDC)
        return False
    return True


# todo async
def send_lease(mount_tx: dict, node_url: str) -> dict:
    response = post(
        f'{node_url}/transactions/broadcast',
        json=mount_tx,
        headers={
            'content-type':
            'application/json'
        })

    if response.ok:
        mount_tx.update({
            'send': True,
            'response': response.json()
        })
        return mount_tx
    else:
        mount_tx.update({
            'send': True,
            'response': response.json()
        })
        return mount_tx
