from lunespy.client.wallet import Account


def validate_lunex(sender: Account, lunex_data: dict) -> bool:
    return True    


def mount_lunex(sender: Account, lunex_data: dict) -> dict:
    return {
        'type': 1,
        'senderPublicKey': 'str',
        'signature': 'str',
        'timestamp': 1,
        'matcherFee': 1,

        'matcherPublicKey': 'str',
        'expiration': 1,
        'orderType': 'str',
        'amount': 1,
        'price': 1,
        'assetPair': {
            'amountAsset': 'str',
            'priceAsset': 'str'
        }
    }


def send_lunex():
    ...
