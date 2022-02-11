from pytest import fixture
from lunespy.utils import now

timestamp = now()


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
    from lunespy.utils.crypto.converters import validate_sign, b58_to_bytes

    tx = basic_transfer_token.sign(
        sender.private_key
    )
    assert True == validate_sign(
        b58_to_bytes(sender.public_key),
        b58_to_bytes(tx["raw_data"]),
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
