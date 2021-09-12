from lunespy.client.wallet.validators import validate_wallet

class Account:
    def __init__(self, **wallet: dict):
        validated_wallet = validate_wallet(wallet)
        self.byte_private_key = validated_wallet['private_key']
        self.private_key = str(self.byte_private_key)[2:-1]

        self.byte_public_key = validated_wallet['public_key']
        self.public_key = str(self.byte_public_key)[2:-1]
        
        if type(validated_wallet['address']) == bytes:
            self.byte_address = validated_wallet['address']
            self.address = str(self.byte_address)[2:-1]
        else:
            self.address = validated_wallet['address']
        
        self.nonce = validated_wallet['nonce']
        self.seed = validated_wallet['seed']

    def __str__(self) -> str:
        from lunespy.utils.settings import bcolors

        return f"seed\n {bcolors.OKGREEN + '└──' +  self.seed + bcolors.ENDC}\
            \nnonce\n {bcolors.OKGREEN + '└──' + str(self.nonce) + bcolors.ENDC}\
            \nprivate key\n {bcolors.OKGREEN + '└──' + self.private_key + bcolors.ENDC}\
            \npubliv key\n {bcolors.OKGREEN + '└──' + self.public_key + bcolors.ENDC}\
            \naddress\n {bcolors.OKGREEN + '└──' + self.address + bcolors.ENDC}"

    __repr__ = __str__

