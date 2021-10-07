from lunespy.client.wallet import Account
from lunespy.client.wallet.errors import InvalidChainAddress
from pytest import raises

def test_seed():
    """
        this seed "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit":
            - should returns this mainnet_address: "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"
            - should returns this testnet_address: "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"
    """
    seed = "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"

    mainnet = Account(seed=seed, network='mainnet')
    assert mainnet.address == "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"

    testnet = Account(seed=seed, network='testnet')
    assert testnet.address == "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"

def test_private_key():
    """ 
        this private_key "BnafXBSq1VDUdZ1nSjJoxhnQdBv2hk3o6dbV49TD1bzo":
            - should returns this mainnet_address: "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"
            - should returns this testnet_address: "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"
    """
    private_key = "BnafXBSq1VDUdZ1nSjJoxhnQdBv2hk3o6dbV49TD1bzo"

    mainnet = Account(private_key=private_key, network='mainnet')
    assert mainnet.address == "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"

    testnet = Account(private_key=private_key, network='testnet')
    assert testnet.address == "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"

def test_public_key():
    """
        this public_key "2uuQVr3B5aGgvSJ5BMCw4Cd19tdYdnMGoYnji99aPde4":
            - should returns this mainnet_address: "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"
            - should returns this testnet_address: "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"
    """
    public_key = "2uuQVr3B5aGgvSJ5BMCw4Cd19tdYdnMGoYnji99aPde4"

    mainnet = Account(public_key=public_key, network='mainnet')
    assert mainnet.address == "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"

    testnet = Account(public_key=public_key, network='testnet')
    assert testnet.address == "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"

def test_address_mainnet():
    """
        this address "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj":
            - should return this mainet_address: "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"
            - should return this testnet_address: Error InvalidChainAddress
    """
    address = "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"

    mainnet = Account(address=address, network='mainnet')
    assert mainnet.address == "37o7aY3eZZTXmzrDa5e4Wj3Z4ZZuyV42Aaj"

    with raises(InvalidChainAddress):
        Account(address=address, network='testnet')
    
def test_address_testnet():
    """
        this address "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u":
            - should return this mainet_address: Error InvalidChainAddress
            - should return this testnet_address: "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"
    """
    from lunespy.client.wallet.errors import InvalidChainAddress

    address = "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"

    testnet = Account(address=address, network='testnet')
    assert testnet.address == "37PmyYwMGrH4uBR5V4DjCEvHGw4f2pdXW5u"

    with raises(InvalidChainAddress):
            Account(address=address, network='mainnet')

def test_seed_with_nonce_1():
    """
        this seed "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"
        with nonce 1:
            - should return this mainet_private_key: "BHKyaXmhajKVNfyHszvFbeQvK8zMTHTMMCWjLxUmcwLw"
            - should return this mainet_public_key: "AMXrxLv1wtnr8EWxvk1hcuujTzh56SiuPGBQqho2ocW2"
            - should return this mainet_address: "37tD32367v1fiWgW8waw3QTdYTKKGrCV3zw"
    """    
    seed = "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"
    nonce = 1
    wallet = Account(seed=seed, nonce=nonce, network='mainnet')
    assert wallet.private_key == "BHKyaXmhajKVNfyHszvFbeQvK8zMTHTMMCWjLxUmcwLw"
    assert wallet.public_key == "AMXrxLv1wtnr8EWxvk1hcuujTzh56SiuPGBQqho2ocW2"
    assert wallet.address == "37tD32367v1fiWgW8waw3QTdYTKKGrCV3zw"

def test_seed_with_nonce_2():
    """
        this seed "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"
        with nonce 1
            - should return this mainet_private_key: "4GSXCGMEvAPrhhTSUHfUfxfieqgpcJN8wsgUYdp82jJL"
            - should return this mainet_public_key: "6dBW6ZD1GGomCjtjngvRHUJWqixoqk7PpCR6Yv8VAi6y"
            - should return this mainet_address: "37qYK5eRJEr8a38hUXmxYv9aoQ8NpXH7Aqd"
    """
    seed = "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"
    nonce = 2
    wallet = Account(seed=seed, nonce=nonce, network='mainnet')
    assert wallet.private_key == "4GSXCGMEvAPrhhTSUHfUfxfieqgpcJN8wsgUYdp82jJL"
    assert wallet.public_key == "6dBW6ZD1GGomCjtjngvRHUJWqixoqk7PpCR6Yv8VAi6y"
    assert wallet.address == "37qYK5eRJEr8a38hUXmxYv9aoQ8NpXH7Aqd"

def test_seed_with_nonce_3():
    """
        this seed "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"
        with nonce 1
            - should return this mainet_private_key: "5MiDw2Sa8PhvJLBfPg272jhLoZsBbZ3uT7p4fNB6X8DJ"
            - should return this mainet_public_key: "2cwvWpBCtgZURG5WEwzpmnJhzhtNN8T6jJH6G6qamfG6"
            - should return this mainet_address: "37w8stLd9JQwUKBrBUQr1VryJuhS3RWqEen"
    """
    seed = "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit"
    nonce = 3
    wallet = Account(seed=seed, nonce=nonce, network='mainnet')
    assert wallet.private_key == "5MiDw2Sa8PhvJLBfPg272jhLoZsBbZ3uT7p4fNB6X8DJ"
    assert wallet.public_key == "2cwvWpBCtgZURG5WEwzpmnJhzhtNN8T6jJH6G6qamfG6"
    assert wallet.address == "37w8stLd9JQwUKBrBUQr1VryJuhS3RWqEen"


def test_all_attributes_of_account():
    """
        this attributes below:
            - should be:
                seed -> "oak display outdoor barely friend spike video defense proud cave lamp oxygen problem traffic exercise"
                hash_seed -> "L79j8bS2SfpjpWZS8oJaqYdczKYun5F1JuQo9uBnAKn97REWjJ2SeoHeEG8Nn6xk7qLaGEHWdtHjVf3emRsuumVKdpaa2zBTRptucQqJ9cs6XDiNsV8XDGh5e1buQmrG6gQFhnWCix"
                nonce -> 0
                network -> 'testnet'
                network_id -> '0'
                private_key -> "7VAsqDQ9PadMbG21fHkbtVHyteuPT26ZspaDQr37scUZ"
                public_key -> "B226T1TgGB23Nc6L2jmowtSWY14dwG9wWEVhpBmBzPkr"
                address -> "37iwu4YZc5umF7u24kMDzgYN55PQy6x3NTm"
    """
    seed = "oak display outdoor barely friend spike video defense proud cave lamp oxygen problem traffic exercise"
    hash_seed = "L79j8bS2SfpjpWZS8oJaqYdczKYun5F1JuQo9uBnAKn97REWjJ2SeoHeEG8Nn6xk7qLaGEHWdtHjVf3emRsuumVKdpaa2zBTRptucQqJ9cs6XDiNsV8XDGh5e1buQmrG6gQFhnWCix"
    nonce = 0
    network = 'testnet'
    network_id = '0'
    private_key = "7VAsqDQ9PadMbG21fHkbtVHyteuPT26ZspaDQr37scUZ"
    public_key = "B226T1TgGB23Nc6L2jmowtSWY14dwG9wWEVhpBmBzPkr"
    address = "37iwu4YZc5umF7u24kMDzgYN55PQy6x3NTm"

    wallet = Account(seed=seed, network='testnet')

    assert wallet.private_key == private_key
    assert wallet.network_id == network_id
    assert wallet.public_key == public_key
    assert wallet.hash_seed == hash_seed
    assert wallet.network == network
    assert wallet.address == address
    assert wallet.nonce == nonce
    assert wallet.seed == seed
     