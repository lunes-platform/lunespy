from lunespy.client.account import Wallet


def validate_reissue(sender: Account, reissue_data: dict) -> bool:
    from lunespy.utils import bcolors

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
    from lunespy.client.transactions.constants import ReissueType
    from lunespy.utils.crypto.converters import sign
    from lunespy.utils import now
    from base58 import b58decode
    import struct

    fee = reissue_data.get('fee', ReissueType.fee.value)
    quantity = reissue_data['quantity']
    reissuable = reissue_data.get('reissuable', False)
    timestamp = reissue_data.get('timestamp', now())
    asset_id = reissue_data['asset_id']
    
    bytes_data = ReissueType.to_byte.value + \
        b58decode(sender.public_key) + \
        b58decode(asset_id) + \
        struct.pack(">Q", quantity) + \
        (b'\1' if reissuable else b'\0') + \
        struct.pack(">Q",fee) + \
        struct.pack(">Q", timestamp)

    signature: bytes = sign(sender.private_key, bytes_data)
    mount_tx = {
        "type": ReissueType.to_int.value,
        "senderPublicKey": sender.public_key,
        "signature": signature.decode(),
        "timestamp": timestamp,
        "fee": fee,

        "assetId": asset_id,
        "reissuable": reissuable,
        "quantity": quantity
    }
    return mount_tx


# todo async
def send_reissue(mount_tx: dict, node_url: str) -> dict:
    from requests import post

    response = post(
        f'{node_url}/transactions/broadcast',
        json=mount_tx,
        headers={
            'content-type':
            'application/json'
        })

    if response.status_code in range(200, 300):
        mount_tx.update({
            'send': True,
            'response': response.json()
        })
        return mount_tx
    else:
        mount_tx.update({
            'send': False,
            'response': response.text
        })
        return mount_tx
