from lunespy.client.transactions.constants import TransferType
from lunespy.client.wallet.validators import validate_address
from lunespy.utils.crypto.converters import sign
from lunespy.client.wallet import Account
from lunespy.utils import lunes_to_unes
from lunespy.utils import bcolors
from lunespy.utils import now
from base58 import b58decode
from requests import post
from struct import pack


def mount_transfer(sender: Account, receiver: Account, transfer_data: dict) -> dict:
    timestamp: int = transfer_data.get('timestamp', int(now() * 1000))
    transfer_fee: int = transfer_data.get('transfer_fee', TransferType.fee.value)
    amount: int = lunes_to_unes(transfer_data['amount'])
    asset_fee: str = transfer_data.get('asset_fee', "")
    asset_id: str = transfer_data.get('asset_id', "")

    bytes_data: bytes = TransferType.to_byte.value + \
        b58decode(sender.public_key) + \
        (b'\1' + b58decode(asset_id) if asset_id != "" else b'\0') + \
        (b'\1' + b58decode(asset_fee) if asset_fee != "" else b'\0') + \
        pack(">Q", timestamp) + \
        pack(">Q", amount) + \
        pack(">Q", transfer_fee) + \
        b58decode(receiver.address)
    signature: bytes = sign(sender.private_key, bytes_data)
    return {
        "type": TransferType.to_int.value,
        "senderPublicKey": sender.public_key,
        "signature": signature.decode(),
        "timestamp": timestamp,
        "fee": transfer_fee,

        "recipient": receiver.address,
        "feeAsset": asset_fee,
        "assetId": asset_id,
        "amount": amount,
    }


def validate_transfer(sender: Account, receiver: Account, transfer_data: dict) -> bool:
    amount: int = transfer_data.get('amount', -1)

    if not sender.private_key:
        print(bcolors.FAIL + 'Sender `Account` not have a private key' + bcolors.ENDC)
        return False
    elif not validate_address(receiver.address, sender.network_id):
        return False
    elif amount <= 0:
        print(bcolors.FAIL + 'You dont pass `amount` param' + bcolors.ENDC)
        return False
    return True


# todo async
def send_transfer(mount_tx: dict, node_url: str) -> dict:
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
            'send': False,
            'response': response.text
        })
        return mount_tx