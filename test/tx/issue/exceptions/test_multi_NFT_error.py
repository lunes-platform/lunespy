from pytest import fixture, mark, raises
from pydantic import ValidationError
from lunespy.wallet import Wallet
from test.tx import sender


@fixture
def error_name_length():
    return [
        {
            "description": "A",
            "reissuable": True,
            "quantity": 10000,
            "decimals": 8,
            "name": "AAA"
        },
        {
            "description": "B",
            "reissuable": True,
            "quantity": 10000,
            "decimals": 8,
            "name": "BBBB-BBBB-BBBB-BBBB"
        },
        {
            "description": "C",
            "reissuable": True,
            "quantity": 10000,
            "decimals": 8,
            "name": "C"
        },
    ]

@fixture
def error_descrition_length():
    return [
        {
            "description": "A" * 1001,
            "reissuable": True,
            "quantity": 10000,
            "decimals": 8,
            "name": "AAAA"
        },
        {
            "description": "B" * 2000,
            "reissuable": True,
            "quantity": 10000,
            "decimals": 8,
            "name": "BBBB"
        },
        {
            "description": "CCC" * 334,
            "reissuable": True,
            "quantity": 10000,
            "decimals": 8,
            "name": "CCCC"
        },
    ]


def test_multiples_NFT_error_name_length(sender: Wallet, error_name_length: list[dict]):
    from lunespy.tx.issue.multi import mint_multiples_NFT

    with raises(ValidationError) as string_err:
        mint_multiples_NFT(sender.public_key, error_name_length)
    assert "name" in str(string_err.value)


def test_multiples_NFT_error_descrition_length(sender: Wallet, error_descrition_length: list[dict]):
    from lunespy.tx.issue.multi import mint_multiples_NFT

    with raises(ValidationError) as string_err:
        mint_multiples_NFT(sender.public_key, error_descrition_length)
    assert "description" in str(string_err.value)
