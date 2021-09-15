def multirate_padding(used_bytes, align_bytes):
    padlen = align_bytes - used_bytes
    if padlen == 0:
        padlen = align_bytes
    # note: padding done in 'internal bit ordering', wherein LSB is leftmost
    if padlen == 1:
        return [0x81]
    else:
        return [0x01] + ([0x00] * (int(padlen) - 2)) + [0x80]


def string_to_bytes(string: str) -> str:
    return string.encode('latin-1')


def string_to_list(string: str) -> list:
    return [char for char in string]


def bytes_to_string(bytes: str, decode: bool=False) -> str:
    
    if decode:
        from base58 import b58decode
        string_base58 = b58decode(bytes)
        return ''.join(
           map(chr, string_base58)
        )
    else:
        return ''.join(
            map(chr, bytes)
        )


def hash_chain(address: str) -> str:
    from pyblake2 import blake2b
    from lunespy.utils.crypto.algorithms import KeccakHash
    
    keccak256 = KeccakHash()

    x = blake2b(
        address,
        digest_size=32
    ).digest()
    y = keccak256.digest( x )
    return y


def sign(privateKey: str, message: bytes) -> bytes:
    import axolotl_curve25519 as curve
    from base58 import b58encode
    from base58 import b58decode
    from os import urandom

    random64 = urandom(64)
    return b58encode(
        curve.calculateSignature(
            random64,
            b58decode( privateKey ),
            message
        )
    )


def sha256(string: str) -> str:
    import hashlib

    return hashlib.sha256(
        string_to_bytes(string)
    ).digest()


def id(message: str) -> str:
    from base58 import b58encode
    import hashlib

    return b58encode(hashlib.sha256( message ).digest())


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


def bits_to_bytes(x):
    return (int(x) + 7) / 8


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
