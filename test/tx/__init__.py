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
