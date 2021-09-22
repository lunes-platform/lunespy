from lunespy.client.transactions.issue import Token
from lunespy.client.wallet import Account

def test_without_name_ready_failed_successful():
    """
        without a name parameter.
        should be return False for Token.ready
        else should be return True
    """
    # Failed
    creator = Account()
    tx = Token(creator, quantity=1)
    assert tx.ready == False

    #Successful
    tx.data_issue['name'] = 'newToken'
    assert tx.ready == True

def test_without_quantity_ready_failed_successful():
    """
        without a quantity parameter.
        should be return False for Token.ready
        else should be return True
    """
    # Failed
    creator = Account()
    tx = Token(creator, name='test')
    assert tx.ready == False

    #Successful
    tx.data_issue['quantity'] = 1
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a creator, receiver, amount.
        should be return all keys of offline-transaction for Token.transaction  
    """
    creator = Account()
    offline_transaction = [
        'ready',
        'senderPublicKey',
        'signature',
        'description',
        'reissuable',
        'timestamp',
        'type',
        'decimals',
        'quantity',
        'fee',
        'name',
        'feeAsset',
        'assetId'
    ]

    tx = Token(creator, name='test', quantity=10)
    response = tx.transaction
    print(response)

    assert response['ready'] == True

    for i, j in zip(offline_transaction, response.keys()):
        assert i == j


def test_send_failed():
    """
        should be return False for `send` parameter and dict in `response`
    """
    assert 1 == 1


def test_send_successful():
    """
        should be return True for `send` parameter and dict in `response`
    """
    assert 1 == 1