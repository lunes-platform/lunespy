from lunespy.client.transactions.lunex import Lunex
from lunespy.client.wallet import Account
from lunespy.utils import now

def test_ready_to_lunex():
    sender = Account()
    data = {
        'side': 'sell',
        'bid_asset': 'asset_id',  # get_asset
        'ask_asset': 'asset_id',  # drop_asset
        'amount': 1,              # get_asset
        'price': 100,             # drop_asset
        'timestamp': int(now()),
        'expires': int(now()) + 30 * 86400,
    }

    tx = Lunex(sender, **data)
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a sender, receiver, amount:
            - should be return all keys of offline_transaction for TransaferToken.transaction  
    """
    sender = Account()
    data = {
        'side': 'sell',
        'bid_asset': 'asset_id',  # get_asset
        'ask_asset': 'asset_id',  # drop_asset
        'amount': 1,              # get_asset
        'price': 100,             # drop_asset
        'timestamp': int(now()),
        'expires': int(now()) + 30 * 86400,
    }
    tx = Lunex(sender, **data)
    response = tx.transaction

    assert True == response['ready'
]
    assert  [
        'ready',
        'type',
        'senderPublicKey',
        'signature',
        'timestamp',
        'matcherFee',

        'matcherPublicKey',
        'expiration',
        'orderType',
        'amount',
        'price',
        'assetPair'
    ] == list(response.keys())
    
    assert [
        'amountAsset',
        'priceAsset'
    ] == list(response['assetPair'].keys())