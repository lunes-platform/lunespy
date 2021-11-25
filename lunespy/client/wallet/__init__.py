class Account:
    """
    params: 
        private_key: str
        public_key: str
        hash_seed: str
        network_id: str | '0' xor '1'
        address: str
        nonce: int | 0 to 4.294.967.295
        network: str | 'mainnet' xor 'testnet'
        seed: str | n words
        n_words: int | n_words should be n // 3  
        byte_private_key: bytes
        byte_public_key: bytes
        byte_address: bytes
    """
    def __init__(self, **wallet: dict):
        from lunespy.client.wallet.validators import validate_wallet
        
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


    def to_json(self, path: str = '.') -> str:
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
