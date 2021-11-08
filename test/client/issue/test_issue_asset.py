from lunespy.client.transactions.issue import IssueAsset
from lunespy.client.wallet import Account

def test_asset_decimals():
    """
        with any decimals parameter:
            - should be return a same decimals parameter passed
    """
    sender = Account()
    tx = IssueAsset(sender, quantity=1, name='Asset', decimals=8)
    assert tx.issue_data['decimals'] == 8



def test_without_name_ready_failed_successful():
    """
        without a name parameter:
            - should be return False for IssueAsset.ready
            - else should be return True
    """
    # Failed
    sender = Account()
    tx = IssueAsset(sender, quantity=1)
    assert tx.ready == False

    #Successful
    tx.issue_data['name'] = 'newNFT'
    assert tx.ready == True

def test_without_quantity_ready_failed_successful():
    """
        without a quantity parameter:
            - should be return False for IssueAsset.ready
            - else should be return True
    """
    # Failed
    sender = Account()
    tx = IssueAsset(sender, name='newNFT')
    assert tx.ready == False

    #Successful
    tx.issue_data['quantity'] = 1
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a sender, receiver, amount:
            - should be return all keys of offline-transaction for Token.transaction  
    """
    sender = Account()
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

    tx = IssueAsset(sender, name='test', quantity=10)
    response = tx.transaction
    print(response)

    assert response['ready'] == True
    assert list(response.keys()) == offline_transaction



