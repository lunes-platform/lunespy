from lunespy.client.transactions.burn import BurnToken
from lunespy.client.wallet import Account


def test_without_asset_id_ready_failed_successful():
    """
        without a asset_id parameter.
        should be return False for BurnToken.ready
        else should be return True
    """
    # Failed
    creator = Account()
    tx = BurnToken(creator, quantity=1)
    assert tx.ready == False

    #Successful
    tx.burn_data['asset_id'] = '7npqMwVEAZ9yGgoRB8AwfHXEkCumWgiqdYr8yeTze7Pp'
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a creator, receiver, amount.
        should be return all keys of offline-transaction for BurnToken.transaction  
    """
    creator = Account()
    offline_transaction = [
        'ready',
        'type',
        'senderPublicKey',
        'signature',
        'timestamp',
        'fee',
        
        'assetId',
        'quantity',
    ]

    tx = BurnToken(creator, asset_id='test', quantity=10)
    response = tx.transaction
    print(response)

    assert response['ready'] == True
    assert list(response.keys()) == offline_transaction
