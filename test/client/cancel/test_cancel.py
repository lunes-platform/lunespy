from lunespy.client.transactions.cancel import CancelLease
from lunespy.client.wallet import Account


def test_without_lease_ready_failed_successful():
    """
        without a lease parameter or a lease with character dont allow.
        should be return False for CancelLease.ready
        else should be return True
    """
    # Failed
    staker = Account()
    tx = CancelLease(staker)
    assert tx.ready == False

    #Successful
    tx.cancel_data['lease_id'] = 'tx'
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a staker, validator_address, amount.
        should be return all keys of offline-transaction for CancelLease.transaction  
    """
    staker = Account()
    offline_transaction = [
        'ready',
        'type',
        'senderPublicKey',
        'signature',
        'timestamp',
        'fee',

        'leaseId'
    ]

    tx = CancelLease(staker, lease_id='tx')
    response = tx.transaction

    assert response['ready'] == True
    assert list(response.keys()) == offline_transaction

