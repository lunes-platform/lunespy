from lunespy.blockchain.nodes import version_all_lunes_node_conected
from lunespy.blockchain.nodes import all_peers_conected_in_node_url
from lunespy.blockchain.nodes import node_version
from pytest import mark


@mark.nodes
@mark.requests
def test_all_peers_conected_in_node_url():
    assert all_peers_conected_in_node_url() != {}


@mark.nodes
@mark.requests
def test_node_version():
    assert type(node_version()['version']) == str


@mark.nodes
@mark.requests
def test_version_all_lunes_node_conected():
    assert version_all_lunes_node_conected() != {}
