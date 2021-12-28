def multirate_padding(used_bytes, align_bytes):
    padlen = align_bytes - used_bytes
    if padlen == 0:
        padlen = align_bytes
    # note: padding done in 'internal bit ordering', wherein LSB is leftmost
    if padlen == 1:
        return [0x81]
    else:
        return [0x01] + ([0x00] * (int(padlen) - 2)) + [0x80]


def bits_to_bytes(x):
    return (int(x) + 7) / 8


def string_to_bytes(string: str) -> bytes:
    return string.encode('latin-1')


def string_to_list(string: str) -> list:
    return [char for char in string]


def bytes_to_string(bytes: bytes, decode: bool=False) -> str:
    if not decode:
        return ''.join(
            map(chr, bytes)
        )
    else:
        from base58 import b58decode

        return ''.join(
            map(chr, b58decode(bytes))
        )


def hash_data(data: str) -> str:
    from lunespy.utils.crypto.algorithms import KeccakHash
    from hashlib import blake2b
    keccak256 = KeccakHash()

    return keccak256.digest( 
        blake2b(data, digest_size=32).digest()
    )


def sign(private_key: str, message: bytes) -> bytes:
    from axolotl_curve25519 import calculateSignature as curve
    from base58 import b58encode
    from base58 import b58decode
    from os import urandom
    return b58encode(
        curve(
            urandom(64),
            b58decode( private_key ),
            message
        )
    )


def sha256(string: str) -> str:
    from hashlib import sha256

    return sha256(
        string_to_bytes(string)
    ).digest()


def id(message: str) -> str:
    from base58 import b58encode
    from hashlib import sha256

    return b58encode(sha256( message ).digest())


def ror(value, right, bits):
    from lunespy.utils.crypto import Masks

    top = value >> right
    bot = (value & Masks[right]) << (bits - right)
    return bot | top


def rol(value, left, bits):
    from lunespy.utils.crypto import Masks

    top = value >> (bits - left)
    bot = (value & Masks[bits - left]) << left
    return bot | top


def keccak_f(state):
    from lunespy.utils.crypto import RoundConstants
    from math import log

    def round(A, RC):
        from lunespy.utils.crypto import RotationConstants
        from functools import reduce
        from operator import xor

        W, H = state.W, state.H
        rangeW, rangeH = state.rangeW, state.rangeH
        lanew = state.lanew
        zero = state.zero

        # theta
        C = [reduce(xor, A[x]) for x in rangeW]
        D = [0] * W
        for x in rangeW:
            D[x] = C[(x - 1) % W] ^ rol(C[(x + 1) % W], 1, lanew)
            for y in rangeH:
                A[x][y] ^= D[x]

        # rho and pi
        B = zero()
        for x in rangeW:
            for y in rangeH:
                B[y % W][(2 * x + 3 * y) % H] = rol(A[x][y], RotationConstants[y][x], lanew)

        # chi
        for x in rangeW:
            for y in rangeH:
                A[x][y] = B[x][y] ^ ((~ B[(x + 1) % W][y]) & B[(x + 2) % W][y])

        # iota
        A[0][0] ^= RC

    l = int(log(state.lanew, 2))
    nr = 12 + 2 * l

    for ir in range(nr):
        round(state.s, RoundConstants[ir])
