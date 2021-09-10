from lunespy.utils.crypto.converters import bytes_to_string
from lunespy.utils.crypto.converters import string_to_bytes
from lunespy.utils.crypto.converters import hash_chain
from lunespy.client.wallet import word_list
from lunespy.server import CHAIN_ID
import axolotl_curve25519 as curve
from base58 import b58decode
from base58 import b58encode
from os import urandom

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
    return ' '.join(words)


def seed_generator(seed: str, nonce: int) -> dict:
    from lunespy.utils.crypto.converters import sha256
    import struct
    
    seed_hash = hash_chain(struct.pack(">L", nonce) + string_to_bytes(seed))
    account_seed_hash = sha256(seed_hash)
    private_key = curve.generatePrivateKey(account_seed_hash)
    public_key = curve.generatePublicKey(private_key)
    return {
        'private_key': b58encode(private_key),
        'public_key': public_key,
        'nonce': nonce,
        'seed': seed
    }


def private_key_generator(private_key: str) -> dict:
    private_key_b58 = b58decode(private_key)
    public_key = curve.generatePublicKey(private_key_b58)
    return {
        'private_key': b58encode(private_key_b58),
        'public_key': public_key,
        'seed': ""
    }
    

def public_key_generator(public_key: str) -> dict:
    public_key_b58 = b58decode(public_key)
    return {
        'private_key': "",
        'public_key': public_key_b58
    }


def addres_generator(public_key: str) -> dict:
    un_hashed_address = chr(1) + str(CHAIN_ID) + hash_chain(public_key)[0:20]
    address_hash = hash_chain(string_to_bytes(un_hashed_address))[0:4]
    address = b58encode(string_to_bytes(un_hashed_address + address_hash))
    public_key_b58 = b58encode(public_key)
    return {
        'public_key': public_key_b58,
        'address': address
    }


def wallet_generator(**data: dict) -> dict:
    response = {}

    if data.get('seed', False):
        response.update(seed_generator(
            data['seed'],
            data['nonce'])
        )

    elif data.get('private_key', False):
        response.update( private_key_generator(data['private_key']) )

    elif data.get('public_key', False):
        response.update( public_key_generator(data['public_key']) )

    else:
        seed = new_seed_generator()
        response.update(seed_generator(
            seed,
            data['nonce']
            )
        )

    response.update( addres_generator(response['public_key']) )
    return response
