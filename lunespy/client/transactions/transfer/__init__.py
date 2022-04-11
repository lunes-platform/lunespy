from lunespy import wallet
from lunespy.wallet.crypto import b58_to_bytes, bytes_to_b58, to_address
from lunespy.utils import lunes_to_unes, now
from pydantic import BaseModel, Field


class TransferToken(BaseModel):
    chain: int = Field(1, ge=0, le=1, description="1 for mainnet, 0 for testnet")
    fee: int = Field(lunes_to_unes(0.01), gt=lunes_to_unes(0.01))
    senderPublicKey: str = Field(..., description="public_key")
    assetId: str = Field("", description="token id | NFT id")
    sender: int = Field("", description="address of sender")
    recipient: str = Field(..., description="address")
    timestamp: int = Field(default_factory=now)
    amount: int = Field(..., gt=0)
    signature: str = Field("")
    feeAsset: int = Field("")

    def sign(cls, private_key: str):
        cls.signature = private_key
        return cls

    def broadcast(cls):
        return 1


def transfer_token_factory(sender: str, receiver: str, amount: int):
    return TransferToken(
        sender=bytes_to_b58(to_address(b58_to_bytes(sender), 1, 1)),
        senderPublicKey=sender,
        recipient=receiver,
        amount=amount,
    )

