from pytest import fixture, mark

class TestAccontFromNewSeed:
    from lunespy.client.wallet import Account


    @fixture
    def account_from_new_seed_mainnet(self):
        return self.Account(chain="mainnet")

    @fixture
    def account_from_new_seed_testnet(self):
        return self.Account(chain="testnet")

    def test_create_account_from_new_seed_mainnet(self, account_from_new_seed_mainnet):
        assert type(account_from_new_seed_mainnet) == self.Account

    def test_create_account_from_new_seed_testnet(self, account_from_new_seed_testnet):
        assert type(account_from_new_seed_testnet) == self.Account

    def test_address_from_create_account_from_new_seed_mainnet(self, account_from_new_seed_mainnet):
        from lunespy.client.wallet.utils import validate_address

        assert validate_address(account_from_new_seed_mainnet.address, chain_id="1") == True

    def test_address_from_create_account_from_new_seed_testnet(self, account_from_new_seed_testnet):
        from lunespy.client.wallet.utils import validate_address

        assert validate_address(account_from_new_seed_testnet.address, chain_id="0") == True


class TestAccountFromSeed:
    from lunespy.client.wallet import Account

    @fixture
    def account_from_seed_mainnet(self):
        seed = "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"
        return self.Account(seed=seed)

    @fixture
    def account_from_seed_testnet(self):
        seed = "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"
        return self.Account(seed=seed, chain="testnet")


    def test_create_account_from_seed_mainnet(self, account_from_seed_mainnet):
        assert account_from_seed_mainnet.address == "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"

    def test_create_account_from_seed_testnet(self, account_from_seed_testnet):
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
    def test_create_account_from_seed_mainnet_with_nonces_0_1_2_3_4(self, nonce, address):

        seed = "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"
        assert self.Account(seed=seed, nonce=nonce).address == address

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
    def test_create_account_from_seed_testnet_with_nonces_0_1_2_3_4(self, nonce, address):

        seed = "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"
        assert self.Account(seed=seed, nonce=nonce, chain="testnet").address == address


class TestAccountFromPrivateKey:

    from lunespy.client.wallet import Account

    @fixture
    def account_from_private_key_mainnet(self):
        private_key = "BnafXBSq1VDUdZ1nSjJoxhnQdBv2hk3o6dbV49TD1bzo"
        return self.Account(private_key=private_key, chain="mainnet")

    @fixture
    def account_from_private_key_testnet(self):
        private_key = "BnafXBSq1VDUdZ1nSjJoxhnQdBv2hk3o6dbV49TD1bzo"
        return self.Account(private_key=private_key, chain="testnet")


    def test_create_account_from_private_key_mainnet(self, account_from_private_key_mainnet):
        assert account_from_private_key_mainnet.address == "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"

    def test_create_account_from_private_key_testnet(self, account_from_private_key_testnet):
        assert account_from_private_key_testnet.address == "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"


class TestAccountFromPublicKey:
    from lunespy.client.wallet import Account

    @fixture
    def account_from_public_key_mainnet(self):
        public_key = "2uuQVr3B5aGgvSJ5BMCw4Cd19tdYdnMGoYnji99aPde4"
        return self.Account(public_key=public_key, chain="mainnet")

    @fixture
    def account_from_public_key_testnet(self):
        public_key = "2uuQVr3B5aGgvSJ5BMCw4Cd19tdYdnMGoYnji99aPde4"
        return self.Account(public_key=public_key, chain="testnet")


    def test_create_account_from_publick_key_mainnet(self, account_from_public_key_mainnet):
        assert account_from_public_key_mainnet.address == "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"

    def test_create_account_from_publick_key_testnet(self, account_from_public_key_testnet):
        assert account_from_public_key_testnet.address == "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"


class TestAccountFromAddress:
    from lunespy.client.wallet import Account

    @fixture
    def account_from_address_mainnet(self):
        address = "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"
        return self.Account(address=address, chain="mainnet")

    @fixture
    def account_from_address_testnet(self):
        address = "7PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"
        return self.Account(address=address, chain="testnet")


    def test_create_account_from_address_mainnet(self, account_from_address_mainnet):
        assert account_from_address_mainnet.address == "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"

    def test_create_account_from_address_testnet(self, account_from_address_testnet):
        assert account_from_address_testnet.address == "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"