import re
from lunespy.wallet import Wallet, wallet_factory
from pytest import fixture, mark, raises
from lunespy.tx.issue import IssueToken
from pydantic import ValidationError


@fixture
def sender():
    from lunespy.wallet import wallet_factory

    return wallet_factory(
        private_key="8YMbX5BCQdazwgdVfeUpKuoUJrmYpMyGVAGAsNaHVj1u"
    )


@fixture
def create_tx(sender: Wallet):
    from lunespy.tx.issue import issue_token_factory

    return issue_token_factory(
        sender_public_key=sender.public_key,
        name="My Test Token",
        quantity=10000,
        description="This Token Is Not Real, Only Test",
        reissuable=True,
        decimals=8,
        timestamp=1650250375987
    )


@fixture
def sign_tx(sender: Wallet, create_tx: IssueToken):
    create_tx.sign(sender.private_key)
    return create_tx


def test_issue_tx(create_tx: IssueToken):

    assert create_tx.dict() == {
        'senderPublicKey': '2ti1GM7F7J78J347fqSWSVocueDV3RSCFkLSKqmhk35Z',
        'description': 'This Token Is Not Real, Only Test',
        'timestamp': 1650250375987,
        'name': 'My Test Token',
        'reissuable': True,
        'quantity': 10000,
        'fee': 100000000,
        'signature': '',
        'decimals': 8,
        'type': 3
    }


def test_signature_of_issue(sign_tx: IssueToken):
    from lunespy.crypto import validate_signature
    from lunespy.crypto import b58_to_bytes

    assert True == validate_signature(
        b58_to_bytes(sign_tx.senderPublicKey),
        b58_to_bytes(sign_tx.message),
        b58_to_bytes(sign_tx.signature),
    )
