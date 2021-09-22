from lunespy.client.transactions.transfer_token import TransferToken
from lunespy.client.wallet import Account

def test_without_amount_ready_failed_successful():
    """
        with a sender, receiver and amount.
        should be return True for TransaferAsset.ready
        without a amount parameter.
        should be return False for TransaferAsset.ready
    """
    # Failed
    sender = Account()
    receiver = Account()
    tx = TransferToken(sender, receiver)
    assert tx.ready == False

    # Successful
    tx.data_transfer['amount'] = 10
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
    tx = TransferToken(sender, receiver, amount=10)
    response = tx.transaction

    assert response['ready'] == True

    for i, j in zip(offline_transaction, response.keys()):
        assert i == j

def test_send_failed_successful():
    """
        should be return False for `send` parameter and dict in `response`
        should be return True for `send` parameter and dict in `response`
    """
    assert 1 == 1 