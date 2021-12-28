from lunespy.server.nodes import version_all_lunes_node_conected
from lunespy.server.nodes import all_node_conected_in_node_url
from lunespy.server.nodes import node_version
from pytest import mark


@mark.requests
def test_all_node_conected_in_node_url():
    assert all_node_conected_in_node_url('http://lunesnode.lunes.io')['status'] == 'ok'


@mark.requests
def test_node_version():
    assert node_version('http://lunesnode.lunes.io')['status'] == 'ok'


@mark.requests
def test_version_all_lunes_node_conected():
    assert version_all_lunes_node_conected('http://lunesnode.lunes.io')['status'] == 'ok'
