from lunespy.client.transactions.alias.constants import DEFAULT_ALIAS_FEE
from lunespy.client.transactions.alias.constants import BYTE_MOUNT_ALIAS
from lunespy.client.transactions.alias.constants import BYTE_TYPE_ALIAS
from lunespy.client.transactions.alias.constants import INT_TYPE_ALIAS
from lunespy.utils.crypto.converters import string_to_bytes
from lunespy.utils.crypto.converters import sign
from lunespy.utils.settings import bcolors
from lunespy.client.wallet import Account
from datetime import datetime
from base58 import b58decode
from requests import post
import struct

def validate_alias(creator: Account, alias_data: dict) -> bool:
    alias: int = alias_data.get('alias', False)
    valid_alias_characters =  "-.0123456789@_abcdefghijklmnopqrstuvwxyz"

    if not creator.private_key:
        print(bcolors.FAIL + 'Sender `Account` not have a private key' + bcolors.ENDC)
        return False

    if alias == False:
        print(bcolors.FAIL + 'Alias_data `alias` dont exists' + bcolors.ENDC)
        return False
    
    if not all(each_char in valid_alias_characters for each_char in alias):
        print(
            bcolors.FAIL + \
            "`Alias` should contain only following characters: -.0123456789@_abcdefghijklmnopqrstuvwxyz" + \
            bcolors.ENDC)
        return False
    
    
    return True

def mount_alias(creator: Account, alias_data: dict) -> dict:
    timestamp: int = alias_data.get('timestamp', int(datetime.now().timestamp() * 1000))
    alias_fee: int = alias_data.get('alias_fee', DEFAULT_ALIAS_FEE)
    alias: str = alias_data['alias']
    alias_lenght: int = len(alias)
    network_id: str = creator.network_id
    
    aliasWithNetwork = b'\x02' +\
        string_to_bytes(str(network_id)) + \
        struct.pack(">H", len(alias)) + \
        string_to_bytes(alias)

    bytes_data = b'\x0a' + \
        b58decode(creator.public_key) + \
        struct.pack(">H", len(aliasWithNetwork)) + \
        aliasWithNetwork + \
        struct.pack(">Q", alias_fee) + \
        struct.pack(">Q", timestamp)

    signature: bytes = sign(creator.private_key, bytes_data)

    mount_tx = {
        "type": INT_TYPE_ALIAS,
        "senderPublicKey": creator.public_key,
        "signature": signature.decode(),
        "timestamp": timestamp,
        "fee": alias_fee,

        "alias": alias
    }
    return mount_tx

def send_alias(mount_tx: dict, node_url_address: str) -> dict:
    
    
    response = post(
        f'{node_url_address}/transactions/broadcast',
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
