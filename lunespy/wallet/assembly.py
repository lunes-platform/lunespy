def random_seed(len: int) -> str:
    from lunespy.wallet.constants import word_list
    from os import urandom

    def f():
        word_count = 2048
        r: bytes = urandom(4)
        x: int = r[3] + (r[2] << 8) + (r[1] << 16) + (r[0] << 24)
        w1: int = x % word_count
        w2: int = ((int(x / word_count) >> 0) + w1) % word_count
        w3: int = ((int((int(x / word_count) >> 0) / word_count) >> 0) + w2) % word_count
        return w1, w2, w3

    n_words_multiple_of_3: int = len // 3

    return " ".join([
        word_list[n]
        for _ in range(n_words_multiple_of_3)
        for n in f()
    ])


def from_seed(seed: str, nonce: int, chain: int):
    from lunespy.crypto import bytes_to_b58, to_address, to_private_key, to_public_key, hidden_seed
    from lunespy.wallet import Wallet

    hash_seed: bytes = hidden_seed(nonce, seed)
    private_key: bytes = to_private_key(hash_seed)
    public_key: bytes = to_public_key(private_key)
    address: bytes = to_address(public_key, chain, 1)

    return Wallet(
        private_key=bytes_to_b58(private_key),
        public_key=bytes_to_b58(public_key),
        address=bytes_to_b58(address),
        nonce=nonce,
        chain=chain,
        seed=seed
    )


def from_private_key(private_key: str, chain: int = 1):
    from lunespy.crypto import bytes_to_b58, b58_to_bytes, to_address, to_private_key, to_public_key
    from lunespy.wallet import Wallet

    private_key: bytes = to_private_key(b58_to_bytes(private_key))
    public_key: bytes = to_public_key(private_key)
    address: bytes = to_address(public_key, chain, 1)

    return Wallet(
        private_key=bytes_to_b58(private_key),
        public_key=bytes_to_b58(public_key),
        address=bytes_to_b58(address),
        seed_len=0,
        nonce=0,
        chain=chain,
        seed=""
    )

