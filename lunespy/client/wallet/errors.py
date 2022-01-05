class WalletError(Exception):
    """Base error class for Wallet"""
    def __init__(self) -> None:
        super().__init__(self.__doc__)

class InvalidVersionAddress(WalletError):
    """Wrong address version"""   

class InvalidChainAddress(WalletError):
    """Wrong chain id"""

class InvalidLengthAddress(WalletError):
    """Wrong address length"""

class InvalidChecksumAddress(WalletError):
    """Wrong address checksum"""

class InvalidNonce(WalletError):
    """Nonce must be between 0 and 4294967295"""