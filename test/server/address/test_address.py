from lunespy.server.address import balance_for_especify_asset_of_address
from lunespy.server.address import aliases_associated_with_an_address
from lunespy.server.address import address_associated_with_an_alias
from lunespy.server.address import balance_all_assets_of_address
from lunespy.server.address import leasing_active_by_address
from lunespy.server.address import address_of_node_from_url
from lunespy.server.address import balance_of_address
from lunespy.server.address import asset_distribution
from pytest import mark


@mark.requests
def test_asset_distribuition():
    assert asset_distribution('9rwhz45pXYRdbHTek28HK87RHCEG1BKP4Eu2FnpAVsC8', 'http://lunesnode.lunes.io')['response'] != {}


@mark.requests
def test_addres_associated_with_an_alias():
    assert address_associated_with_an_alias('gabriel', 'http://lunesnode.lunes.io')['status'] == 'ok'


@mark.requests
def test_balance_all_assets_of_address():
    assert balance_all_assets_of_address('37qrqmmQ8jwJJB2aXMnXt98kiwezyzb5ww7', 'http://lunesnode.lunes.io')['status'] == 'ok'


@mark.requests
def test_balance_for_especify_asset_of_address():
    assert balance_for_especify_asset_of_address('37qrqmmQ8jwJJB2aXMnXt98kiwezyzb5ww7', '9rwhz45pXYRdbHTek28HK87RHCEG1BKP4Eu2FnpAVsC8', 'http://lunesnode.lunes.io')['status'] == 'ok'


@mark.requests
def test_balance_of_address():
    assert balance_of_address('37qrqmmQ8jwJJB2aXMnXt98kiwezyzb5ww7', 'http://lunesnode.lunes.io')["response"]["balance"] == int


@mark.requests
def test_balance_of_address():
    assert balance_of_address('37qrqmmQ8jwJJB2aXMnXt98kiwezyzb5ww7', 'http://lunesnode.lunes.io')["status"] == "ok"


@mark.requests
def test_balance_of_address():
    assert type(balance_of_address('37qrqmmQ8jwJJB2aXMnXt98kiwezyzb5ww7', 'http://lunesnode.lunes.io')) == dict


@mark.requests
def test_balance_of_address():
    assert len(balance_of_address('37qrqmmQ8jwJJB2aXMnXt98kiwezyzb5ww7', 'http://lunesnode.lunes.io')["response"].keys()) >  1


@mark.requests
def test_leasing_active_by_address():
    full_url = f'http://lunesnode.lunes.io/leasing/active/37nX3hdCt1GWeSsAMNFmWgbQWZZhbvBG3mX'
    assert leasing_active_by_address('37nX3hdCt1GWeSsAMNFmWgbQWZZhbvBG3mX', 'http://lunesnode.lunes.io')['response'] != {full_url: []}


@mark.requests
def test_address_of_node_from_url():
    assert address_of_node_from_url('http://lunesnode.lunes.io')['status'] == 'ok'


@mark.requests
def test_aliases_associated_with_an_address():
    assert aliases_associated_with_an_address('3868pVhDQAs2v5MGxNN75CaHzyx1YV8TivM', 'http://lunesnode.lunes.io')['response'] != []

