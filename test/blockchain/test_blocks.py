from lunespy.blockchain.blocks import blocks_generated_by_specified_address
from lunespy.blockchain.blocks import block_from_height
from lunespy.blockchain.blocks import range_block
from lunespy.blockchain.blocks import last_block
from pytest import mark


@mark.blocks
@mark.requests
def test_block_from_height():
    assert type(block_from_height(1)['version']) == int

@mark.blocks
@mark.requests
def test_block_from_height_wrong_height():
    assert block_from_height(98231472)['status'] == 'error'


@mark.blocks
@mark.requests
def test_range_block():
    assert range_block(1, 5) != []


@mark.blocks
@mark.requests
def test_range_block_with_the_first_block_bigger_than_second():
    assert type(range_block(5, 1)) == type(None)


@mark.blocks
@mark.requests
def test_range_block_with_a_bigger_sequence_requested():
    assert type(range_block(10, 21844123)) == type(None)


@mark.blocks
@mark.requests
def test_last_block():
    assert last_block() != {}


@mark.blocks
@mark.requests
def test_blocks_generated_by_specified_address():
    assert blocks_generated_by_specified_address('37nX3hdCt1GWeSsAMNFmWgbQWZZhbvBG3mX', 1766888, 1766889) != []
