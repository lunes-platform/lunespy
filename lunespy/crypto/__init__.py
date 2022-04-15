def validate_signature(public_key: bytes, message: bytes, signature: bytes) -> bool:
    from axolotl_curve25519 import verifySignature

    return True if verifySignature(
        public_key,
        message,
        signature
    ) == 0 else False

def fast_signature(private_key: bytes, message: bytes) -> bytes:
    from axolotl_curve25519 import calculateSignature as curve
    from os import urandom

    return curve(
        urandom(64),
        private_key,
        message
    )

def to_sha256(message: bytes) -> bytes:
    from hashlib import sha256

    return sha256(message).digest()

def to_keccak256(message: bytes) -> bytes:
    from sha3 import keccak_256

    return keccak_256(message).digest()

def to_blake2b32b(message: bytes) -> bytes:
    from hashlib import blake2b

    return blake2b(message, digest_size=32).digest()

def bytes_to_b58(message: bytes) -> str:
    from base58 import b58encode

    return b58encode(message).decode()

def b58_to_bytes(message: str) -> bytes:
    from base58 import b58decode

    return b58decode(message)

def to_address(public_key: bytes, chain: int, addr_version: int) -> bytes:
    from lunespy.wallet.constants import ADDRESS_CHECKSUM_LENGTH, ADDRESS_HASH_LENGTH

    raw_addr: bytes = (
        chr(addr_version).encode('latin-1') +
        str(chain).encode('latin-1') +
        to_keccak256(to_blake2b32b(public_key))[:ADDRESS_HASH_LENGTH]
    )
    checksum: bytes = to_keccak256(to_blake2b32b(raw_addr))[:ADDRESS_CHECKSUM_LENGTH]

    return (raw_addr + checksum)

def to_private_key(seed: bytes) -> bytes:
    from axolotl_curve25519 import generatePrivateKey

    return generatePrivateKey(seed)

def to_public_key(private_key: bytes) -> bytes:
    from axolotl_curve25519 import generatePublicKey

    return generatePublicKey(private_key)

def hidden_seed(nonce: int, seed: str) -> bytes:
    from struct import pack

    raw_seed: bytes = (pack(">L", nonce) + seed.encode())
    return to_sha256(to_keccak256(to_blake2b32b(raw_seed)))

def validate_address(chain: int, address: str) -> bool:
    from lunespy.wallet.constants import ADDRESS_CHECKSUM_LENGTH, ADDRESS_VERSION, ADDRESS_LENGTH

    raw_address: bytes = b58_to_bytes(address)
    address_left, checksum = raw_address[:-ADDRESS_CHECKSUM_LENGTH], raw_address[-ADDRESS_CHECKSUM_LENGTH:]
    hash_address_left: str = to_keccak256(to_blake2b32b(address_left))
    addr_checksum: str = hash_address_left[:ADDRESS_CHECKSUM_LENGTH]

    if checksum != addr_checksum:
        return False
    elif raw_address[0] not in ADDRESS_VERSION:
        return False
    elif raw_address[1] != str(chain).encode()[0]:
        return False
    elif len(raw_address) != ADDRESS_LENGTH:
        return False

    return True

def same_chain_address(address_1: str, address_2: str) -> bool:
    x = validate_address(1, address_1) and validate_address(1, address_2)
    y = validate_address(0, address_1) and validate_address(0, address_2)

    return x or y