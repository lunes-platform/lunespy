from lunespy.client.transactions.alias import CreateAlias
from lunespy.client.wallet import Account


def test_without_alias_ready_failed_successful():
    """
        without a alias parameter or a alias with character dont allow.
        should be return False for CreateAlias.ready
        else should be return True
    """
    # Failed
    sender = Account()
    tx = CreateAlias(sender)
    assert tx.ready == False

    # Failed
    tx.alias_data['alias'] = 'Bahia'
    assert tx.ready == False

    #Successful
    tx.alias_data['alias'] = 'bahia'
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a sender, receiver, amount.
        should be return all keys of offline-transaction for CreateAlias.transaction  
    """
    sender = Account()
    offline_transaction = [
        'ready',
        'type',
        'senderPublicKey',
        'signature',
        'timestamp',
        'fee',

        'alias'
    ]

    tx = CreateAlias(sender, alias='bahia')
    response = tx.transaction
    print(response)

    assert response['ready'] == True
    assert list(response.keys()) == offline_transaction
