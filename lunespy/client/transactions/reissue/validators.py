from lunespy.client.transactions.constants import ReissueType
from lunespy.utils.crypto.converters import sign
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account
from datetime import datetime
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


<<<<<<< HEAD
def mount_reissue(creator: Account, reissue_data: dict) -> dict:
    reissue_fee = reissue_data.get('reissue_fee', ReissueType.type_int.value)
=======
def mount_reissue(sender: Account, reissue_data: dict) -> dict:
    reissue_fee = reissue_data.get('reissue_fee', DEFAULT_REISSUE_FEE)
>>>>>>> 7a8b7a98cf48f34cba15898d9528f974f0f6d973
    timestamp = reissue_data.get('timestamp', int(datetime.now().timestamp() * 1000))
    reissuable = reissue_data.get('reissuable', False)
    asset_id = reissue_data['asset_id']
    quantity = reissue_data['quantity']

<<<<<<< HEAD
    bytes_data = ReissueType.type_byte.value + \
        b58decode(creator.public_key) + \
=======
    bytes_data = BYTE_TYPE_REISSUE + \
        b58decode(sender.public_key) + \
>>>>>>> 7a8b7a98cf48f34cba15898d9528f974f0f6d973
        b58decode(asset_id) + \
        struct.pack(">Q", quantity) + \
        (b'\1' if reissuable else b'\0') + \
        struct.pack(">Q",reissue_fee) + \
        struct.pack(">Q", timestamp)

    signature: bytes = sign(sender.private_key, bytes_data)
    mount_tx = {
<<<<<<< HEAD
        "type": ReissueType.type_int.value,
        "senderPublicKey": creator.public_key,
=======
        "type": INT_TYPE_REISSUE,
        "senderPublicKey": sender.public_key,
>>>>>>> 7a8b7a98cf48f34cba15898d9528f974f0f6d973
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
