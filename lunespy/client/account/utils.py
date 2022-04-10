def address_generator(public_key: bytes, chain_id: str, address_version: str = None) -> bytes:
    from lunespy.utils.crypto.converters import hash_keccak256_blake2b32b

    version = address_version if address_version else chr(1)
    public_key_hash = hash_keccak256_blake2b32b(public_key)[:20]
    raw_address = (version + chain_id + public_key_hash)
    checksum = hash_keccak256_blake2b32b(raw_address.encode('latin-1'))[:4]
    return (raw_address + checksum).encode('latin-1')


def new_seed_generator(n_words: int) -> str:
    from lunespy.client.account.constants import word_list
    from os import urandom

    def f():
        word_count = 2048
        r: bytes = urandom(4)
        x: int = r[3] + (r[2] << 8) + (r[1] << 16) + (r[0] << 24)
        w1: int = x % word_count
        w2: int = ((int(x / word_count) >> 0) + w1) % word_count
        w3: int = ((int((int(x / word_count) >> 0) / word_count) >> 0) + w2) % word_count
        return w1, w2, w3

    n_words_multiple_of_3: int = n_words // 3

    return " ".join([
        word_list[n]
        for _ in range(n_words_multiple_of_3)
        for n in f()
    ])


def seed_generator(seed: str, nonce: int, chain_id: str, address_version: str) -> dict:
    from lunespy.utils.crypto.converters import string_to_b58, hash_keccak256_blake2b32b, sha256, from_hex
    from axolotl_curve25519 import generatePrivateKey, generatePublicKey
    from struct import pack

    nonce_seed: str = (pack(">L", nonce) + seed.encode()).hex()
    raw_seed: str = hash_keccak256_blake2b32b(from_hex(nonce_seed)).encode('latin-1').hex()
    hash_seed: str = sha256(from_hex(raw_seed)).hex()

    private_key: str = generatePrivateKey(from_hex(hash_seed)).hex()
    public_key: str = generatePublicKey(from_hex(private_key)).hex()
    address = address_generator(from_hex(public_key), chain_id, address_version).hex()

    return {
        'seed': seed,
        'nonce': nonce,
        'chain': 'mainnet' if chain_id == '1' else 'testnet',
        'private_key': string_to_b58(from_hex(private_key)),
        'public_key': string_to_b58(from_hex(public_key)),
        'address': string_to_b58(from_hex(address))
    }


def private_key_generator(private_key: str, chain_id: str, address_version: str) -> dict:
    from lunespy.utils.crypto.converters import string_to_b58, b58_to_bytes, from_hex
    from axolotl_curve25519 import generatePublicKey

    public_key = generatePublicKey(b58_to_bytes(private_key)).hex()
    address = address_generator(from_hex(public_key), chain_id, address_version).hex()

    return {
        'chain': 'mainnet' if chain_id == '1' else 'testnet',
        'chain_id': chain_id,
        'private_key': private_key,
        'public_key': string_to_b58(from_hex(public_key)),
        'address': string_to_b58(from_hex(address))
    }


def public_key_generator(public_key: str, chain_id: str, address_version: str) -> dict:
    from lunespy.utils.crypto.converters import string_to_b58, b58_to_bytes

    return {
        'chain': 'mainnet' if chain_id == '1' else 'testnet',
        'public_key': public_key,
        'address': string_to_b58(address_generator(b58_to_bytes(public_key), chain_id, address_version))
    }


def validate_address(address: str, chain_id: str) -> bool:
    from lunespy.client.account.errors import InvalidChecksumAddress ,InvalidVersionAddress ,InvalidLengthAddress, InvalidChainAddress
    from lunespy.client.account.constants import ADDRESS_CHECKSUM_LENGTH, ADDRESS_VERSION, ADDRESS_LENGTH
    from lunespy.utils.crypto.converters import b58_to_bytes, hash_keccak256_blake2b32b

    def slice(string: str, index: int) -> tuple:
        return string[:-index], string[-index:]

    raw_address: str = b58_to_bytes(address).decode('latin-1')
    address_left, checksum = slice(raw_address, ADDRESS_CHECKSUM_LENGTH)
    hash_address_left: str = hash_keccak256_blake2b32b(address_left.encode('latin-1'))
    chain: str = hash_address_left[:ADDRESS_CHECKSUM_LENGTH]

    if checksum != chain:
        raise InvalidChecksumAddress
    elif raw_address[0] not in ADDRESS_VERSION:
        raise InvalidVersionAddress
    elif raw_address[1] != chain_id:
        raise InvalidChainAddress
    elif len(raw_address) != ADDRESS_LENGTH:
        raise InvalidLengthAddress

    return True


def new(n_words, seed, nonce, chain, private_key, public_key, address, address_version):
    from lunespy.client.account.errors import InvalidNonce, InvalidData
    from lunespy.client.account.constants import ADDRESS_VERSION

    if seed:
        if nonce:
            if 0 <= nonce <= 4_294_967_296:
                InvalidNonce
        chain = chain if chain else "mainnet"

        return seed_generator(
            seed,
            nonce if nonce else 0,
            "1" if chain == "mainnet" else "0",
            address_version if address_version else ADDRESS_VERSION[0]
        )

    elif private_key:
        chain = chain if chain else "mainnet"

        return private_key_generator(
            private_key,
            "1" if chain == "mainnet" else "0",
            address_version if address_version else ADDRESS_VERSION[0],
        )

    elif public_key:
        chain = chain if chain else "mainnet"

        return public_key_generator(
            public_key,
            "1" if chain == "mainnet" else "0",
            address_version if address_version else ADDRESS_VERSION[0]
        )

    elif address:
        chain = chain if chain else "mainnet"
        validate_address(
            address,
            "1" if chain == "mainnet" else "0"
        )
        return {
            "address": address,
            "chain_id": "1" if chain == "mainnet" else "0",
        }

    else:
        if nonce:
            if 0 <= nonce <= 4_294_967_296:
                InvalidNonce
        chain = chain if chain else "mainnet"
        seed: str = new_seed_generator(
            n_words if n_words else 12
        )

        return seed_generator(
            seed,
            nonce if nonce else 0,
            "1" if chain == "mainnet" else "0",
            address_version if address_version else ADDRESS_VERSION[0]
        )

