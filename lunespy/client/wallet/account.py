from lunespy.client.wallet.validators import validate_wallet

class Account():
    def __init__(self, **wallet: dict):
        validated_wallet = validate_wallet(wallet)
        self.byte_private_key = validated_wallet['private_key']
        self.private_key = str(self.byte_private_key)[2:-1]

        self.byte_public_key = validated_wallet['public_key']
        self.public_key = str(self.byte_public_key)[2:-1]
        
        self.byte_address = validated_wallet['address']
        self.address = str(self.byte_address)[2:-1]
        
        self.nonce = validated_wallet['nonce']
        self.seed = validated_wallet['seed']