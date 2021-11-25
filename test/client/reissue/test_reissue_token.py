from lunespy.client.transactions.reissue import ReissueToken
from lunespy.client.wallet import Account


def test_token_without_asset_id_ready_failed_successful():
    """
        without a asset_id parameter:
            - should be return False for ReissueToken.ready
            - else should be return True
    """
    # Failed
    sender = Account()
    tx = ReissueToken(sender, quantity=1)
    assert tx.ready == False

    #Successful
    tx.reissue_data['asset_id'] = '7npqMwVEAZ9yGgoRB8AwfHXEkCumWgiqdYr8yeTze7Pp'
    assert tx.ready == True


def test_token_transaction_full_data():
    """
        with a sender, asset_id and quantity:
            - should be return all keys of offline-transaction for ReissueToken.transaction  
    """
    sender = Account()
    offline_transaction = [
        'ready',
        'type',
        'senderPublicKey',
        'signature',
        'timestamp',
        'fee',

        'assetId',
        'reissuable',
        'quantity',
    ]

    tx = ReissueToken(sender, asset_id='test', quantity=10)
    response = tx.transaction
    print(response)

    assert response['ready'] == True
    assert list(response.keys()) == offline_transaction
