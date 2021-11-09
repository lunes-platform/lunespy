from lunespy.client.transactions.constants import ReissueType
from lunespy.utils.crypto.converters import sign
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account
from lunespy.utils import now
from base58 import b58decode
from requests import post
import struct

def validate_reissue(sender: Account, reissue_data: dict) -> bool:
    quantity: int = reissue_data.get('quantity', -1)
    asset_id: str = reissue_data.get('asset_id', False)

    if not sender.private_key:
        print(bcolors.FAIL + 'Creator `Account` not have a private key' + bcolors.ENDC)
        return False

    if quantity < 0:
        print(bcolors.FAIL + 'To Reissue the `quantity` cannot be less than 0' + bcolors.ENDC)
        return False
    
    if asset_id == False:
        print(bcolors.FAIL + 'To Reissue pass an `asset_id`' + bcolors.ENDC)
        return False

    return True


def mount_reissue(sender: Account, reissue_data: dict) -> dict:
    reissue_fee = reissue_data.get('reissue_fee', ReissueType.fee.value)
    timestamp = reissue_data.get('timestamp', int(now() * 1000))
    reissuable = reissue_data.get('reissuable', False)
    asset_id = reissue_data['asset_id']
    quantity = reissue_data['quantity']

    bytes_data = ReissueType.to_byte.value + \
        b58decode(sender.public_key) + \
        b58decode(asset_id) + \
        struct.pack(">Q", quantity) + \
        (b'\1' if reissuable else b'\0') + \
        struct.pack(">Q",reissue_fee) + \
        struct.pack(">Q", timestamp)

    signature: bytes = sign(sender.private_key, bytes_data)
    mount_tx = {
        "type": ReissueType.to_int.value,
        "senderPublicKey": sender.public_key,
        "signature": signature.decode(),
        "timestamp": timestamp,
        "fee": reissue_fee,

        "assetId": asset_id,
        "reissuable": reissuable,
        "quantity": quantity
    }
    return mount_tx


# todo async
def send_reissue(mount_tx: dict, node_url: str) -> dict:
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
