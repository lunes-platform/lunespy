import pytest


class TestCreateAccountStepByStep:
    from pytest import mark


    @mark.parametrize(
        "nonce, seed, hex_seed",
        [
            (
                0,
                "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit",
                "000000007363727562206775617264207377696d2063617463682072616e67652075706f6e206461776e20656e73757265207365676d656e7420616c7068612073656e74656e6365207370656e64206566666f7274206261722062656e65666974"
            ),
            (
                1,
                "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit",
                "000000017363727562206775617264207377696d2063617463682072616e67652075706f6e206461776e20656e73757265207365676d656e7420616c7068612073656e74656e6365207370656e64206566666f7274206261722062656e65666974"
            ),
            (
                2,
                "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit",
                "000000027363727562206775617264207377696d2063617463682072616e67652075706f6e206461776e20656e73757265207365676d656e7420616c7068612073656e74656e6365207370656e64206566666f7274206261722062656e65666974"
            ),
            (
                3,
                "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit",
                "000000037363727562206775617264207377696d2063617463682072616e67652075706f6e206461776e20656e73757265207365676d656e7420616c7068612073656e74656e6365207370656e64206566666f7274206261722062656e65666974"
            ),
            (
                4,
                "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit",
                "000000047363727562206775617264207377696d2063617463682072616e67652075706f6e206461776e20656e73757265207365676d656e7420616c7068612073656e74656e6365207370656e64206566666f7274206261722062656e65666974"
            )
        ]
    )
    def test_nonce_seed_for_0_1_2_3_4_nonces(self, nonce, seed, hex_seed):
        from struct import pack

        nonce_seed: str = (pack(">L", nonce) + seed.encode()).hex()
        assert nonce_seed == hex_seed


    @mark.parametrize(
        "hex_seed, raw_seed",
        [
            (
                "000000007363727562206775617264207377696d2063617463682072616e67652075706f6e206461776e20656e73757265207365676d656e7420616c7068612073656e74656e6365207370656e64206566666f7274206261722062656e65666974",
                "cc872e22459e5c220323651e07097a30252162075fa10152e1de0f9b9c8c358a"
            ),
            (
                "000000017363727562206775617264207377696d2063617463682072616e67652075706f6e206461776e20656e73757265207365676d656e7420616c7068612073656e74656e6365207370656e64206566666f7274206261722062656e65666974",
                "312a14407453264a7dc508b4daa627f521bac6cd817f4f0d816690d7b5806897"
            ),
            (
                "000000027363727562206775617264207377696d2063617463682072616e67652075706f6e206461776e20656e73757265207365676d656e7420616c7068612073656e74656e6365207370656e64206566666f7274206261722062656e65666974",
                "29201f71d95566db58d1e3886b32a7da0333217dd6f6f63b6b73790fe8971b9a"
            ),
            (
                "000000037363727562206775617264207377696d2063617463682072616e67652075706f6e206461776e20656e73757265207365676d656e7420616c7068612073656e74656e6365207370656e64206566666f7274206261722062656e65666974",
                "efdee9564b60ab769e337c12ef27e5d20fa5c2e1951eda41dafa18be779a55c5"
            ),
            (
                "000000047363727562206775617264207377696d2063617463682072616e67652075706f6e206461776e20656e73757265207365676d656e7420616c7068612073656e74656e6365207370656e64206566666f7274206261722062656e65666974",
                "098d7080d6bfaf9a7b007e2aa91f3731c12498eff1a20c22e71692a008b0ffac"
            )
        ]
    )
    def test_raw_seed_for_0_1_2_3_4_nonces(self, hex_seed, raw_seed):
        from lunespy.utils.crypto.converters import hash_keccak256_blake2b32b, from_hex

        result: str = hash_keccak256_blake2b32b(from_hex(hex_seed)).encode('latin-1').hex()
        assert result == raw_seed


    @mark.parametrize(
        "raw_seed, hash_seed",
        [
            (
                "cc872e22459e5c220323651e07097a30252162075fa10152e1de0f9b9c8c358a",
                "a34211e1159080cbf115cdd1108adb9b323018d1e34f2368fc66d54a3fa51460"
            ),
            (
                "312a14407453264a7dc508b4daa627f521bac6cd817f4f0d816690d7b5806897",
                "9ec39e2bebaf5171478e8675e2f78cbd0956c1363b28643bd5ab087197f42b74"
            ),
            (
                "29201f71d95566db58d1e3886b32a7da0333217dd6f6f63b6b73790fe8971b9a",
                "3287a10f344eeab1ea6543c044ae687c1c9c17215176d2ff7f7f3b1894d7198d"
            ),
            (
                "efdee9564b60ab769e337c12ef27e5d20fa5c2e1951eda41dafa18be779a55c5",
                "44bcf98e997b77bb868b8ee090e960db764f03b3ac91bfbdebcde877b0374cc5"
            ),
            (
                "098d7080d6bfaf9a7b007e2aa91f3731c12498eff1a20c22e71692a008b0ffac",
                "b0844296190762a600795411a184cc3a13049ea11acd3fc6e6abdac7c7d91a66"
            )
        ]
    )
    def test_hash_seed_for_0_1_2_3_4_nonces(self, raw_seed, hash_seed):
        from lunespy.utils.crypto.converters import sha256, from_hex

        result: str = sha256(from_hex(raw_seed)).hex()
        assert result == hash_seed


    @mark.parametrize(
        "hash_seed, private_key",
        [
            (
                "a34211e1159080cbf115cdd1108adb9b323018d1e34f2368fc66d54a3fa51460",
                "a04211e1159080cbf115cdd1108adb9b323018d1e34f2368fc66d54a3fa51460"
            ),
            (
                "9ec39e2bebaf5171478e8675e2f78cbd0956c1363b28643bd5ab087197f42b74",
                "98c39e2bebaf5171478e8675e2f78cbd0956c1363b28643bd5ab087197f42b74"
            ),
            (
                "3287a10f344eeab1ea6543c044ae687c1c9c17215176d2ff7f7f3b1894d7198d",
                "3087a10f344eeab1ea6543c044ae687c1c9c17215176d2ff7f7f3b1894d7194d"
            ),
            (
                "44bcf98e997b77bb868b8ee090e960db764f03b3ac91bfbdebcde877b0374cc5",
                "40bcf98e997b77bb868b8ee090e960db764f03b3ac91bfbdebcde877b0374c45"
            ),
            (
                "b0844296190762a600795411a184cc3a13049ea11acd3fc6e6abdac7c7d91a66",
                "b0844296190762a600795411a184cc3a13049ea11acd3fc6e6abdac7c7d91a66"
            )
        ]
    )
    def test_generate_private_key_for_0_1_2_3_4_nonces(self, hash_seed, private_key):
        from lunespy.utils.crypto.converters import from_hex
        from axolotl_curve25519 import generatePrivateKey

        result: str = generatePrivateKey(from_hex(hash_seed)).hex()
        assert result == private_key


    @mark.parametrize(
        "private_key, public_key",
        [
            (
                "a04211e1159080cbf115cdd1108adb9b323018d1e34f2368fc66d54a3fa51460",
                "1c6924c7246f785f98d0d727a1474eedc8a047d1b1668caa38ce09d6e3267575"
            ),
            (
                "98c39e2bebaf5171478e8675e2f78cbd0956c1363b28643bd5ab087197f42b74",
                "8afbb187cc11d78b6b6ea39f4542e67d2e5a9bfb704c50e2f69f00f718ccee7f"
            ),
            (
                "3087a10f344eeab1ea6543c044ae687c1c9c17215176d2ff7f7f3b1894d7194d",
                "538f37cfbc714c62bcbb150679ed72573877f77b6beb7f5d6f7db1feea07b666"
            ),
            (
                "40bcf98e997b77bb868b8ee090e960db764f03b3ac91bfbdebcde877b0374c45",
                "18111dd232ddce7cf1a96d74cae4f10a42eb1fb34a3ddc726e111909a14e1873"
            ),
            (
                "b0844296190762a600795411a184cc3a13049ea11acd3fc6e6abdac7c7d91a66",
                "c7331af1e72a2ea9019be355a04c7bbfb59f3042d19ca24feb42c7d32315a138"
            )
        ]
    )
    def test_generate_public_key_for_0_1_2_3_4_nonces(self, private_key, public_key):
        from lunespy.utils.crypto.converters import from_hex
        from axolotl_curve25519 import generatePublicKey

        result: str = generatePublicKey(from_hex(private_key)).hex()
        assert result == public_key


    @mark.parametrize(
        "public_key, address",
        [
            (
                "1c6924c7246f785f98d0d727a1474eedc8a047d1b1668caa38ce09d6e3267575",
                "01312c2e5258dc5bccbb5c535944270f73b98f9739266329c8c0"
            ),
            (
                "8afbb187cc11d78b6b6ea39f4542e67d2e5a9bfb704c50e2f69f00f718ccee7f",
                "0131640f230f396c4cf3f6ce7a6156387d52929902bff77423d8"
            ),
            (
                "538f37cfbc714c62bcbb150679ed72573877f77b6beb7f5d6f7db1feea07b666",
                "013146cc1229797733630bfa38be72ca6df585e8521fd44b5738"
            ),
            (
                "18111dd232ddce7cf1a96d74cae4f10a42eb1fb34a3ddc726e111909a14e1873",
                "0131842e3a128fd462b51805798d36909dac78ff9d43abb4d3b3"
            ),
            (
                "c7331af1e72a2ea9019be355a04c7bbfb59f3042d19ca24feb42c7d32315a138",
                "01317d211450834bfc6e0024549218833debf377968a4eca4b2d"
            )
        ]
    )
    def test_generate_mainnet_version_1_address_for_0_1_2_3_4_nonces(self, public_key, address):
        from lunespy.client.account.utils import address_generator
        from lunespy.utils.crypto.converters import from_hex

        result = address_generator(from_hex(public_key), chain_id="1", address_version=chr(1)).hex()
        assert result == address


    @mark.parametrize(
        "public_key, address",
        [
            (
                "1c6924c7246f785f98d0d727a1474eedc8a047d1b1668caa38ce09d6e3267575",
                "0b312c2e5258dc5bccbb5c535944270f73b98f973926fe567f22"
            ),
            (
                "8afbb187cc11d78b6b6ea39f4542e67d2e5a9bfb704c50e2f69f00f718ccee7f",
                "0b31640f230f396c4cf3f6ce7a6156387d52929902bfabb54a49"
            ),
            (
                "538f37cfbc714c62bcbb150679ed72573877f77b6beb7f5d6f7db1feea07b666",
                "0b3146cc1229797733630bfa38be72ca6df585e8521f152bafba"
            ),
            (
                "18111dd232ddce7cf1a96d74cae4f10a42eb1fb34a3ddc726e111909a14e1873",
                "0b31842e3a128fd462b51805798d36909dac78ff9d43f2b8e319"
            ),
            (
                "c7331af1e72a2ea9019be355a04c7bbfb59f3042d19ca24feb42c7d32315a138",
                "0b317d211450834bfc6e0024549218833debf377968ab695eaf7"
            )
        ]
    )
    def test_generate_mainnet_version_2_address_for_0_1_2_3_4_nonces(self, public_key, address):
        from lunespy.client.account.utils import address_generator
        from lunespy.utils.crypto.converters import from_hex

        result = address_generator(from_hex(public_key), chain_id="1", address_version=chr(11)).hex()
        assert result == address


    @mark.parametrize(
        "public_key, address",
        [
            (
                "1c6924c7246f785f98d0d727a1474eedc8a047d1b1668caa38ce09d6e3267575",
                "01302c2e5258dc5bccbb5c535944270f73b98f973926d12b5dc0"
            ),
            (
                "8afbb187cc11d78b6b6ea39f4542e67d2e5a9bfb704c50e2f69f00f718ccee7f",
                "0130640f230f396c4cf3f6ce7a6156387d52929902bfdc19cb02"
            ),
            (
                "538f37cfbc714c62bcbb150679ed72573877f77b6beb7f5d6f7db1feea07b666",
                "013046cc1229797733630bfa38be72ca6df585e8521f42414610"
            ),
            (
                "18111dd232ddce7cf1a96d74cae4f10a42eb1fb34a3ddc726e111909a14e1873",
                "0130842e3a128fd462b51805798d36909dac78ff9d43e66f1ea7"
            ),
            (
                "c7331af1e72a2ea9019be355a04c7bbfb59f3042d19ca24feb42c7d32315a138",
                "01307d211450834bfc6e0024549218833debf377968a9619b6bb"
            )
        ]
    )
    def test_generate_testnet_version_1_address_for_0_1_2_3_4_nonces(self, public_key, address):
        from lunespy.client.account.utils import address_generator
        from lunespy.utils.crypto.converters import from_hex

        result = address_generator(from_hex(public_key), chain_id="0", address_version=chr(1)).hex()
        assert result == address


    @mark.parametrize(
        "public_key, address",
        [
            (
                "1c6924c7246f785f98d0d727a1474eedc8a047d1b1668caa38ce09d6e3267575",
                "0b302c2e5258dc5bccbb5c535944270f73b98f97392650423846"
            ),
            (
                "8afbb187cc11d78b6b6ea39f4542e67d2e5a9bfb704c50e2f69f00f718ccee7f",
                "0b30640f230f396c4cf3f6ce7a6156387d52929902bfbb9f09d2"
            ),
            (
                "538f37cfbc714c62bcbb150679ed72573877f77b6beb7f5d6f7db1feea07b666",
                "0b3046cc1229797733630bfa38be72ca6df585e8521fb809f734"
            ),
            (
                "18111dd232ddce7cf1a96d74cae4f10a42eb1fb34a3ddc726e111909a14e1873",
                "0b30842e3a128fd462b51805798d36909dac78ff9d43136b6231"
            ),
            (
                "c7331af1e72a2ea9019be355a04c7bbfb59f3042d19ca24feb42c7d32315a138",
                "0b307d211450834bfc6e0024549218833debf377968ab7dbdb69"
            )
        ]
    )
    def test_generate_testnet_version_2_address_for_0_1_2_3_4_nonces(self, public_key, address):
        from lunespy.client.account.utils import address_generator
        from lunespy.utils.crypto.converters import from_hex

        result = address_generator(from_hex(public_key), chain_id="0", address_version=chr(11)).hex()
        assert result == address
