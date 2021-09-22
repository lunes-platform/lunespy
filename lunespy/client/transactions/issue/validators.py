from lunespy.client.transactions.issue.constants import DEFAULT_ISSUE_FEE
from lunespy.client.transactions.issue.constants import BYTE_TYPE_ISSUE
from lunespy.client.transactions.issue.constants import INT_TYPE_ISSUE
from lunespy.utils.crypto.converters import string_to_bytes
from lunespy.utils.crypto.converters import sign
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account
from datetime import datetime
from base58 import b58decode
from requests import post
import struct


def mount_issue(creator: Account, issue_data: dict) -> dict:
    timestamp: int = issue_data.get('timestamp', int(datetime.now().timestamp() * 1000))
    issue_fee: int = issue_data.get('issue_fee', DEFAULT_ISSUE_FEE)
    reissuable: bool = issue_data.get('reissuable', False)
    description: str = issue_data.get('description', '')
    quantity: int = issue_data.get('quantity', 0)
    decimals: str = issue_data.get('decimals', 0)
    name: str = issue_data.get('name', '')

    bytes_data: bytes = BYTE_TYPE_ISSUE + \
        b58decode(creator.public_key) + \
        struct.pack(">H", len(name)) + \
        string_to_bytes(name) + \
        struct.pack(">H", len(description)) + \
        string_to_bytes(description) + \
        struct.pack(">Q", quantity) + \
        struct.pack(">B", decimals) + \
        (b'\1' if reissuable else b'\0') + \
        struct.pack(">Q", issue_fee) + \
        struct.pack(">Q", timestamp)

    signature: bytes = sign(creator.private_key, bytes_data)
    mount_tx = {
        "senderPublicKey": creator.public_key,
        "signature": signature.decode(),
        "description": description,
        "reissuable": reissuable,
        "timestamp": timestamp,
        "type": INT_TYPE_ISSUE,
        "decimals": decimals,
        "quantity": quantity,
        "fee": issue_fee,
        "name": name
    }
    return mount_tx


def validate_issue(creator: Account, issue_data: dict) -> bool:
    quantity: int = issue_data.get('quantity', -1)
    name: str = issue_data.get('name', '')

    if not creator.private_key:
        print(bcolors.FAIL + 'Sender `Account` not have a private key' + bcolors.ENDC)
        return False

    if quantity < 0:
        print(bcolors.FAIL + 'Issue_data `quantity` cannot be less than 0' + bcolors.ENDC)
        return False

    if len(name) not in range(4, 16 + 1):
        print(bcolors.FAIL + 'Asset name must be between 4 and 16 characters long' + bcolors.ENDC)
        return False

    return True


# todo async
def send_issue(mount_tx: dict, node: str) -> dict:
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
