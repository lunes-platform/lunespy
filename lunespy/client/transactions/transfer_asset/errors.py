class TransferError(Exception):
    """Base error class for Transfer"""
    def __init__(self) -> None:
        super().__init__(self.__doc__)
