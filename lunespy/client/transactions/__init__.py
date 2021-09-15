class BaseTransaction:
    def __init__(self) -> None:
        pass

    @property
    def ready(self) -> bool:
        pass

    @property
    def transaction(self) -> dict:
        pass

    @property
    def send(self) -> dict:
        pass