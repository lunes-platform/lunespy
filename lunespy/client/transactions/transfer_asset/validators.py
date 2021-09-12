from lunespy.client.transactions.transfer_asset.constants import DEFAULT_TX_FEE
from lunespy.server import NODE_URL
from lunespy.server.address import balance
from lunespy.utils.crypto.converters import sign
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account
from datetime import datetime
from base58 import b58decode
from requests import post
import struct

def mount_transfer(sender: Account, receiver: Account, tx_data: dict) -> dict:
    timestamp: int = tx_data.get('timestamp', int(datetime.now().timestamp() * 1000))
    amount: int = tx_data['amount']
    tx_fee: int = tx_data.get('tx_fee', DEFAULT_TX_FEE)
    asset_id = tx_data.get('asset_id', "")
    fee_asset = tx_data.get('fee_asset', "")
    
    bytes_data: bytes = b'\4' + \
        b58decode(sender.public_key) + \
        (b'\1' + b58decode(asset_id) if asset_id != "" else b'\0') + \
        (b'\1' + b58decode(fee_asset) if fee_asset != "" else b'\0') + \
        struct.pack(">Q", timestamp) + \
        struct.pack(">Q", amount) + \
        struct.pack(">Q", tx_fee) + \
        b58decode(receiver.address)
    signature: bytes = sign(sender.private_key, bytes_data)
    mount_tx: dict = {
        "senderPublicKey": sender.public_key,
        "signature": signature.decode(),
        "timestamp": timestamp,
        "recipient": receiver.address,
        "feeAsset": fee_asset,
        "assetId": asset_id,
        "amount": amount,
        "type": 4,
        "fee": tx_fee
    }
    return mount_tx

# todo async
def validate_transfer(sender: Account, tx_data: dict) -> bool:
    amount: int = tx_data.get('amount', -1)
    tx_fee: int = tx_data.get('tx_fee', DEFAULT_TX_FEE)
    
    if not sender.private_key:
        print(bcolors.FAIL + 'Sender `Account` not have a private key' + bcolors.ENDC)
        return False
    elif amount <= 0:
        print(bcolors.FAIL + 'You dont pass `amount` param' + bcolors.ENDC)
        return False
    return True

# todo async
def send_transfer(mount_tx: dict) -> dict:
    response = post(f'{NODE_URL}/transactions/broadcast', json=mount_tx, headers={'content-type': 'application/json'})
    if response.ok:
        mount_tx['send'] = True
        mount_tx['reason'] = response.json()
        return mount_tx
    else:
        mount_tx['send'] = False
        mount_tx['reason'] = response.json()
        return mount_tx