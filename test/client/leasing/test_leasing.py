from lunespy.client.transactions.leasing import CreateLeasing
from lunespy.client.wallet import Account


def test_without_leasing_ready_failed_successful():
    """
        without a leasing parameter or a leasing with character dont allow.
        should be return False for CreateLeasing.ready
        else should be return True
    """
    # Failed
    creator = Account()
    validator_address = Account()
    tx = CreateLeasing(creator, validator_address, amount=0)
    assert tx.ready == False

    #Successful
    tx.leasing_data['amount'] = 1
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a creator, validator_address, amount.
        should be return all keys of offline-transaction for CreateLeasing.transaction  
    """
    creator = Account()
    validator_address = Account().address
    offline_transaction = [
        'ready',
        'senderPublicKey',
        'signature',
        'recipient',
        'type',
        'timestamp',
        'fee',
        'amount',
    ]

    tx = CreateLeasing(creator, validator_address, amount=1)
    response = tx.transaction
    print(response)

    assert response['ready'] == True

    for i, j in zip(offline_transaction, response.keys()):
        assert i == j
