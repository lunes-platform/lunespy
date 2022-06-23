from lunespy.wallet import Wallet
from pytest import fixture, mark
from test.tx import sender
from typing import List


@fixture
def list_of_tokens():
    return [
        {
            "description": "A",
            "reissuable": True,
            "quantity": 10000,
            "decimals": 8,
            "name": "AAAA"
        },
        {
            "description": "B",
            "reissuable": True,
            "quantity": 10000,
            "decimals": 8,
            "name": "BBBB"
        },
        {
            "description": "C",
            "reissuable": True,
            "quantity": 10000,
            "decimals": 8,
            "name": "CCCC"
        },
    ]


def test_length_of_create_multiples_tokens(sender: Wallet, list_of_tokens: List[dict]):
    from lunespy.tx.issue.multi import issue_multiples_tokens

    tokens = issue_multiples_tokens(sender.public_key, list_of_tokens)

    assert tokens.length == len(list_of_tokens)


def test_create_multiples_tokens(sender: Wallet, list_of_tokens: List[dict]):
    from lunespy.tx.issue.multi import issue_multiples_tokens

    tokens = issue_multiples_tokens(sender.public_key, list_of_tokens)

    for i in tokens.tokens:
        assert i.senderPublicKey == sender.public_key


def test_signing_multiples_tokens(sender: Wallet, list_of_tokens: List[dict]):
    from lunespy.crypto import b58_to_bytes, validate_signature
    from lunespy.tx.issue.multi import issue_multiples_tokens

    tokens = issue_multiples_tokens(sender.public_key, list_of_tokens)

    tokens.sign(sender.private_key)

    for i in tokens.tokens:
        assert True == validate_signature(
            b58_to_bytes(sender.public_key),
            b58_to_bytes(i.message),
            b58_to_bytes(i.signature),
        )
