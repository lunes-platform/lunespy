def from_hex(string: str) -> bytes:
    return bytes.fromhex(string)


def string_to_b58(data: bytes) -> str:
    from base58 import b58encode

    return b58encode(data).decode()


def b58_to_bytes(data: str) -> bytes:
    from base58 import b58decode

    return b58decode(data)


def validate_sign(public_key: bytes, message: bytes, signature: bytes) -> bool:
    from axolotl_curve25519 import verifySignature

    verified = verifySignature(
        public_key,
        message,
        signature
    )

    return True if verified == 0 else False


def hash_keccak256_blake2b32b(data: bytes) -> str:
    from lunespy.utils.crypto.algorithms import KeccakHash
    from hashlib import blake2b
    keccak256 = KeccakHash()

    return keccak256.digest( 
        blake2b(data, digest_size=32).digest()
    )


def sign(private_key: bytes, message: bytes) -> bytes:
    from axolotl_curve25519 import calculateSignature as curve
    from os import urandom

    return curve(
            urandom(64),
            private_key,
            message
        )


def sha256(string: bytes) -> bytes:
    from hashlib import sha256

    return sha256(
        string
    ).digest()

