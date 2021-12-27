from lunespy.utils.crypto.converters import string_to_bytes
from lunespy.utils.crypto.converters import hash_data
from lunespy.client.wallet.constants import word_list
from base58 import b58decode
from base58 import b58encode
from os import urandom


def address_generator(public_key: str, network_id: str) -> dict:
    un_hashed_address = chr(1) + str(network_id) + hash_data(public_key)[0:20]
    address_hash = hash_data(string_to_bytes(un_hashed_address))[0:4]
    address = b58encode(string_to_bytes(un_hashed_address + address_hash))
    public_key_b58 = b58encode(public_key)
    return {
        'seed': "",
        'hash_seed': "",
        'nonce': 0,
        'network': 'mainnet' if network_id == '1' else 'testnet',
        'network_id': network_id,
        'private_key': "",
        'public_key': public_key_b58.decode(),
        'address': address.decode(),
        'byte_private_key': b"",
        'byte_public_key': public_key_b58,
        'byte_address': address

    }


def new_seed_generator(n_words: int) -> str:
    from lunespy.utils.crypto.converters import bytes_to_string

    def f():
        wordCount = 2048
        r = bytes_to_string(urandom(4))
        x = (ord(r[3])) + (ord(r[2]) << 8) + (ord(r[1]) << 16) + (ord(r[0]) << 24)
        w1 = x % wordCount
        w2 = ((int(x / wordCount) >> 0) + w1) % wordCount
        w3 = ((int((int(x / wordCount) >> 0) / wordCount) >> 0) + w2) % wordCount
        return w1, w2, w3

    n_words_multiple_of_3: int = n_words // 3

    return " ".join([
        word_list[n]
        for _ in range(n_words_multiple_of_3)
        for n in f()
    ])


def seed_generator(seed: str, nonce: int, network_id: str) -> dict:
    from lunespy.utils.crypto.converters import sha256
    from axolotl_curve25519 import generatePrivateKey, generatePublicKey
    from struct import pack

    hash_seed = hash_data(
        pack(">L", nonce) + string_to_bytes(seed)
    )
    account_hash_seed = sha256(hash_seed)
    private_key = generatePrivateKey(account_hash_seed)
    public_key = generatePublicKey(private_key)
    address = address_generator(public_key, network_id)
    return {
        'seed': seed,
        'hash_seed': b58encode(seed).decode(),
        'nonce': nonce,
        'network': 'mainnet' if network_id == '1' else 'testnet',
        'network_id': network_id,
        'private_key': b58encode(private_key).decode(),
        'public_key': b58encode(public_key).decode(),
        'address': address['address'],
        'byte_private_key': b58encode(private_key),
        'byte_public_key': b58encode(public_key),
        'byte_address': address['byte_address']
    }


def private_key_generator(private_key: str, network_id: str) -> dict:
    from axolotl_curve25519 import generatePublicKey

    private_key_b58 = b58decode(private_key)
    public_key = generatePublicKey(private_key_b58)
    address = address_generator(public_key, network_id)
    return {
        'seed': "",
        'hash_seed': "",
        'nonce': 0,
        'network': 'mainnet' if network_id == '1' else 'testnet',
        'network_id': network_id,
        'private_key': b58encode(private_key_b58).decode(),
        'public_key': b58encode(public_key).decode(),
        'address': address['address'],
        'byte_private_key': b58encode(private_key_b58),
        'byte_public_key': b58encode(public_key),
        'byte_address': address['byte_address']

    }
    

def public_key_generator(public_key: str, network_id: str) -> dict:
    public_key_b58 = b58decode(public_key)
    address = address_generator(public_key_b58, network_id)
    return {
        'seed': "",
        'hash_seed': "",
        'nonce': 0,
        'network': 'mainnet' if network_id == '1' else 'testnet',
        'network_id': network_id,
        'private_key': "",
        'public_key': b58encode(public_key_b58).decode(),
        'address': address['address'],
        'byte_private_key': b"",
        'byte_public_key': b58encode(public_key_b58),
        'byte_address': address['byte_address']
    }


def wallet_generator(**data: dict) -> dict:
    if data.get('seed', False):
        return seed_generator(seed=data['seed'], nonce=data['nonce'], network_id=data['network_id'])

    elif data.get('private_key', False):
        return private_key_generator(private_key=data['private_key'], network_id=data['network_id'])

    elif data.get('public_key', False):
        return public_key_generator(public_key=data['public_key'], network_id=data['network_id'])

    elif data.get('address', False):
        return address_generator(public_key="", network_id=data['network_id'])

    elif data.get('n_words', False):
        seed = new_seed_generator(n_words=data['n_words'])
        return seed_generator(seed=seed, nonce=data['nonce'], network_id=data['network_id'])
    
    else:
        n_words: int = 12
        seed: str = new_seed_generator(n_words)
        return seed_generator(seed=seed, nonce=data['nonce'], network_id=data['network_id'])
