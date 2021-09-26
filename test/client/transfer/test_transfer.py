from lunespy.client.transactions.transfer import TransferToken
from lunespy.client.wallet import Account

def test_without_amount_ready_failed_successful():
    """
        with a sender, receiver and amount:
            - should be return True for TransaferToken.ready
        without a amount parameter:
            - should be return False for TransaferToken.ready
    """
    # Failed
    sender = Account()
    receiver = Account()
    tx = TransferToken(sender, receiver)
    assert tx.ready == False

    # Successful
    tx.transfer_data['amount'] = 10
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a sender, receiver, amount:
            - should be return all keys of offline_transaction for TransaferToken.transaction  
    """
    sender = Account()
    receiver = Account()
    offline_transaction = [
        'ready',
        'type',
        'senderPublicKey',
        'signature',
        'timestamp',
        'fee',

        'recipient',
        'feeAsset',
        'assetId',
        'amount']
    tx = TransferToken(sender, receiver, amount=10)
    response = tx.transaction

    assert response['ready'] == True
    assert list(response.keys()) == offline_transaction
