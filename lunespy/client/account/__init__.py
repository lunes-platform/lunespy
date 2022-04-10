class Wallet:
    """
    This is a class for Wallet.

    Parameters: 
        private_key(str): The pivate key of your wallet.
        public_key(str): The public key of your wallet.
        hash_seed(str): The seed of your wallet hashed.
        chain_id(str): The id of your chain. | '0' xor '1'
        address(str): The address of your wallet.
        nonce(int): The ip of your nonce. | 0 to 4.294.967.295
        chain(str): The chain of your node. | 'mainnet' xor 'testnet'
        seed(str): The seed of your wallet. | n words
        n_words(int): The amount words of your seed wallet. | n_words should be n // 3
    """

    def __init__(self, n_words: int = None, seed: str = None, nonce: int = None,
                 chain: str = None, private_key: str = None, public_key: str = None,
                 address: str = None, address_version: int = None) -> None:
        from lunespy.client.account.utils import new

        self.__dict__ = new(n_words, seed, nonce, chain, private_key, public_key, address, address_version)

    def __str__(self) -> str:
        from lunespy.utils import bcolors

        data = ''
        for key, value in self.__dict__.items():
            if 'byte' not in key and 'id' not in key:
                data += f"\n{key}{bcolors.OKGREEN}\n └── {value}{bcolors.ENDC}"
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
            name=f'wallet-{self.chain}',
            path=path
        )


class LunexWallet(Wallet):
    """
    params: 
        public_key: str
        chain: str | 'mainnet' xor 'testnet'
        url: str | 'http://ip:port'
    """
    def __init__(self, **data):
        super().__init__(**data)
        self.url: str  = data['url']
