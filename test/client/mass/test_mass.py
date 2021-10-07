from lunespy.client.transactions.mass import MassTransferToken
from lunespy.client.wallet.errors import InvalidChainAddress
from lunespy.client.wallet import Account
from pytest import raises

def test_ready_between_different_networks():
    """
        with a Account in network `mainnet`:
            should br return Error for receiver in network `testnet`
        else should be return True
    """
    sender_mainnet = Account(network='mainnet')    
    receivers_list = [
        { 'receiver': Account(network='testnet').address, 'amount': 100 }
        for tx in range(4)
    ]

    with raises(InvalidChainAddress):
        tx = MassTransferToken(sender_mainnet, receivers_list)
        tx.ready

    sender_testnet = Account(network='testnet')
    tx = MassTransferToken(sender_testnet, receivers_list)
    assert tx.ready == True


def test_ready_without_amount_failed_successful():
    """
        with amount less or iqual than 0:
            should be return `False` in MassTransferToken.ready
        else should be return True
    """

    # Failed
    sender = Account()
    receivers_list = [
        { 'receiver': Account().address, 'amount': tx }
        for tx in range(4)
    ]
    tx = MassTransferToken(sender, receivers_list)
    assert tx.ready == False

    # Successful
    tx.receivers_list[0]['amount'] = 10
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a sender, receiver, amount:
            - should be return all keys of offline_transaction for TransaferToken.transaction  
    """
    sender = Account()
    receivers_list = [
        { 'receiver': Account().address, 'amount': 10 }
        for tx in range(4)
    ]
    offline_transaction = [
        'ready',
        'type',
        'senderPublicKey',
        'signature',
        'timestamp',
        'fee',

        'version',
        'assetId',
        'transfers',
        'proofs'
    ]
    tx = MassTransferToken(sender, receivers_list)
    response = tx.transaction

    assert response['ready'] == True
    assert list(response.keys()) == offline_transaction
