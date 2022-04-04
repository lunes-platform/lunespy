from pytest import fixture

timestamp = 1234567890123


@fixture
def sender():
    from lunespy.client.wallet import Account

    return Account(
        private_key="8YMbX5BCQdazwgdVfeUpKuoUJrmYpMyGVAGAsNaHVj1u"
    )


@fixture
def receiver():
    from lunespy.client.wallet import Account

    return Account(
        private_key="G6E2xNBWtsRG8XBDmeTQQxZNHHUa6K9dnc9KrYtKyGwM"
    )


@fixture
def basic_transfer_token(sender, receiver):
    from lunespy.client.transactions.transfer import TransferToken

    return TransferToken(
        sender=sender.public_key,
        receiver=receiver.address,
        amount=1000,
        chain="mainnet",
        timestamp=timestamp
    )


@fixture
def tx_with_sign(sender, receiver):
    from lunespy.client.transactions.constants import TransferType

    return {
        "ready": True,
        "type":  TransferType.to_int.value,
        "sender": sender.address,
        "senderPublicKey": sender.public_key,
        "recipient": receiver.address,
        "amount": 100000000000,
        "timestamp": timestamp,
        "fee": TransferType.fee.value,
        "assetId": "",
        "feeAsset": ""
    }


def test_transfer_ready(basic_transfer_token):
    """
        passed public_key, address, amount, chain
        should be return True for tx.ready
    """

    assert basic_transfer_token.ready == True


def test_transfer_transaction(basic_transfer_token, tx_with_sign):
    """
        passed public_key, address, amount, chain
        should be return a dict for tx.trasaction
    """

    assert basic_transfer_token.transaction == tx_with_sign


def test_transfer_sign(basic_transfer_token, sender):
    """
        passed private_key
        should be return a signature for tx.sign
    """
    from lunespy.client.transactions.transfer.validators import serialize_transfer
    from lunespy.utils.crypto.converters import validate_sign, b58_to_bytes

    tx = basic_transfer_token.sign(
        sender.private_key
    )
    assert True == validate_sign(
        b58_to_bytes(sender.public_key),
        serialize_transfer(**basic_transfer_token.transaction),
        b58_to_bytes(tx["signature"])
    )


def test_transfer_transaction_after_signed_tx(basic_transfer_token, sender):
    from pytest import raises
    """
        after sign transaction
        should be return a dict with `signature` and `rawData` keys for tx.transaction
    """
    before = basic_transfer_token.transaction
    basic_transfer_token.sign(sender.private_key)
    after = basic_transfer_token.transaction

    with raises(KeyError):
        assert before['signature']
    assert type(after['signature']) == str


def test_serialize_transfer(basic_transfer_token):
    """
        passed basic_transaction
        should be return a raw_data
    """
    from lunespy.client.transactions.transfer.validators import serialize_transfer
    from base58 import b58encode

    tx: dict = basic_transfer_token.transaction
    message: bytes = serialize_transfer(**tx)

    assert b58encode(message) == "2J2EfWqeqbH17PC5yfioAeQ5h27J76uduH5nafAUuJhKb8gHCSqoQozy16kAgeAgAbjYrewhxEcXeaqvU8knmWWtY2woSGVoE5C8GvPU2NN3R8y9CNes".encode()
    assert list(message) == [4, 28, 26, 172, 20, 253, 115, 23, 6, 248, 59, 119, 129, 151, 144, 5, 252, 208, 116, 12, 81, 146, 227, 208, 88, 57, 27, 134, 143, 7, 76, 94, 8, 0, 0, 0, 0, 1, 31, 113, 251, 4, 203, 0, 0, 0, 23, 72, 118, 232, 0, 0, 0, 0, 0, 0, 15, 66, 64, 1, 49, 146, 80, 170, 11, 139, 27, 185, 41, 131, 242, 219, 45, 180, 199, 38, 41, 173, 240, 198, 30, 146, 73, 23, 128]
    assert tx == {
        'senderPublicKey': '2ti1GM7F7J78J347fqSWSVocueDV3RSCFkLSKqmhk35Z',
        'recipient': '37xRcbn1LiT1Az4REoLhjpca93jPG1gTEwq',
        'sender': '37tQRv7x2RHd32Ss2i1EFTWSTSsqkwXcaBe',
        'timestamp': 1234567890123,
        'amount': 100000000000,
        'fee': 1000000,
        'feeAsset': '',
        'assetId': '',
        'ready': True,
        'type': 4
    }
