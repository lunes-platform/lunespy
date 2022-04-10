from lunespy.client.account import Wallet


def mount_burn(sender: Account, burn_data: dict) -> dict:
    from lunespy.utils import now
    from lunespy.client.transactions.constants import BurnType
    from lunespy.utils.crypto.converters import sign
    from base58 import b58decode
    import struct

    timestamp: int = burn_data.get('timestamp', now())
    fee: int = burn_data.get('fee', BurnType.fee.value)
    quantity: int = burn_data.get('quantity', 0)
    asset_id: int = burn_data['asset_id']

    bytes_data: bytes = BurnType.to_byte.value + \
        b58decode(sender.public_key) + \
        b58decode(asset_id) + \
        struct.pack(">Q", quantity) + \
        struct.pack(">Q", fee) + \
        struct.pack(">Q", timestamp)

    signature: bytes = sign(sender.private_key, bytes_data)
    mount_tx = {
        "type": BurnType.to_int.value,
        "senderPublicKey": sender.public_key,
        "signature": signature.decode(),
        "timestamp": timestamp,
        "fee": fee,

        "assetId": asset_id,
        "quantity": quantity
    }
    return mount_tx


def validate_burn(sender: Account, burn_data: dict) -> bool:
    from lunespy.utils import bcolors

    quantity: int = burn_data.get('quantity', -1)
    asset_id: str = burn_data.get('asset_id', False)

    if not sender.private_key:
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
def send_burn(mount_tx: dict, node_url: str) -> dict:
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
