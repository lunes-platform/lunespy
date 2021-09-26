from lunespy.client.transactions.issue import IssueToken
from lunespy.client.wallet import Account

def test_without_name_ready_failed_successful():
    """
        without a name parameter:
            - should be return False for Token.ready
            - else should be return True
    """
    # Failed
    creator = Account()
    tx = IssueToken(creator, quantity=1)
    assert tx.ready == False

    #Successful
    tx.issue_data['name'] = 'newToken'
    assert tx.ready == True

def test_without_quantity_ready_failed_successful():
    """
        without a quantity parameter:
            - should be return False for IssueToken.ready
            - else should be return True
    """
    # Failed
    creator = Account()
    tx = IssueToken(creator, name='test')
    assert tx.ready == False

    #Successful
    tx.issue_data['quantity'] = 1
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a creator, receiver, amount:
            - should be return all keys of offline-transaction for IssueToken.transaction  
    """
    creator = Account()
    offline_transaction = [
        'ready',
        'type',
        'senderPublicKey',
        'signature',
        'timestamp',
        'fee',

        'description',
        'reissuable',
        'decimals',
        'quantity',
        'name'
    ]

    tx = IssueToken(creator, name='test', quantity=10)
    response = tx.transaction
    print(response)

    assert response['ready'] == True
    assert list(response.keys()) == offline_transaction



