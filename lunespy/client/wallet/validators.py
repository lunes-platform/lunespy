from lunespy.client.wallet.errors import InvalidChecksumAddress
from lunespy.client.wallet.errors import InvalidVersionAddress
from lunespy.client.wallet.errors import InvalidLengthAddress
from lunespy.client.wallet.errors import InvalidChainAddress
from lunespy.client.wallet.errors import InvalidNonce
from lunespy.client.wallet.generators import wallet_generator
from lunespy.client.wallet import ADDRESS_CHECKSUM_LENGTH
from lunespy.client.wallet import ADDRESS_VERSION
from lunespy.client.wallet import ADDRESS_LENGTH
from lunespy.utils.crypto.converters import bytes_to_string
from lunespy.utils.crypto.converters import string_to_bytes
from lunespy.utils.crypto.converters import hash_chain
from lunespy.server import CHAIN_ID
from lunespy.server import OFFLINE
from lunespy.server.address import aliases

def validate_wallet(wallet: dict) -> dict:
    wallet['nonce'] = wallet.get('nonce', 0)
    
    if wallet['nonce'] not in range(0, 4294967295 + 1):
        raise InvalidNonce

    elif wallet.get('seed', False):
        return wallet_generator(seed=wallet['seed'], nonce=wallet['nonce'])
    
    elif wallet.get('privateKey', False):
        return wallet_generator(privateKey=wallet['privateKey'])
    
    elif wallet.get('publicKey', False):
        return wallet_generator(publicKey=wallet['publicKey'])
    
    elif wallet.get('address', False):
        if validate_address(wallet['address']):
            return {
                'privateKey': '',
                'publicKey': '',
                'address': wallet['address'],
                'nonce': 0,
                'seed': ''
            }
        
    elif wallet.get('alias') and not OFFLINE:
        return {
            'address': aliases(wallet['alias']),
            'publicKey': '',
            'privateKey': '',
            'seed': '',
            'nonce': 0,
        }
    
    else:
        return wallet_generator(nonce=wallet['nonce'])


def validate_address(address: str) -> bool:
    bytes_address = bytes_to_string(address)
    checksum = bytes_address[-ADDRESS_CHECKSUM_LENGTH:]
    chain = hash_chain(string_to_bytes(
        bytes_address[:-ADDRESS_CHECKSUM_LENGTH]
        )
    )[:ADDRESS_CHECKSUM_LENGTH]
    if checksum != chain:
        raise InvalidChecksumAddress
    elif bytes_address[0] != chr(ADDRESS_VERSION):
        raise InvalidVersionAddress
    elif bytes_address[1] != CHAIN_ID:
        raise InvalidChainAddress
    elif len(bytes_address) != ADDRESS_LENGTH:
        raise InvalidLengthAddress
    return True
