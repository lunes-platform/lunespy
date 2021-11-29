from enum import Enum

class Node(Enum):
    mainnet_url: str = 'https://lunesnode.lunes.io'
    testnet_url: str = 'https://lunesnode-testnet.lunes.io'
    mainnet_blockexplorer: str = 'https://blockexplorer.lunes.io'
    testnet_blockexplorer: str = 'https://blockexplorer-testnet.lunes.io'
    mainnet_total_supply: float = 150_728_537.61498705
    testnet_total_supply: float = 800_100_000.00000000  