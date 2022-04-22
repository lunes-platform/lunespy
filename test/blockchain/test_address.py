from typing import Type
from lunespy.blockchain.address import balance_for_especify_asset_of_address
from lunespy.blockchain.address import aliases_associated_with_an_address
from lunespy.blockchain.address import address_associated_with_an_alias
from lunespy.blockchain.address import balance_all_assets_of_address
from lunespy.blockchain.address import leasing_active_by_address
from lunespy.blockchain.address import address_of_node_from_url
from lunespy.blockchain.address import balance_of_address
from lunespy.blockchain.address import asset_distribution
from pytest import mark


@mark.address
@mark.requests
def test_address_associated_with_an_alias():
    assert type(address_associated_with_an_alias('gabriel')['address']) == str


@mark.address
@mark.requests
def test_address_associated_with_an_alias_with_wrong_alias():
    assert type(address_associated_with_an_alias('jor4ge')) == type(None)


@mark.address
@mark.requests
def test_asset_distribuition():
    assert asset_distribution('9rwhz45pXYRdbHTek28HK87RHCEG1BKP4Eu2FnpAVsC8') != {}


@mark.address
@mark.requests
def test_balance_all_assets_of_address():
    assert type(balance_all_assets_of_address('37qrqmmQ8jwJJB2aXMnXt98kiwezyzb5ww7')['address']) == str


@mark.address
@mark.requests
def test_balance_all_assets_of_wrong_address():
    assert type(balance_all_assets_of_address('37qrqmmQ8jwJJBnXt98kiwezyzb5ww7')) == type(None)


@mark.address
@mark.requests
def test_balance_for_especify_asset_of_address():
    assert type(balance_for_especify_asset_of_address('37qrqmmQ8jwJJB2aXMnXt98kiwezyzb5ww7', '9rwhz45pXYRdbHTek28HK87RHCEG1BKP4Eu2FnpAVsC8')['address']) == str


@mark.address
@mark.requests
def test_balance_for_especify_asset_of_address_with_a_wrong_address():
    assert type(balance_for_especify_asset_of_address('37qrqmmQ8jwJ2aXMt98kiwezyzb5ww7', '9rwhz45pXYRdbHTek28HK87RHCEG1BKP4Eu2FnpAVsC8')) == type(None)


@mark.address
@mark.requests
def test_balance_for_especify_asset_of_address_with_a_wrong_asset_id():
    assert type(balance_for_especify_asset_of_address('37qrqmmQ8jwJJB2aXMnXt98kiwezyzb5ww7', '9rwhz45pXYRdbHTek87RHCEG1BKP4Eu2FnpAVsC8')['balance']) == type(0)


@mark.address
@mark.requests
def test_balance_of_address_response_type():
    assert type(balance_of_address('37qrqmmQ8jwJJB2aXMnXt98kiwezyzb5ww7')["balance"]) == int


@mark.address
@mark.requests
def test_balance_of_address_with_wrong_address():
    assert type(balance_of_address('37qrqmmQ8jwJJB2aXMnXt98kizb5ww7')) == type(None)


@mark.address
@mark.requests
def test_balance_of_address():
    assert type(balance_of_address('37qrqmmQ8jwJJB2aXMnXt98kiwezyzb5ww7')["address"]) == str


@mark.address
@mark.requests
def test_balance_of_address_type():
    assert type(balance_of_address('37qrqmmQ8jwJJB2aXMnXt98kiwezyzb5ww7')) == dict


@mark.address
@mark.requests
def test_leasing_active_by_address():
    full_url = f'http://lunesnode.lunes.io/leasing/active/37nX3hdCt1GWeSsAMNFmWgbQWZZhbvBG3mX'
    assert leasing_active_by_address('37nX3hdCt1GWeSsAMNFmWgbQWZZhbvBG3mX') != {full_url: []}


@mark.address
@mark.requests
def test_address_of_node_from_url():
    assert address_of_node_from_url() != []


@mark.address
@mark.requests
def test_aliases_associated_with_an_address():
    assert aliases_associated_with_an_address('3868pVhDQAs2v5MGxNN75CaHzyx1YV8TivM') != []
