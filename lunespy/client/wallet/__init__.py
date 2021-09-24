from lunespy.client.wallet.validators import validate_wallet


class Account:
    def __init__(self, **wallet: dict):        
        __validated_wallet = validate_wallet(wallet)
        
        self.private_key = __validated_wallet['private_key']
        self.public_key = __validated_wallet['public_key']
        self.hash_seed = __validated_wallet['hash_seed']
        self.network_id = __validated_wallet['network_id']
        self.address = __validated_wallet['address']
        self.nonce = __validated_wallet['nonce']
        self.network = __validated_wallet['network']
        self.seed = __validated_wallet['seed']

        self.byte_private_key = __validated_wallet['byte_private_key']
        self.byte_public_key = __validated_wallet['byte_public_key']
        self.byte_address = __validated_wallet['byte_address']

    def __str__(self) -> str:
        from lunespy.utils.settings import bcolors

        return f"\
            \nseed\n {bcolors.OKGREEN + '└── ' +  self.seed + bcolors.ENDC}\
            \nnetwork\n {bcolors.OKCYAN + '└── ' + self.network + bcolors.ENDC}\
            \nnonce\n {bcolors.OKBLUE + '└── ' + str(self.nonce) + bcolors.ENDC}\
            \nprivate key\n {bcolors.OKBLUE + '└── ' + self.private_key + bcolors.ENDC}\
            \npublic key\n {bcolors.OKBLUE + '└── ' + self.public_key + bcolors.ENDC}\
            \naddress\n {bcolors.OKBLUE + '└── ' + self.address + bcolors.ENDC}"

    def __repr__(self) -> str:
        return f"seed\n └──  {self.seed}\
            \nnetwork\n └── {self.network}\
            \nnonce\n └── {str(self.nonce)}\
            \nprivate key\n └── {self.private_key}\
            \npublic key\n └── {self.public_key}\
            \naddress\n └── {self.address}"


    def to_json(self, path: str = './') -> None:
        from lunespy.utils.settings import bcolors
        import json

        wallet = {
            'seed': self.seed,
            'nonce': self.nonce,
            'private_key': self.private_key,
            'public_key': self.public_key,
            'address': self.address
        }
        with open(f'{path}wallet.json', 'w') as file:
            file.write(json.dumps(wallet))
        print(f"{bcolors.OKGREEN}Your wallet has been saved in `{path}wallet.json`{bcolors.ENDC}")