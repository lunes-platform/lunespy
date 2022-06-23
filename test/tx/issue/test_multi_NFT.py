from lunespy.wallet import Wallet
from pytest import fixture, mark
from test.tx import sender

@fixture
def list_of_tokens():
    return [
        {
            "description": "A",
            "reissuable": True,
            "name": "AAAA"
        },
        {
            "description": "B",
            "reissuable": True,
            "name": "BBBB"
        },
        {
            "description": "C",
            "reissuable": True,
            "name": "CCCC"
        },
    ]


def test_length_of_create_multiples_NFT(sender: Wallet, list_of_tokens: list[dict]):
    from lunespy.tx.issue.multi import mint_multiples_NFT

    tokens = mint_multiples_NFT(sender.public_key, list_of_tokens)

    assert tokens.length == len(list_of_tokens)


def test_create_multiples_NFT(sender: Wallet, list_of_tokens: list[dict]):
    from lunespy.tx.issue.multi import mint_multiples_NFT

    tokens = mint_multiples_NFT(sender.public_key, list_of_tokens)

    for i in tokens.tokens:
        assert i.senderPublicKey == sender.public_key


def test_signing_multiples_NFT(sender: Wallet, list_of_tokens: list[dict]):
    from lunespy.crypto import b58_to_bytes, validate_signature
    from lunespy.tx.issue.multi import mint_multiples_NFT

    tokens = mint_multiples_NFT(sender.public_key, list_of_tokens)

    tokens.sign(sender.private_key)

    for i in tokens.tokens:
        assert True == validate_signature(
            b58_to_bytes(sender.public_key),
            b58_to_bytes(i.message),
            b58_to_bytes(i.signature),
        )
