from lunespy.client.transactions.lease import CreateLease
from lunespy.client.wallet import Account

def test_without_lease_ready_failed_successful():
    """
        with amount parameter iquals or less than 0:
            - should be return False for CreateLease.ready
            - else should be return True
    """
    # Failed
    sender = Account()
    validator_address = Account()
    tx = CreateLease(sender, validator_address, amount=0)
    assert tx.ready == False

    #Successful
    tx.lease_data['amount'] = 1
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a sender, validator_address, amount:
            - should be return all keys of offline-transaction for CreateLease.transaction  
    """
    sender = Account()
    validator_address = Account().address
    offline_transaction = [
        'ready',
        'type',
        'senderPublicKey',
        'signature',
        'timestamp',
        'fee',

        'recipient',
        'amount'
    ]

    tx = CreateLease(sender, validator_address, amount=1)
    response = tx.transaction
    print(response)

    assert response['ready'] == True
    assert list(response.keys()) == offline_transaction

