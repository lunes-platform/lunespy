from lunespy.client.transactions.cancel import CancelLease
from lunespy.client.wallet import Account


def test_without_lease_ready_failed_successful():
    """
        without a lease parameter or a lease with character dont allow.
        should be return False for CancelLease.ready
        else should be return True
    """
    # Failed
    sender = Account()
    tx = CancelLease(sender)
    assert tx.ready == False

    #Successful
    tx.cancel_data['lease_tx_id'] = 'tx'
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a sender, validator_address, amount.
        should be return all keys of offline-transaction for CancelLease.transaction  
    """
    sender = Account()
    offline_transaction = [
        'ready',
        'type',
        'senderPublicKey',
        'signature',
        'timestamp',
        'fee',

        'leaseId'
    ]

    tx = CancelLease(sender, lease_tx_id='tx')
    response = tx.transaction

    assert response['ready'] == True
    assert list(response.keys()) == offline_transaction

