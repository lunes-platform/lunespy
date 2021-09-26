from lunespy.client.transactions.issue import IssueNFT
from lunespy.client.wallet import Account

def test_nft_ready():
    """
        with decimals parameter iquals or more than :
            - should be return tx.issue_data['decimals'] iquals 0
    """
    creator = Account()
    tx = IssueNFT(creator, name="NFT!", quantity=1, decimals=10)
    assert tx.issue_data['decimals'] == 0


def test_without_name_ready_failed_successful():
    """
        without a name parameter:
            - should be return False for IssueNFT.ready
            - else should be return True
    """
    # Failed
    creator = Account()
    tx = IssueNFT(creator, quantity=1)
    assert tx.ready == False

    #Successful
    tx.issue_data['name'] = 'newNFT'
    assert tx.ready == True

def test_without_quantity_ready_failed_successful():
    """
        without a quantity parameter:
            - should be return False for IssueNFT.ready
            - else should be return True
    """
    # Failed
    creator = Account()
    tx = IssueNFT(creator, name='newNFT')
    assert tx.ready == False

    #Successful
    tx.issue_data['quantity'] = 1
    assert tx.ready == True


def test_transaction_full_data():
    """
        with a creator, receiver, amount:
            - should be return all keys of offline-transaction for Token.transaction  
    """
    creator = Account()
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

    tx = IssueNFT(creator, name='test', quantity=10)
    response = tx.transaction
    print(response)

    assert response['ready'] == True
    assert list(response.keys()) == offline_transaction



