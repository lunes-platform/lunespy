def validate_wallet(wallet: dict) -> dict:
    from lunespy.client.wallet.errors import InvalidNonce
    from lunespy.client.wallet.generators import wallet_generator

    wallet['nonce'] = wallet.get('nonce', 0)

    if wallet.get('network', 'mainnet') == 'mainnet':
        wallet['network_id'] = '1'
        wallet['network'] = 'mainnet'
    else:
        wallet['network_id'] = '0'
        wallet['network'] = 'testnet'

    if wallet['nonce'] not in range(0, 4_294_967_295 + 1):
        raise InvalidNonce

    elif wallet.get('seed', False):
        return wallet_generator(**wallet)

    elif wallet.get('private_key', False):
        return wallet_generator(**wallet)

    elif wallet.get('public_key', False):
        return wallet_generator(**wallet)

    elif wallet.get('address', False):
        if validate_address(wallet['address'], network_id=wallet['network_id']):
            return {
                'private_key': '',
                'public_key': '',
                'address': wallet['address'],
                'nonce': 0,
                'network': wallet['network'],
                'network_id': wallet['network_id'],
                'seed': '',
                'hash_seed': '',
                'byte_private_key': b'',
                'byte_public_key': b'',
                'byte_address': wallet['address'].encode()
            }

    elif wallet.get('alias'):
        from lunespy.server.address import aliases

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
        return wallet_generator(**wallet)


def validate_address(address: str, network_id: str) -> bool:
    from lunespy.client.wallet.errors import InvalidChecksumAddress
    from lunespy.client.wallet.errors import InvalidVersionAddress
    from lunespy.client.wallet.errors import InvalidLengthAddress
    from lunespy.client.wallet.errors import InvalidChainAddress
    from lunespy.client.wallet.constants import ADDRESS_CHECKSUM_LENGTH
    from lunespy.client.wallet.constants import ADDRESS_VERSION
    from lunespy.client.wallet.constants import ADDRESS_LENGTH
    from lunespy.utils.crypto.converters import bytes_to_string
    from lunespy.utils.crypto.converters import string_to_bytes
    from lunespy.utils.crypto.converters import hash_data

    bytes_address = bytes_to_string(address, decode=True)
    checksum = bytes_address[-ADDRESS_CHECKSUM_LENGTH:]
    length_checksum = bytes_address[:-ADDRESS_CHECKSUM_LENGTH]
    length_checksum_bytes = string_to_bytes(length_checksum)
    hash_checksum = hash_data(length_checksum_bytes)
    network = hash_checksum[:ADDRESS_CHECKSUM_LENGTH]

    if checksum != network:
        raise InvalidChecksumAddress
    elif bytes_address[0] != chr(ADDRESS_VERSION):
        raise InvalidVersionAddress
    elif bytes_address[1] != network_id:
        raise InvalidChainAddress
    elif len(bytes_address) != ADDRESS_LENGTH:
        raise InvalidLengthAddress
    return True
