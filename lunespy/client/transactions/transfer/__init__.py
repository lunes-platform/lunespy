from lunespy.client.transactions import BaseTransaction

class TransferToken(BaseTransaction):
    def __init__(self, sender: str, receiver: str, chain: str, amount: float, asset_fee: int=None, token_id: str=None, timestamp: int=None, fee: int=None) -> None:

        from lunespy.client.transactions.constants import TransferType
        from lunespy.utils import now, lunes_to_unes

        self.timestamp: int = timestamp if timestamp != None else now()
        self.fee: int = fee if fee != None else TransferType.fee.value
        self.asset_id: str = token_id if token_id != None else ""
        self.asset_fee: str = asset_fee if asset_fee != None else ""
        if self.asset_id == "":
            self.amount: int = lunes_to_unes(amount)
        else:
            self.amount: int = amount
        self.receiver: str = receiver
        self.sender: str = sender
        self.chain: str = chain
        self.chain_id: str = "1" if chain == "mainnet" else "0"
        self.history: list = []
        self._tx = None

        super().__init__('Transfer', self.__dict__)


    @property
    def ready(self) -> bool:
        from lunespy.client.transactions.transfer.validators import validate_transfer

        return validate_transfer(
            sender=self.sender,
            receiver=self.receiver,
            amount=self.amount,
            chain=self.chain
        )


    @property
    def transaction(self) -> dict:
        from lunespy.client.transactions.transfer.validators import mount_transfer

        return super().transaction(
            mount_tx=mount_transfer,
            timestamp=self.timestamp,
            asset_fee=self.asset_fee,
            receiver=self.receiver,
            asset_id=self.asset_id,
            amount=self.amount,
            sender=self.sender,
            chain_id=self.chain_id,
            fee=self.fee
        ) if not self._tx else self._tx


    def sign(self, private_key: str) -> dict:
        from lunespy.client.transactions.transfer.validators import sign_transaction

        self._tx = super().sign(
            sign_tx=sign_transaction,
            private_key=private_key,
            **self.transaction
        )
        return self._tx


    def broadcast(self, node_url: str = None) -> dict:
        from lunespy.client.transactions.transfer.validators import broadcast_transfer

        tx = super().broadcast(broadcast_transfer, node_url, self.chain)
        self.history.append(tx)
        return tx
