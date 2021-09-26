from lunespy.client.transactions.alias import CreateAlias
from lunespy.client.wallet import Account


def test_without_alias_ready_failed_successful():
    """
        without a alias parameter or a alias with character dont allow.
        should be return False for CreateAlias.ready
        else should be return True
    """
    # Failed
    creator = Account()
    tx = CreateAlias(creator)
    assert tx.ready == False

    # Failed
    tx.alias_data['alias'] = 'Bahia'
    assert tx.ready == False

    #Successful
    tx.alias_data['alias'] = 'bahia'
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a creator, receiver, amount.
        should be return all keys of offline-transaction for CreateAlias.transaction  
    """
    creator = Account()
    offline_transaction = [
        'ready',
        'type',
        'senderPublicKey',
        'signature',
        'timestamp',
        'fee',

        'alias'
    ]

    tx = CreateAlias(creator, alias='bahia')
    response = tx.transaction
    print(response)

    assert response['ready'] == True
    assert list(response.keys()) == offline_transaction
