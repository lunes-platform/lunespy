class Account:
    """
    This is a class for Wallet Account.

    Parameters: 
        private_key(str): The pivate key of your wallet.
        public_key(str): The public key of your wallet.
        hash_seed(str): The seed of your wallet hashed.
        network_id(str): The id of your network. | '0' xor '1'
        address(str): The address of your wallet.
        nonce(int): The ip of your nonce. | 0 to 4.294.967.295
        network(str): The network of your node. | 'mainnet' xor 'testnet'
        seed(str): The seed of your wallet. | n words
        n_words(int): The amount words of your seed wallet. | n_words should be n // 3  
        byte_private_key(bytes): The byte of your wallet private key.
        byte_public_key(bytes): The byte of your wallet public key.
        byte_address(bytes): The byte of your wallet address
    """

    def __init__(self, n_words: int = None, seed: str = None, nonce: int = None,
                 network: str = None, private_key: str = None, public_key: str = None,
                 hash_seed:str = None, network_id: str = None, address: str = None) -> None:
        from lunespy.client.wallet.validators import validate_wallet
        from lunespy.utils import drop_none

        wallet: dict = drop_none({
            'private_key': private_key,
            'public_key': public_key,
            'hash_seed': hash_seed,
            'network_id': network_id,
            'address': address,
            'nonce': nonce,
            'network': network,
            'seed': seed,
            'n_words': n_words
        })

        self.__dict__ = validate_wallet(wallet)


    def __str__(self) -> str:
        from lunespy.utils import bcolors

        data = ''
        for key, value in self.__dict__.items():
            if 'byte' not in key and 'id' not in key:
                data += f"\n{key}{bcolors.OKGREEN}\n └── {value}{bcolors.ENDC}"
        return data


    def __repr__(self) -> str:
        data = ''
        for key, value in self.__dict__.items():
                data += f"{key} -> {value}\n"
        return data


    def to_json(self, path: str = './data/') -> str:
        from lunespy.utils import export_json

        data = {
            key: value 
            for (key, value) in self.__dict__.items()
            if 'byte' not in key and 'id' not in key
        }

        return export_json(
            data=data,
            name=f'wallet-{self.network}',
            path=path
        )


class LunexAccount(Account):
    """
    params: 
        public_key: str
        network: str | 'mainnet' xor 'testnet'
        url: str | 'http://ip:port'
    """
    def __init__(self, **data):
        super().__init__(**data)
        self.url: str  = data['url']
