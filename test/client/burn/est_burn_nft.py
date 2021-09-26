from lunespy.client.transactions.burn import BurnNFT
from lunespy.client.wallet import Account


def test_without_asset_id_ready_failed_successful():
    """
        without a asset_id parameter:
            - should be return False for BurnNFT.ready
            - else should be return True
    """
    # Failed
    burner = Account()
    tx = BurnNFT(burner, quantity=1)
    assert tx.ready == False

    #Successful
    tx.burn_data['asset_id'] = '7npqMwVEAZ9yGgoRB8AwfHXEkCumWgiqdYr8yeTze7Pp'
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a burner, asset_id and quantity:
            - should be return all keys of offline-transaction for BurnNFT.transaction  
    """
    burner = Account()
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

    tx = BurnNFT(burner, asset_id='test', quantity=10)
    response = tx.transaction
    print(response)

    assert response['ready'] == True
    assert list(response.keys()) == offline_transaction
