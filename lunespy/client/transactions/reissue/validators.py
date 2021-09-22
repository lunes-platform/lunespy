from lunespy.client.transactions.reissue.constants import DEFAULT_REISSUE_FEE
from lunespy.client.transactions.reissue.constants import BYTE_TYPE_REISSUE
from lunespy.client.transactions.reissue.constants import INT_TYPE_REISSUE
from lunespy.utils.crypto.converters import sign
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account
from datetime import datetime
from base58 import b58decode
from requests import post
import struct

def validate_reissue(creator: Account, reissue_data: dict) -> bool:
    quantity: int = reissue_data.get('quantity', -1)
    asset_id: str = reissue_data.get('asset_id', False)

    if not creator.private_key:
        print(bcolors.FAIL + 'Creator `Account` not have a private key' + bcolors.ENDC)
        return False

    if quantity < 0:
        print(bcolors.FAIL + 'Reissue_data `quantity` cannot be less than 0' + bcolors.ENDC)
        return False
    
    if asset_id == False:
        print(bcolors.FAIL + 'Reissue_data `asset_id` cannot exists' + bcolors.ENDC)
        return False

    return True


def mount_reissue(creator: Account, reissue_data: dict) -> dict:
    reissue_fee = reissue_data.get('reissue_fee', DEFAULT_REISSUE_FEE)
    timestamp = reissue_data.get('timestamp', int(datetime.now().timestamp() * 1000))
    reissuable = reissue_data.get('reissuable', False)
    asset_id = reissue_data['asset_id']
    quantity = reissue_data['quantity']

    bytes_data = BYTE_TYPE_REISSUE + \
        b58decode(creator.public_key) + \
        b58decode(asset_id) + \
        struct.pack(">Q", quantity) + \
        (b'\1' if reissuable else b'\0') + \
        struct.pack(">Q",reissue_fee) + \
        struct.pack(">Q", timestamp)

    signature: bytes = sign(creator.private_key, bytes_data)
    mount_tx = {
        "senderPublicKey": creator.public_key,
        "assetId": asset_id,
        "type": INT_TYPE_REISSUE,
        "reissuable": reissuable,
        "signature": signature.decode(),
        "timestamp": timestamp,
        "quantity": quantity,
        "fee": reissue_fee,
    }
    return mount_tx


# todo async
def send_reissue(mount_tx: dict, node: str) -> dict:
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
