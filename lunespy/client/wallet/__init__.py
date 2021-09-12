from lunespy.client.wallet.validators import validate_wallet

class Account:
    def __init__(self, **wallet: dict):
        validated_wallet = validate_wallet(wallet)
        
        self.private_key = validated_wallet['private_key']
        self.public_key = validated_wallet['public_key']
        self.address = validated_wallet['address']
        self.nonce = validated_wallet['nonce']
        self.seed = validated_wallet['seed']

        self.byte_private_key = validated_wallet['byte_private_key']
        self.byte_public_key = validated_wallet['byte_public_key']
        self.byte_address = validated_wallet['byte_address']

    def __str__(self) -> str:
        from lunespy.utils.settings import bcolors

        return f"\
            \nseed\n {bcolors.OKGREEN + '└──' +  self.seed + bcolors.ENDC}\
            \nnonce\n {bcolors.OKBLUE + '└──' + str(self.nonce) + bcolors.ENDC}\
            \nprivate key\n {bcolors.OKBLUE + '└──' + self.private_key + bcolors.ENDC}\
            \npubliv key\n {bcolors.OKBLUE + '└──' + self.public_key + bcolors.ENDC}\
            \naddress\n {bcolors.OKBLUE + '└──' + self.address + bcolors.ENDC}"

    __repr__ = __str__

