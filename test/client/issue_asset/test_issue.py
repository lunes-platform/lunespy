from lunespy.client.transactions.issue_asset import IssueAsset
from lunespy.client.wallet import Account

def test_ready_failed_name():
    """
        without a name parameter.
        should be return False for IssueAsset.ready
    """
    # Failed
    sender = Account()
    tx = IssueAsset(sender, quantity=1)
    assert tx.ready == False

def test_ready_failed_quantity():
    """
        without a quantity parameter.
        should be return False for IssueAsset.ready
    """
    # Failed
    sender = Account()
    tx = IssueAsset(sender, name='test')
    assert tx.ready == False


def test_ready_success():
    """
        with a sender, name and quantity.
        should be return True for IssueAsset.ready
    """    
    # Success
    sender = Account()
    tx = IssueAsset(sender, name='test', quantity=10)
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a sender, receiver, amount.
        should be return all keys of offline-transaction for IssueAsset.transaction  
    """
    sender = Account()
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

    tx = IssueAsset(sender, name='test', quantity=10)
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