from lunespy.client.account import Wallet


def validate_alias(sender: Account, alias_data: dict) -> bool:
    from lunespy.utils import bcolors

    alias: int = alias_data.get('alias', False)
    valid_alias_characters =  "-.0123456789@_abcdefghijklmnopqrstuvwxyz"

    if not sender.private_key:
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


def mount_alias(sender: Account, alias_data: dict) -> dict:
    from lunespy.utils import now
    from lunespy.utils.crypto.converters import sign
    from lunespy.client.transactions.constants import AliasType
    from lunespy.utils.crypto.converters import string_to_bytes
    from base58 import b58decode
    import struct

    timestamp: int = alias_data.get('timestamp', now())
    fee: int = alias_data.get('fee', AliasType.fee.value)
    alias: str = alias_data['alias']
    chain_id: str = sender.chain_id

    aliasWithNetwork = AliasType.mount.value +\
        string_to_bytes(str(chain_id)) + \
        struct.pack(">H", len(alias)) + \
        string_to_bytes(alias)

    bytes_data = AliasType.to_byte.value + \
        b58decode(sender.public_key) + \
        struct.pack(">H", len(aliasWithNetwork)) + \
        aliasWithNetwork + \
        struct.pack(">Q", fee) + \
        struct.pack(">Q", timestamp)

    signature: bytes = sign(sender.private_key, bytes_data)

    mount_tx = {
        "type": AliasType.to_int.value,
        "senderPublicKey": sender.public_key,
        "signature": signature.decode(),
        "timestamp": timestamp,
        "fee": fee,

        "alias": alias
    }
    return mount_tx


def send_alias(mount_tx: dict, node_url: str) -> dict:
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
