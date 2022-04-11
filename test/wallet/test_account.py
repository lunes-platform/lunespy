from lunespy.wallet.crypto import validate_address
from lunespy.wallet import wallet_factory
from pytest import fixture, mark




@fixture
def account_from_new_seed_mainnet():
    return wallet_factory(chain=1)

@fixture
def account_from_new_seed_testnet():
    return wallet_factory(chain=0)

def validate_address_mainnet(account_from_new_seed_mainnet):
    assert validate_address(chain=1, address=account_from_new_seed_mainnet.address) == True

def validate_address_testnet(account_from_new_seed_testnet):
    assert validate_address(chain=0, address=account_from_new_seed_testnet.address) == True


@fixture
def account_from_seed_mainnet():
    seed = "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"
    return wallet_factory(seed=seed)

@fixture
def account_from_seed_testnet():
    seed = "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"
    return wallet_factory(seed=seed, chain=0)


def test_create_account_from_seed_mainnet(account_from_seed_mainnet):
    assert account_from_seed_mainnet.address == "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"

def test_create_account_from_seed_testnet(account_from_seed_testnet):
    assert account_from_seed_testnet.address == "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"


@mark.parametrize(
    "nonce, address",
    [
        (0, "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"),
        (1, "37tD32367v1fiWgW8waw3QTdYTKKGrCV3zw"),
        (2, "37qYK5eRJEr8a38hUXmxYv9aoQ8NpXH7Aqd"),
        (3, "37w8stLd9JQwUKBrBUQr1VryJuhS3RWqEen"),
        (4, "37vVbQVXEE4Lvs7X4wimsoxAvqBmoyHsWDJ"),
    ]
)
def test_create_account_from_seed_mainnet_with_nonces_0_1_2_3_4(nonce, address):
    seed = "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"
    assert wallet_factory(seed=seed, nonce=nonce).address == address

@mark.parametrize(
    "nonce, address",
    [
        (0, "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"),
        (1, "37UsS2vnqCqCqhFN3vAbivLMkpp4L8GMCyP"),
        (2, "37SCi6Y81XffhDhZPWMdES2K1md7skK1mFu"),
        (3, "37XoGuEKrbEUbVki6SzWh1jhXHCB6jnKFxS"),
        (4, "37X9zRPDwWst43gNyvJSZKpu9CgWsHt1U8i"),
    ]
)
def test_create_account_from_seed_testnet_with_nonces_0_1_2_3_4(nonce, address):
    seed = "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"
    assert wallet_factory(seed=seed, nonce=nonce, chain=0).address == address


@fixture
def account_from_private_key_mainnet():
    private_key = "BnafXBSq1VDUdZ1nSjJoxhnQdBv2hk3o6dbV49TD1bzo"
    return wallet_factory(private_key=private_key, chain=1)

@fixture
def account_from_private_key_testnet():
    private_key = "BnafXBSq1VDUdZ1nSjJoxhnQdBv2hk3o6dbV49TD1bzo"
    return wallet_factory(private_key=private_key, chain=0)


def test_create_account_from_private_key_mainnet(account_from_private_key_mainnet):
    assert account_from_private_key_mainnet.address == "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"

def test_create_account_from_private_key_testnet(account_from_private_key_testnet):
    assert account_from_private_key_testnet.address == "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"
