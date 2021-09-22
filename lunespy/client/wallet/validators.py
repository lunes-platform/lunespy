from lunespy.client.wallet.errors import InvalidChecksumAddress
from lunespy.client.wallet.errors import InvalidVersionAddress
from lunespy.client.wallet.errors import InvalidLengthAddress
from lunespy.client.wallet.errors import InvalidChainAddress
from lunespy.client.wallet.errors import InvalidNonce
from lunespy.client.wallet.generators import wallet_generator
from lunespy.client.wallet.constants import ADDRESS_CHECKSUM_LENGTH
from lunespy.client.wallet.constants import ADDRESS_VERSION
from lunespy.client.wallet.constants import ADDRESS_LENGTH
from lunespy.utils.crypto.converters import bytes_to_string
from lunespy.utils.crypto.converters import string_to_bytes
from lunespy.utils.crypto.converters import hash_chain
from lunespy.server import OFFLINE
from lunespy.server.address import aliases

def validate_wallet(wallet: dict) -> dict:
    wallet['nonce'] = wallet.get('nonce', 0)

    if wallet.get('chain', 'mainnet') == 'mainnet':
        chain_id: str = '1'
    else:
        chain_id: str = '0'

    if wallet['nonce'] not in range(0, 4294967295 + 1):
        raise InvalidNonce

    elif wallet.get('seed', False):
        return wallet_generator(seed=wallet['seed'], nonce=wallet['nonce'], chain_id=chain_id)

    elif wallet.get('private_key', False):
        return wallet_generator(private_key=wallet['private_key'], nonce=wallet['nonce'], chain_id=chain_id)

    elif wallet.get('public_key', False):
        return wallet_generator(public_key=wallet['public_key'], nonce=wallet['nonce'], chain_id=chain_id)

    elif wallet.get('address', False):
        if validate_address(wallet['address'], chain_id=chain_id):
            return {
                'private_key': '',
                'public_key': '',
                'address': wallet['address'],
                'nonce': 0,
                'seed': '',
                'hash_seed': '',
                'byte_private_key': b'',
                'byte_public_key': b'',
                'byte_address': wallet['address'].encode()
            }

    elif wallet.get('alias') and not OFFLINE:
        return {
            'private_key': '',
            'public_key': '',
            'address': aliases(wallet['alias']),
            'nonce': 0,
            'seed': '',
            'byte_private_key': b'',
            'byte_public_key': b'',
            'byte_address': aliases(wallet['alias']).encode(),
        }

    else:
        return wallet_generator(nonce=wallet['nonce'], chain_id=chain_id)


def validate_address(address: str, chain_id: str) -> bool:
    bytes_address = bytes_to_string(address, decode=True)
    checksum = bytes_address[-ADDRESS_CHECKSUM_LENGTH:]
    chain = hash_chain(string_to_bytes(
        bytes_address[:-ADDRESS_CHECKSUM_LENGTH]
        )
    )[:ADDRESS_CHECKSUM_LENGTH]

    if checksum != chain:
        raise InvalidChecksumAddress
    elif bytes_address[0] != chr(ADDRESS_VERSION):
        raise InvalidVersionAddress
    elif bytes_address[1] != chain_id:
        raise InvalidChainAddress
    elif len(bytes_address) != ADDRESS_LENGTH:
        raise InvalidLengthAddress
    return True
