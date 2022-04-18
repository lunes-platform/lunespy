from lunespy.wallet import Wallet, wallet_factory
from lunespy.tx.transfer import TransferToken
from lunespy.crypto import same_chain_address
from pytest import fixture, mark, raises
from pydantic import ValidationError


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
        sender_public_key=sender.public_key,
        receiver_address=receiver.address,
        amount=1000,
        timestamp=1650250375987
    )


@fixture
def sign_tx(sender: Wallet, create_tx: TransferToken):
    create_tx.sign(sender.private_key)
    return create_tx



def test_issue_tx(create_tx: TransferToken):

    assert create_tx.dict() == {
        'senderPublicKey': '2ti1GM7F7J78J347fqSWSVocueDV3RSCFkLSKqmhk35Z',
        'recipient': '37xRcbn1LiT1Az4REoLhjpca93jPG1gTEwq',
        'sender': '37tQRv7x2RHd32Ss2i1EFTWSTSsqkwXcaBe',
        'timestamp': 1650250375987,
        'amount': 100000000000,
        'signature': '',
        'fee': 1000000,
        'feeAsset': '',
        'assetId': '',
        'type': 4
    }


@mark.parametrize(
    "sender, receiver, result",
    [
        [wallet_factory(chain=1), wallet_factory(chain=0), False],
        [wallet_factory(chain=0), wallet_factory(chain=1), False],
    ]
)
def test_invalid_create_transfer(sender: Wallet, receiver: Wallet, result):
    from lunespy.tx.transfer import transfer_token_factory

    assert same_chain_address(sender.address, receiver.address) == result
    with raises(ValidationError):
        transfer_token_factory(
            sender_public_key=sender.public_key,
            receiver_address=receiver.address,
            amount=1000,
            chain=sender.chain
        )

def test_create_transfer_testnet():
    from lunespy.tx.transfer import transfer_token_factory
    from lunespy.wallet import wallet_factory

    sender = wallet_factory(chain=0)
    receiver = wallet_factory(chain=0)

    transfer_token_factory(
        sender_public_key=sender.public_key,
        receiver_address=receiver.address,
        amount=1000,
        chain=0
    )


def test_signature_of_transfer(sign_tx: TransferToken):
    from lunespy.crypto import validate_signature
    from lunespy.crypto import b58_to_bytes

    assert True == validate_signature(
        b58_to_bytes(sign_tx.senderPublicKey),
        b58_to_bytes(sign_tx.message),
        b58_to_bytes(sign_tx.signature),
    )

