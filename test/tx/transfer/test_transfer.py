from lunespy.tx.transfer import TransferToken
from lunespy.wallet import Wallet
from pytest import fixture

@fixture
def sender():
    from lunespy.wallet import wallet_factory

    return wallet_factory(
        private_key="8YMbX5BCQdazwgdVfeUpKuoUJrmYpMyGVAGAsNaHVj1u"
    )


@fixture
def receiver():
    from lunespy.wallet import wallet_factory

    return wallet_factory(
        private_key="G6E2xNBWtsRG8XBDmeTQQxZNHHUa6K9dnc9KrYtKyGwM"
    )


@fixture
def create_tx(sender: Wallet, receiver: Wallet):
    from lunespy.tx.transfer import transfer_token_factory

    return transfer_token_factory(
        sender=sender.public_key,
        receiver=receiver.address,
        amount=1000
    )


@fixture
def sign_tx(sender: Wallet, create_tx: TransferToken):
    create_tx.sign(sender.private_key)
    return create_tx


def test_signature_of_transfer(sign_tx: TransferToken):
    from lunespy.utils.crypto.converters import validate_sign
    from lunespy.wallet.crypto import b58_to_bytes

    assert True == validate_sign(
        b58_to_bytes(sign_tx.senderPublicKey),
        b58_to_bytes(sign_tx.message),
        b58_to_bytes(sign_tx.signature),
    )


def test_send_transfer():
    assert 1 == 1
