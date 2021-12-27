from lunespy.server.blocks import block_from_height
from lunespy.server.blocks import range_block
from lunespy.server.blocks import last_block
from lunespy.server.blocks import blocks_generated_by_specified_address



def test_block_from_height():
    assert block_from_height(1,'http://lunesnode.lunes.io')['status'] == 'ok'


def test_range_block():
    assert range_block(1,5, 'http://lunesnode.lunes.io')['status'] == 'ok'


def test_last_block():
    assert last_block('http://lunesnode.lunes.io')['status'] == 'ok'


def test_blocks_generated_by_specified_address():
    assert blocks_generated_by_specified_address('37nX3hdCt1GWeSsAMNFmWgbQWZZhbvBG3mX', 1766888, 1766889, 'http://lunesnode.lunes.io')['response'] != []
