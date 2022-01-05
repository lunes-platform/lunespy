from lunespy.client.transactions.transfer import TransferToken
from lunespy.client.wallet.errors import InvalidChainAddress
from lunespy.client.wallet import Account
from pytest import raises


def test_ready_between_different_networks():
    """
        with a Account in chain `mainnet`:
            should br return Error for receiver in chain `testnet`
        else should be return True
    """
    sender_mainnet = Account(chain='mainnet')    
    receiver_testnet = Account(chain='testnet')

    with raises(InvalidChainAddress):
        tx = TransferToken(sender_mainnet, receiver_testnet, amount=1)
        tx.ready

    sender_testnet = Account(chain='testnet')
    tx = TransferToken(sender_testnet, receiver_testnet, amount=1)
    assert tx.ready == True


def test_ready_without_amount_failed_successful():
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
