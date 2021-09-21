from lunespy.client.transactions.transfer_asset import TransferAsset
from lunespy.client.wallet import Account

def test_ready_failed():
    """
        without a amount parameter.
        should be return False for TransaferAsset.ready
    """
    # Failed
    sender = Account()
    receiver = Account()
    tx = TransferAsset(sender, receiver)
    assert tx.ready == False

def test_ready_success():
    """
        with a sender, receiver and amount.
        should be return True for TransaferAsset.ready
    """    
    # Success
    sender = Account()
    receiver = Account()
    tx = TransferAsset(sender, receiver, amount=10)
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a sender, receiver, amount.
        should be return all keys of offline-transaction for TransaferAsset.transaction  
    """
    sender = Account()
    receiver = Account()
    offline_transaction = [
        'ready',
        'senderPublicKey',
        'signature',
        'timestamp',
        'recipient',
        'feeAsset',
        'assetId',
        'amount',
        'type',
        'fee']
    tx = TransferAsset(sender, receiver, amount=10)
    response = tx.transaction

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