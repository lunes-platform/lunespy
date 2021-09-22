from lunespy.utils.crypto.converters import bytes_to_string
from lunespy.utils.crypto.converters import string_to_bytes
from lunespy.utils.crypto.converters import hash_chain
from lunespy.client.wallet.constants import word_list
import axolotl_curve25519 as curve
from base58 import b58decode
from base58 import b58encode
from os import urandom



def address_generator(public_key: str, chain_id: str) -> dict:
    un_hashed_address = chr(1) + str(chain_id) + hash_chain(public_key)[0:20]
    address_hash = hash_chain(string_to_bytes(un_hashed_address))[0:4]
    address = b58encode(string_to_bytes(un_hashed_address + address_hash))
    public_key_b58 = b58encode(public_key)
    return {
        'seed': "",
        'hash_seed': "",
        'nonce': 0,
        'private_key': "",
        'public_key': public_key_b58.decode(),
        'address': address.decode(),
        'byte_private_key': b"",
        'byte_public_key': public_key_b58,
        'byte_address': address

    }


def new_seed_generator() -> str:
    wordCount = 2048
    words = []
    for i in range(5):
        r = bytes_to_string(urandom(4))
        x = (ord(r[3])) + (ord(r[2]) << 8) + (ord(r[1]) << 16) + (ord(r[0]) << 24)
        w1 = x % wordCount
        w2 = ((int(x / wordCount) >> 0) + w1) % wordCount
        w3 = ((int((int(x / wordCount) >> 0) / wordCount) >> 0) + w2) % wordCount
        words.append(word_list[w1])
        words.append(word_list[w2])
        words.append(word_list[w3])
    return " ".join(words)


def seed_generator(seed: str, nonce: int, chain_id: str) -> dict:
    from lunespy.utils.crypto.converters import sha256
    import struct
    
    hash_seed = hash_chain(struct.pack(">L", nonce) + string_to_bytes(seed))
    account_hash_seed = sha256(hash_seed)
    private_key = curve.generatePrivateKey(account_hash_seed)
    public_key = curve.generatePublicKey(private_key)
    address = address_generator(public_key, chain_id)
    return {
        'seed': seed,
        'hash_seed': b58encode(seed).decode(),
        'nonce': nonce,
        'private_key': b58encode(private_key).decode(),
        'public_key': b58encode(public_key).decode(),
        'address': address['address'],
        'byte_private_key': b58encode(private_key),
        'byte_public_key': b58encode(public_key),
        'byte_address': address['byte_address']
    }


def private_key_generator(private_key: str, chain_id: str) -> dict:
    private_key_b58 = b58decode(private_key)
    public_key = curve.generatePublicKey(private_key_b58)
    address = address_generator(public_key, chain_id)
    return {
        'seed': "",
        'hash_seed': "",
        'nonce': 0,
        'private_key': b58encode(private_key_b58).decode(),
        'public_key': b58encode(public_key).decode(),
        'address': address['address'],
        'byte_private_key': b58encode(private_key_b58),
        'byte_public_key': b58encode(public_key),
        'byte_address': address['byte_address']

    }
    

def public_key_generator(public_key: str, chain_id: str) -> dict:
    public_key_b58 = b58decode(public_key)
    address = address_generator(public_key_b58, chain_id)
    return {
        'seed': "",
        'hash_seed': "",
        'nonce': 0,
        'private_key': "",
        'public_key': b58encode(public_key_b58).decode(),
        'address': address['address'],
        'byte_private_key': b"",
        'byte_public_key': b58encode(public_key_b58),
        'byte_address': address['byte_address']
    }



def wallet_generator(**data: dict) -> dict:
    if data.get('seed', False):
        return seed_generator(seed=data['seed'], nonce=data['nonce'], chain_id=data['chain_id'])

    elif data.get('private_key', False):
        return private_key_generator(private_key=data['private_key'], chain_id=data['chain_id'])

    elif data.get('public_key', False):
        return public_key_generator(public_key=data['public_key'], chain_id=data['chain_id'])

    elif data.get('address', False):
        return address_generator(public_key="", chain_id=data['chain_id'])

    else:
        seed = new_seed_generator()
        return seed_generator(seed=seed, nonce=data['nonce'], chain_id=data['chain_id'])