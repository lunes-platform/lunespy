from lunespy.client.transactions.burn.constants import DEFAULT_BURN_FEE
from lunespy.client.transactions.burn.constants import BYTE_TYPE_BURN
from lunespy.client.transactions.burn.constants import INT_TYPE_BURN
from lunespy.utils.crypto.converters import string_to_bytes
from lunespy.utils.crypto.converters import sign
from lunespy.utils.crypto.converters import bytes_to_string
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account
from datetime import datetime
from base58 import b58decode
from requests import post
import struct


def mount_burn(burner: Account, burn_data: dict) -> dict:
    timestamp: int = burn_data.get('timestamp', int(datetime.now().timestamp() * 1000))
    burn_fee: int = burn_data.get('burn_fee', DEFAULT_BURN_FEE)
    quantity: int = burn_data.get('quantity', 0)
    asset_id: int = burn_data['asset_id']

    bytes_data: bytes = BYTE_TYPE_BURN + \
        b58decode(burner.public_key) + \
        b58decode(asset_id) + \
        struct.pack(">Q", quantity) + \
        struct.pack(">Q", burn_fee) + \
        struct.pack(">Q", timestamp)

    signature: bytes = sign(burner.private_key, bytes_data)
    mount_tx = {
        "senderPublicKey": burner.public_key,
        "signature": signature.decode(),
        "assetId": asset_id,
        "timestamp": timestamp,
        "type": INT_TYPE_BURN,
        "quantity": quantity,
        "fee": burn_fee,
    }
    return mount_tx


def validate_burn(burner: Account, burn_data: dict) -> bool:
    quantity: int = burn_data.get('quantity', -1)
    asset_id: str = burn_data.get('asset_id', False)

    if not burner.private_key:
        print(bcolors.FAIL + 'Burner `Account` not have a private key' + bcolors.ENDC)
        return False

    if quantity < 0:
        print(bcolors.FAIL + 'Burn `quantity` cannot be less than 0' + bcolors.ENDC)
        return False

    if asset_id == False:
        print(bcolors.FAIL + 'Burn_data `asset_id` cannot exists' + bcolors.ENDC)
        return False

    return True


# todo async
def send_burn(mount_tx: dict, node: str) -> dict:
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
        mount_tx['response'] = response.json()
        return mount_tx
