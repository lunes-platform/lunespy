from lunespy.client.transactions.reissue import ReissueToken
from lunespy.client.wallet import Account


def test_without_asset_id_ready_failed_successful():
    """
        without a asset_id parameter.
        should be return False for ReissueToken.ready
        else should be return True
    """
    # Failed
    creator = Account()
    tx = ReissueToken(creator, quantity=1)
    assert tx.ready == False

    #Successful
    tx.reissue_data['asset_id'] = '7npqMwVEAZ9yGgoRB8AwfHXEkCumWgiqdYr8yeTze7Pp'
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a creator, receiver, amount.
        should be return all keys of offline-transaction for ReissueToken.transaction  
    """
    creator = Account()
    offline_transaction = [
        'ready',
        'senderPublicKey',
        'assetId',
        'type',
        'reissuable',
        'signature',
        'timestamp',
        'quantity',
        'fee'
    ]

    tx = ReissueToken(creator, asset_id='test', quantity=10)
    response = tx.transaction
    print(response)

    assert response['ready'] == True

    for i, j in zip(offline_transaction, response.keys()):
        assert i == j


# todo a mock
def test_send_failed_successful():
    """
        should be return False for `send` parameter and dict in `response`
        should be return True for `send` parameter and dict in `response`
    """
    assert 1 == 1