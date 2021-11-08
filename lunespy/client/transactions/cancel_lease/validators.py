from lunespy.client.transactions.constants import CancelLeaseType
from lunespy.utils.crypto.converters import sign
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account

from datetime import datetime
from base58 import b58decode
from requests import post
import struct


def mount_cancel(sender: Account, cancel_data: dict) -> dict:
    lease_tx_id: str = cancel_data['lease_tx_id']
    timestamp: int = cancel_data.get('timestamp', int(datetime.now().timestamp() * 1000))
    cancel_fee: int = cancel_data.get('cancel_fee', CancelLeaseType.fee.value)

<<<<<<< HEAD:lunespy/client/transactions/cancel_lease/validators.py
    bytes_data: bytes = CancelLeaseType.type_byte.value + \
        b58decode(staker.public_key) + \
=======
    bytes_data: bytes = BYTE_TYPE_CANCEL_LEASE + \
        b58decode(sender.public_key) + \
>>>>>>> 7a8b7a98cf48f34cba15898d9528f974f0f6d973:lunespy/client/transactions/cancel/validators.py
        struct.pack(">Q", cancel_fee) + \
        struct.pack(">Q", timestamp) + \
        b58decode(lease_tx_id)

    signature: bytes = sign(sender.private_key, bytes_data)
    mount_tx: dict = {
<<<<<<< HEAD:lunespy/client/transactions/cancel_lease/validators.py
        "type": CancelLeaseType.type_int.value,
        "senderPublicKey": staker.public_key,
=======
        "type": INT_TYPE_CANCEL_LEASE,
        "senderPublicKey": sender.public_key,
>>>>>>> 7a8b7a98cf48f34cba15898d9528f974f0f6d973:lunespy/client/transactions/cancel/validators.py
        "signature": signature.decode(),
        "timestamp": timestamp,
        "fee": cancel_fee,

        "leaseId": lease_tx_id
    }
    return mount_tx


def validate_cancel(sender: Account, cancel_data: dict) -> bool:
    amount: int = cancel_data.get('amount', -1)
    lease_tx_id: str = cancel_data.get('lease_tx_id', '')

    if not sender.private_key:
        print(bcolors.FAIL + 'Staker `Account` not have a private key' + bcolors.ENDC)
        return False
    elif lease_tx_id == '':
        print(bcolors.FAIL + 'Leasing must be `lease_tx_id`' + bcolors.ENDC)
        return False
    return True


# todo async
def send_cancel(mount_tx: dict, node_url: str) -> dict:
    response = post(
        f'{node_url}/transactions/broadcast',
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